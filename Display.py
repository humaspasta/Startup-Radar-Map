from dash import Dash , html, dcc
import plotly.express as px
import pandas as pd
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
        Retrieves and holds lasso data
        '''
        self.lasso_data = selected_points

    def export_lasso(self):
        '''
        Exports the set of points retrieved in the lasso. 
        '''
        
        pass



    def update_log(self):
        '''
        
        '''
        pass

