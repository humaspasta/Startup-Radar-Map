import pandas as pd
import json
import sqlite3 as sql
import dotenv as env
import os
from sentence_transformers import SentenceTransformer
import requests as rq


class Processing:

    def __init__(self):
        
        env.load_dotenv('info.env') 
        db_path = os.getenv('DB_FILE', 'meta.sqlite')
        self.conn = sql.connect(db_path) #making connecting to response sql database
        self.cursor = self.conn.cursor()
        self.BASE_URL = 'https://api.perplexity.ai/chat/completions' #The url we use to make requests to SONAR API
        self.max_tokens = 200 # The maximum number of tokens that SONAR should use per response # A token is about 4 words this means nothing will be returned in response to the call I believe...
        self.temperature = 0.2 #a value that determines how syntactically creative a response should be. 

        self.headers = {
            "Authorization": f"Bearer {os.environ['API_KEY']}",
            "Content-Type": "application/json"
        } #api key and format of information sent in request

       

        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.vectors_path = 'vectors.parquet'
        self.sentance_number = 0

        create_table = """CREATE TABLE IF NOT EXISTS  startup_info ( 
            link TEXT NOT NULL PRIMARY KEY,
            Summary TEXT NOT NULL,
            Name TEXT NOT NULL,
            Sector TEXT NOT NULL,
            Funding_Stage TEXT NOT NULL,
            Sources TEXT NOT NULL
        );
        """
        self.cursor.execute(create_table) 
        self.conn.commit()

    def scrape(self, link:str) -> str:

        '''
        Gets a JSON file containing information of a given startup for caching.
        Uses perplexity SONAR for retrieving website information. Stores information in sql database. 
        '''
        
        self.cursor.execute('''SELECT 1 FROM startup_info WHERE link = ? LIMIT 1''' , (link,))
        result = self.cursor.fetchone() #fetches result of cursor execute

        if result: #if result is not null then the result already exists in the database and it will return that reuslt
            return result
        else:
            #Providing information to sonar on what is needed, how to format the information requested, and the amount of resources it should consume.
            other_data = {
                "model": "sonar",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional buisness analyst. For any given link to a company, provide a structured analysis including: the company name; the industry sector; a summary on their key products and services, recent performance, and strengths and weaknesses; and the funding stage they are in. Keep it under 200 words."
                    },
                    {
                        "role": "user",
                        "content": f"Analyze the follwing link {link}"
                    }
                ]
                ,
                "response_format": {
                    'type' : "json_schema",
                    'json_schema' : {
                        'schema' : {
                            'type':'object',
                            'properties' :
                            {
                                'Name' : {'type' :  'string'},
                                'Summary' : {'type' : "string"},
                                'Sector': {'type' : 'string'},
                                'Funding_Stage' :  {'type' : 'string'},
                                'sources' : {
                                    'type' : 'array',
                                   
                                }
                            },
                            'required' : ['Name' , 'Summary' , 'Sector' , 'Funding_Stage' , 'sources']
                        }
                    }
                },
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                'search_mode' : 'academic',
                'search_after_date' : '1/1/2022',
            }
            try:
                response = rq.request('POST', url=self.BASE_URL, headers = self.headers, json=other_data, timeout=8) # sending a request to perplexity API to retrieve data
                response.raise_for_status()
            except:
                print('Time our occured. Moving on to next link.')
                return
            
            result = response.json()
            try:
                structured_data = json.loads(result["choices"][0]["message"]["content"])
            except:
                print('Malformed Json, skipping')
                return
        


            self.store(structured_data , link)

            return structured_data['Summary']#returning summary string
      

          
    
    def store(self, response:dict , link:str) -> None:
        '''
        Stores the link along with detailed information about the startup in that link in sqlite database.
        link: The link analyzed
        Summary: Summary of the startup
        Sector: Sector of the startup
        Funding_Stage: The startups current funding state
        Sources: A list of sources used in Sonar's analysis of the startup
        '''
        
        #creating the table where data will be stored in the database
        self.cursor.execute('''INSERT INTO startup_info(link, Summary,  Name, Sector, Funding_Stage, sources) VALUES (? , ?, ?, ?, ?, ?)''' ,
                             (link , response['Summary'], response['Name'], response['Sector'], response['Funding_Stage'], str(response['sources'])[1:-1])) #caching summary using the link as the key
        
        self.conn.commit()#saving changes to database 
    
    
    def vectorize_all(self):
        data = pd.read_sql_query('SELECT * FROM startup_info', self.conn) # load startup info into a DF
        if 'Summary' not in data.columns:
            raise ValueError("'summary' column's missing")
        
        summaries = data['Summary'].fillna("").tolist() # exctrs summaries into a list and fills NaNs wiht empty strings


        vectors = self.model.encode(summaries)

        metadata_columns = ['Name', 'Sector', 'Summary' , 'Funding_Stage'] #  columns here are defined as the metadata
        for col in metadata_columns: 
            if col not in data.columns:
                raise ValueError(f"missing '{col}'")
            
        metadata = data[metadata_columns] # slicing out metadata cols into their own DF

        df_vectors = pd.DataFrame(vectors) # turns the numpy arry of vectors into a new DF

        concatenated = pd.concat([metadata.reset_index(drop=True), df_vectors], axis=1) # horizontal concatenization of metadata and DFs

        concatenated.columns = concatenated.columns.map(str) #converting column to strings for parqet
        concatenated.to_parquet(self.vectors_path, index=False)


    def store_vector(self):
        df = pd.read_parquet(self.vectors_path)
        metadata = df.iloc[:, :4] # slices off metadata
        vectors = df.iloc[:, 4:] # remaining cols are the vect embeddings

        return vectors, metadata
    


