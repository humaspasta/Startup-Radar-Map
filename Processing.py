import pandas as pd
import json
import sqlite3 as sql
import dotenv as env
import os
class Processing:

    def __init__(self , data_path):
        self.conn = sql.connect('')
        env.load_dotenv('info.env') #loading .env file

        self.data = pd.read_csv(data_path)

    def scrape(self, link:str):
        '''
        Gets a JSON file containing information of a given startup for caching.
        Uses perplexity SONAR for retrieving website information. Stores information in sql database
        '''

        output = ...
        json_text = json.dumps(output)
        self.store_JSON(json_text)
      

          
    
    def store_JSON(filename:str):
        '''
        Stores the JSON file in a sqlite database
        '''
        pass

    def vectorize(startup:str):
        '''
        Vectorizes the startup 
        '''
        pass

    def store_vector(vector):
        '''
        imbedds the vector into a given parquet file
        '''
        pass

    





