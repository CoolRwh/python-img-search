import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))
elastic_url = os.environ.get('ELASTIC_SEARCH_URL',"http://elastic:123456@127.0.0.1:9200")
if __name__ == '__main__':
    
    print(bool("0"))
    
    
