import pandas as pd
import json
import sqlite3 as sql
import dotenv as env
import os
import requests as rq
class Processing:

    def __init__(self , data_path):
        self.conn = sql.connect('SonarResponses.db')
        env.load_dotenv('info.env') #loading .env file
        self.BASE_URL = "some url"
        self.max_tokens = ...
        self.temperature = 0
        self.headers = {
            "Authorization": f"Bearer {os.environ('API_KEY')}",
            "Content-Type": "application/json"
        }

        self.data = pd.read_csv(data_path)

    def scrape(self, link:str):
        '''
        Gets a JSON file containing information of a given startup for caching.
        Uses perplexity SONAR for retrieving website information. Stores information in sql database
        '''
        other_data = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides interesting, accurate, and concise facts. Respond with a summary, a sector label, and all the sources used to come to the conclusions you did in your sector label, kept under 100 words."
                },
                {
                    "role": "user",
                    "content": f"Given the following link, provide a summary of the startup which includes what they do and their goal for the future. Also provide a label for the sector this company is in as well as all the sources you used. Feel free to use sources outside of this one "
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        response = rq.post(url=self.BASE_URL, data = other_data, json=other_data, timeout=30) # sending a request to perplexity API to retrieve data
        response.raise_for_status()
        
        json_text = json.dumps(response.json)

        self.store_result(json_text)
      

          
    
    def store_JSON(self, response:str):
        '''
        Stores the JSON file in a sqlite database
        '''
        with self.conn.cursor() as cursor:
            cursor.execut('CREATE TABLE IF NOT EXISTS str') #will come back to this later. This is for sure not the right way of storing. 

        

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

    





