import requests
import sqlalchemy 
import pandas as pd

from io import StringIO

def get_data():
    base_url = "https://api.acleddata.com/acled/read.csv"
    params = {
        "limit": 2000
    }

    # NOTE: setting verify to false is STRONGLY discouraged
    # This setting is only used in development due to restrictions
    # In my current environement, and should be disabled whenever possible
    r = requests.get(base_url, params=params, verify=False)
    wrap = StringIO(r.text)
    df = pd.read_csv(wrap)
    
    return df
