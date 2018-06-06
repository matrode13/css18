#Task 2.2 Data Aquisition
import os
import urllib
import json
import pickle
import pytrends
import pandas as pd
from pytrends.request import TrendReq

dataDirectory=".."
#create a new directory for the interest_over_time
timeDirectory="interest_over_time"
meberListJsonPath=os.path.join(dataDirectory, "memberList.json")

with open(meberListJsonPath) as meberListJsonFile:
    #load the local copy of the parliaments list file
    members = json.load(meberListJsonFile)
    
    for memberUuid in members:
        
        currentPath=os.path.join(dataDirectory, timeDirectory, memberUuid+".pickle")
        
        #check if file already exists
        if not os.path.isfile(currentPath): 
        
            #get firstName and lastName to search for
            firstName = members[memberUuid]["firstName"]
            lastName = members[memberUuid]["lastName"]
            name = firstName +" " + lastName
            print("Working on " +name)
            if name=="Angela Merkel":
                continue
            pytrends = TrendReq(hl='de-DE', tz=360)
            kw_list = [name, "Angela Merkel"]
            pytrends.build_payload(kw_list, cat=396, timeframe='today 5-y', geo='', gprop='')
            #cat=396 is the category for politics on google trends, sse here: https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories
            df = pd.DataFrame(pytrends.interest_over_time())
            df.to_pickle(currentPath)
            if df["Angela Merkel"].max() == 100:
                continue
            else:
                print("Higher volume "+name)
            sleep(30)
        else:
            #print progress
            print('.', end='')
