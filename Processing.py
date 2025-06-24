import pandas as pd
import json
import sqlite3 as sql
import dotenv as env
import os
from sentence_transformers import SentenceTransformer
class Processing:

    def __init__(self , data_path):
        self.conn = sql.connect('')
        env.load_dotenv('info.env') 
        db_path = os.getenv('DB_FILE', 'startups.db')
        self.data = pd.read_csv(data_path)

        self.model = SentenceTranformer('all-MiniLM-L6-v2')

        self.vectors_path = 'vectors.parquet'

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

    def vectorize_all(self):
        if 'summary' not in self.data.columns:
            raise ValueError("'summary' column's missing")
        
        summaries = self.data['summary'].fillna("").tolist()


        vectors = self.model.encode(summaries)

        metadata_columns = ['statup_name', 'homepage_url', 'sector', 'funding_stage']
        for col in metadata_columns: 
            if col not in self.data.columns:
                raise ValueError(f"missing '{col}'")
            
        metadata = self.data[metadata_columns]

        df_vectors = pd.DataFrame(vectors)

        concatenated = pd.concat([metadata.reset_index(drop=True), df_vectors], axis=1)

        concatenated.to_parquet(self.vectors_path, index=false)


    def store_vector(self):
        df = pd.read_parquet(self.vectors_path)
        metadata = df.iloc[:, :4]
        vectors = df.iloc[:, 4:]

        return vectors, metadata
    


