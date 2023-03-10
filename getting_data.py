# So at the beggining it looked like this, that was my first research for this project
# In first try I did only 1 search so got 10 new jobs back, then i was searching for about 100 results daily

from serpapi import GoogleSearch
import numpy as np
import pandas as pd
import datetime
api_key = 'd9e1f7d32270c69ad8a9a1a657a16bc1fc98e3c32d6b99fd67c1d2167d66790b'

for num in range(10):

            start = num * 10
            search_loc = 'United States'

            search = GoogleSearch({
            "q":'data analyst',
            "api_key":api_key ,
            "device":'desktop',
            "engine":'google_jobs',
            'hl':'en',
            'location':search_loc,
            'chips':'date_posted:today',
            'start':start,
            })

            # check if the last search page (i.e., no results)
            results = search.get_dict()
            try:
                if results['error'] == "Google hasn't returned any results for this query.":
                    break
            except KeyError:
                print(f"Getting SerpAPI data for page: {start}")
            else:
                continue

            #converting into Data frame

            jobs_df = results['jobs_results']
            jobs_df = pd.DataFrame(jobs_df)
            jobs = pd.concat([pd.DataFrame(jobs_df),
                               pd.json_normalize(jobs_df['detected_extensions'])],
                               axis=1).drop('detected_extensions',1)
            jobs['date_time'] = datetime.datetime.utcnow()

            #concat DataFrame
            if start == 0:
                jobs_all = jobs
            else:
                jobs_all = pd.concat([jobs_all, jobs])

            jobs_all['search_term'] = 'data analyst'
            jobs_all['search_location'] = search_loc

# then I concatenated them and saved as csv
#concatenating first search with next
test_jobs = jobs_all
result = pd.concat([jobs_all,test_jobs])
result.to_csv('analiza-ofert.csv')

# later I put it into function do_stuff()
#And everyday I looked for new job offers and added them to csv file as below, by concatenating
def do_stuff():
    from serpapi import GoogleSearch
    import numpy as np
    import pandas as pd
    import datetime
    api_key = 'd9e1f7d32270c69ad8a9a1a657a16bc1fc98e3c32d6b99fd67c1d2167d66790b'

    for num in range(10):

        start = num * 10
        search_loc = 'United States'

        search = GoogleSearch({
        "q":'data analyst',
        "api_key":api_key ,
        "device":'desktop',
        "engine":'google_jobs',
        'hl':'en',
        'location':search_loc,
        'chips':'date_posted:today',
        'start':start,
        })

        # check if the last search page (i.e., no results)
        results = search.get_dict()
        try:
            if results['error'] == "Google hasn't returned any results for this query.":
                break
        except KeyError:
            print(f"Getting SerpAPI data for page: {start}")
        else:
            continue

        #converting into Data frame

        jobs_df = results['jobs_results']
        jobs_df = pd.DataFrame(jobs_df)
        jobs = pd.concat([pd.DataFrame(jobs_df),
                           pd.json_normalize(jobs_df['detected_extensions'])],
                           axis=1).drop('detected_extensions',1)
        jobs['date_time'] = datetime.datetime.utcnow()

        #concat DataFrame
        if start == 0:
            jobs_all = jobs
        else:
            jobs_all = pd.concat([jobs_all, jobs])

        jobs_all['search_term'] = 'data analyst'
        jobs_all['search_location'] = search_loc
    
    return jobs_all


df = do_stuff()
df1 = pd.read_csv('analiza-ofert.csv')
result = pd.concat([df,df1])
result.to_csv('analiza-ofert.csv')
# last search in US returned only few results so I changed location to United Kingdom and used all free searches that left to look for offers from previous week

def do_stuff2():
    from serpapi import GoogleSearch
    import numpy as np
    import pandas as pd
    import datetime
    api_key = 'd9e1f7d32270c69ad8a9a1a657a16bc1fc98e3c32d6b99fd67c1d2167d66790b'

    for num in range(17):

        start = num * 10
        search_loc = 'United Kingdom'

        search = GoogleSearch({
        "q":'data analyst',
        "api_key":api_key ,
        "device":'desktop',
        "engine":'google_jobs',
        'hl':'en',
        'location':search_loc,
        'chips':'date_posted:week',
        'start':start,
        })

        # check if the last search page (i.e., no results)
        results = search.get_dict()
        try:
            if results['error'] == "Google hasn't returned any results for this query.":
                break
        except KeyError:
            print(f"Getting SerpAPI data for page: {start}")
        else:
            continue

        #converting into Data frame

        jobs_df = results['jobs_results']
        jobs_df = pd.DataFrame(jobs_df)
        jobs = pd.concat([pd.DataFrame(jobs_df),
                           pd.json_normalize(jobs_df['detected_extensions'])],
                           axis=1).drop('detected_extensions',1)
        jobs['date_time'] = datetime.datetime.utcnow()

        #concat DataFrame
        if start == 0:
            jobs_all = jobs
        else:
            jobs_all = pd.concat([jobs_all, jobs])

        jobs_all['search_term'] = 'data analyst'
        jobs_all['search_location'] = search_loc
    
    return jobs_all
    
#getting results
df = do_stuff()
df1 = do_stuff2()

#concatenating them
df = pd.concat([df,df1])

#reading data from previous searches and concatenating with new data
df1 = pd.read_csv('analiza-ofert.csv')
df2 = pd.concat([df,df1])

# saving final csv file
df2.to_csv('analiza-ofert-final.csv')

# And I added all the data to my database to ensure I won't lose anything by mistake
import pandas as pd
import sqlalchemy
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/oferty_pracy')
df2.to_sql('oferty',con=engine,index=False,if_exists='append')