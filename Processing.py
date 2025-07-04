import pandas as pd
import json
import sqlite3 as sql
import dotenv as env
import os
from sentence_transformers import SentenceTransformer
import requests as rq


class Processing:

    def __init__(self , data_path):
        
        env.load_dotenv('info.env') 
        db_path = os.getenv('DB_FILE', 'meta.sqlite')
        self.conn = sql.connect(db_path) #making connecting to response sql database
        self.cursor = self.conn.cursor()

        self.BASE_URL = "some url" #The url we use to make requests to SONAR API
        self.max_tokens = 0 # The maximum number of tokens that SONAR should use per response # A token is about 4 words this means nothing will be returned in response to the call I believe...
        self.temperature = 0 #a value that determines how syntactically creative a response should be. 

        self.headers = {
            "Authorization": f"Bearer {os.environ['API_KEY']}",
            "Content-Type": "application/json"
        } #api key and format of information sent in request

        self.data = pd.read_csv(data_path)

        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.vectors_path = 'vectors.parquet'
        self.sentance_number = 0

    def scrape(self, link:str) -> str:

        '''
        Gets a JSON file containing information of a given startup for caching.
        Uses perplexity SONAR for retrieving website information. Stores information in sql database. 
        '''
        
        self.cursor.execute('''SELECT 1 FROM link WHERE link = ? LIMIT 1''' , (link))
        result = self.cursor.fetchone() #fetches result of cursor execute

        if result: #if result is not null then the result already exists in the database and it will return that reuslt
            return result
        else:
            other_data = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides interesting, accurate, and concise facts. Respond with a summary, a sector label, and all the sources used to come to the conclusions you did in your sector label, kept under 100 words."
                    },
                    {
                        "role": "user",
                        "content": f"Given the following link {link}, provide a summary of the startup this link refers too which includes what they do and their goal for the future. Also provide a label for the sector this company, what funding stage they are in, as well as all the sources you used. Feel free to use sources outside of this one "
                    }
                ],
                "response_format": {
                    'type' : "json_schema",
                    'json_schema' : {
                        'schema' : {
                            'type':'object',
                            'properties' :
                            {
                                'Name' : {'type' ,  'string'},
                                'Summary' : {'type' : "string"},
                                'Sector': {'type' : 'string'},
                                'Funding_Stage' :  {'type' : 'string'},
                                'sources' : {
                                    'type' : 'array',
                                    'items' : {'type' : 'string'}
                                }
                            },
                            'required' : ['Name' , 'Sumary' , 'Sector' , 'Funding_Stage' , 'sources']
                        }
                    }
                },

                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }

            response = rq.post(url=self.BASE_URL, data = self.headers, json=other_data, timeout=30) # sending a request to perplexity API to retrieve data
            response.raise_for_status()
            
            result = response.json()

            structured_data = json.loads(result["choices"][0]["message"]["content"])


            self.store(structured_data , link)

            return structured_data['Summary']#returning summary string
      

          
    
    def store(self, response:dict , link:str) -> None:
        '''
        Stores the link , summary pair in sqlite database.
        '''
        
        #creating the table where data will be stored in the database
        create_table = """CREATE TABLE IF NOT EXISTS  startup_info ( 
            link TEXT NOT NULL PRIMARY,
            Summary TEXT NOT NULL,
            Sector TEXT NOT NULL,
            Funding_Stage TEXT NOT NULL,
            Sources TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table) 
        self.cursor.execute(''' 
        INSERT INTO startup_info(link, summary,  Sector, Funding_Stage, sources) VALUES (? , ?, ?, ?)
            ''' , (link , response['Summary'], response['Sector'], response['Funding_Stage'], response['sources'])) #caching summary using the link as the key
        
        self.conn.commit()#saving changes to database 
    
    
    def vectorize_all(self):
        data = pd.read_sql_query('SELECT * FROM startup_info', self.conn) # load startup info into a DF
        if 'summary' not in data.columns:
            raise ValueError("'summary' column's missing")
        
        summaries = data['summary'].fillna("").tolist() # exctrs summaries into a list and fills NaNs wiht empty strings


        vectors = self.model.encode(summaries)

        metadata_columns = ['statup_name', 'sector', 'funding_stage'] #  columns here are defined as the metadata
        for col in metadata_columns: 
            if col not in data.columns:
                raise ValueError(f"missing '{col}'")
            
        metadata = data[metadata_columns] # slicing out metadata cols into their own DF

        df_vectors = pd.DataFrame(vectors) # turns the numpy arry of vectors into a new DF

        concatenated = pd.concat([metadata.reset_index(drop=True), df_vectors], axis=1) # horizontal concatenization of metadata and DFs

        concatenated.to_parquet(self.vectors_path, index=False)


    def store_vector(self):
        df = pd.read_parquet(self.vectors_path)
        metadata = df.iloc[:, :3] # slices off metadata
        vectors = df.iloc[:, 3:] # remaining cols are the vect embeddings

        return vectors, metadata
    


