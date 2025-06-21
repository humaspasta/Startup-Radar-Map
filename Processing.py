import pandas as pd
import json

class Processing:
    def scrape(filename:str):
        '''
        Gets a JSON file containing information of a given startup for caching.
        Uses perplexity SONAR for retrieving website information.
        '''

        '''
        
        
        '''

        info_dict = {}

        startups_df = None
        try:
            csv = pd.read_csv(filename)
        except FileNotFoundError as fl:
            print("File " + filename +" not found. Check if file exists or if name is correct.")
            return
        except Exception as e:
            print("Something else went wrong: " + e)
            return

        rows = startups_df['homepage_url']

        for link in rows:
            #code for retrieving JSON data for each file
            output = ...
            json_object = json.dumps(output)

          
        
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

    





