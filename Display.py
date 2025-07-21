import datetime
from dash import Dash , html, dcc
import plotly.express as px
import pandas as pd
import os 
import json 
import numpy as np 
import umap 
from Processing import Processing

import os
class Display_Data:

    def __init__(self, data_path: str ='startup.csv'):
        self.processor = Processing()
        self.lasso_data = []
        self.umap_model = umap.UMAP(n_components=2, random_state=42) #umap reducer for 2d projection fits once and then transforms 
        
        self._fitted = False 
        self.data = pd.read_csv(data_path)
        self._projections=None
        self._metadata = None
        self.processor.vectorize_all()
        
    def project_vector_2d(self , vectors: np.ndarray)-> np.ndarray:
        
        arr = np.array(vectors)
        if not self._fitted: # fits map on the first call then reuse for consistent projections
            coords = self.umap_model.fit_transform(arr)
            self._fitted = True
        else: 
            coords = self.umap_model.transform(arr)
        return coords


    def get_plottable_vectors(self) -> pd.DataFrame:
        '''
        Returns a pandas dataframe with the columns: X points , Y points, Startup Name, Summary, Sector, Funding Stage, sources
        X points and Y Points will be used for plotting in 2d and  Startup Name, Summary, Sector, Funding Stage, sources will be used
        in the hovercard to display information
        '''
        vectors_df, meta_df= self.processor.store_vector() # retrieve stored vects and metadata

        coords = self.project_vector_2d(vectors_df.values) #proj all vects at once to 2d
        df_coords = pd.DataFrame(coords, columns=['x','y'])

        df_meta = meta_df.reset_index(drop=True) # align meta data 
        df= pd.concat([df_coords, df_meta], axis=1)

        return df
        

    def preserve_lasso(self , selected_points):
        '''
        Retrieves and stores lasso data
        '''
        self.lasso_data = selected_points

    def export_lasso(self) -> None:
        '''
        Exports the set of points retrieved in the lasso. 
        '''
        if len(self.lasso_data) != 0:
            unique_values = list(set(tuple(row) for row in self.lasso_data))

            data_interst = pd.DataFrame(unique_values , columns=['x' , 'y' , 'Summary', 'Name' , 'Sector' , 'Sources'])
            data_interst.to_csv(os.path.join('.' , 'SelectedData.csv')) #create csv or overwrite it if it already exists
            return dcc.send_file(os.path.join('.' , 'SelectedData.csv'))

    def update_log(self):
        '''
        returns a simple one-line log saying when the main data file was last updated 
        '''
        path = self.processor.vectors_path ## will add more functionality to this..
        if os.path.exist(path):
            mtime = os.path.getmtime(path)
            ts = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            return f"Data last ingested on **{ts}**"
        else: 
            return "No ingestion data found"

    def scrape_all_links(self) -> None:
        '''
        Scrapes all links in startup.csv file and saves them to database using scrape method in Processing(). 
        '''
        links = self.data['Links']
        for link in links:
            
            self.processor.scrape(link)
    
    def clear_cache(self) -> None:
        '''
        Clears the startup_data table in the sql database
        '''
        self.processor.cursor.execute('''
            DELETE FROM startup_info
        ''')
        self.processor.conn.commit()