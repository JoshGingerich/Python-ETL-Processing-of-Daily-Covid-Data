import pandas as pd

nyurl = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv'
jhurl = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'

def extract_and_merge(url1, url2):
    try:
        #import and clean nyt data, convert date from object to date type, remove uncommon dates from john hopkins
        nyt = pd.read_csv(url1)

        nytclean = nyt[(nyt.date != '2020-01-21')]
        nytclean.date = pd.to_datetime(nytclean.date)
        #print(nytclean.info())

        #import and clean john hopkins data, only grab USA data, convert date from object to date type and rename as date for join operation
        jh = pd.read_csv(url2)

        jhus = jh[jh['Country/Region']=='US']
        jhus.Date = pd.to_datetime(jhus.Date)
        jhus = jhus.rename(columns={"Date" : "date"})
        jhus.Recovered = jhus.Recovered.astype(int)
        #print(jhus.info())


        #merge nyt and jh data together on date column only show attributes of date, cases, deaths, and recovered
        covid = pd.merge_asof(nytclean,jhus, on='date')
        covid = covid[['date','cases','deaths','Recovered']]
        covid.date = covid.date.astype(str)
        #print(covid.info())
        #print(covid)
        return(covid)
    except Exception as error:
        print(error)
        exit(1)