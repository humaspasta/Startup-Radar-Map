from dash import Dash , html, dcc
import plotly.express as px
import pandas as pd
import os
class Display_Data:

    def __init__(self):
        self.lasso_data = []


    
    def project_vector_2d(self , vector):
        '''
        Projects a vector to 2d
        '''
        pass


    def get_plottable_vectors(self) -> pd.DataFrame:
        '''
        Returns a pandas dataframe with the columns: X points , Y points, Startup Name, Summary, Sector, Funding Stage, sources
        X points and Y Points will be used for plotting in 2d and  Startup Name, Summary, Sector, Funding Stage, sources will be used
        in the hovercard to display information
        '''
        pass



        '''
        I will work on both lasso methods
        '''
    def preserve_lasso(self , selected_points):
        '''
        Retrieves and stores lasso data
        '''
        self.lasso_data = selected_points
        print(selected_points)

    def export_lasso(self) -> None:
        '''
        Exports the set of points retrieved in the lasso. 
        '''
        if len(self.lasso_data) != 0:
            unique_values = list(set(tuple(row) for row in self.lasso_data))

            data_interst = pd.DataFrame(unique_values , columns=['x' , 'y' , 'Startup Name' , 'Sector' , 'Summary' , 'Sources'])
            data_interst.to_csv(os.path.join('.' , 'SelectedData.csv')) #create csv or overwrite it if it already exists
            return dcc.send_file(os.path.join('.' , 'SelectedData.csv'))

    def update_log(self):
        '''
        
        '''
        pass

