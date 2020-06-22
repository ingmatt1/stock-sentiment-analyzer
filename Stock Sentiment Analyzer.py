from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt

def sentiment(sentiment_df):
    score_list = []
    
    for index, row in sentiment_df.iterrows():
        score=sentiment_df.loc[index, 'compound']
        
        if score >= 0.05 : 
            score = "positive"
        elif score <= - 0.05 : 
            score = "negative"
        else: 
            score ="neutral"
        
        score_list.append(score)
        
    sentiment_df['score']=score_list
        
    return sentiment_df

def scored_news(tickers):
    finviz = 'https://finviz.com/quote.ashx?t='
    
    news_tables = {}
    
    for ticker in tickers:
        url = finviz + ticker
        req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
        response = urlopen(req)    
        html = BeautifulSoup(response, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
        
    parsed = []
    
    for name, table in news_tables.items():
        for i in table.findAll('tr'):
            a_text = i.a.get_text() 
            td_text = i.td.text.split()
    
            if len(td_text) == 1:
                time = td_text[0]
            else:
                date = td_text[0]
                time = td_text[1]
    
            parsed.append([name, date, time, a_text])
            
    vader = SentimentIntensityAnalyzer()
    cols = ['ticker', 'date', 'time', 'headline']

    scored_news = pd.DataFrame(parsed, columns=cols)
    scores = scored_news['headline'].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)

    scored_news = scored_news.join(scores_df, rsuffix='right')
    
    scored_news['date'] = pd.to_datetime(scored_news.date).dt.date
    
    return sentiment(scored_news)

def just_sentiment(tickers): 
    sentiment_df = scored_news(tickers)
    del sentiment_df['pos']
    del sentiment_df['neg']
    del sentiment_df['compound']
    del sentiment_df['neu']
    
    return sentiment_df

def date_range(df):
    date_ranges = {}
    n_tickers=int(len(df.index)/100)
    for i in range(n_tickers):
        if i==0: 
            recent_date = df.loc[i, 'date']
            furthest_date = df.loc[99, 'date']
            ticker=df.loc[i, 'ticker']
        else: 
            recent_date = df.loc[i*100, 'date']
            furthest_date = df.loc[i*100+99, 'date']
            ticker=df.loc[i*100, 'ticker']
        

        date_str = furthest_date.strftime("%b %d, %Y") + ' to ' + recent_date.strftime("%b %d, %Y")
        date_ranges[ticker]=date_str
        
    return date_ranges 

def tally_scores(df): 
    n_tickers=int(len(df.index)/100)
    tally ={}
    tickers=[]
    for i in range(n_tickers):
        if i==0: 
            ticker=df.loc[i, 'ticker']
        else: 
            ticker=df.loc[i*100, 'ticker']
        tickers.append(ticker)
    
    tally['tickers']=tickers
    tally['positive']=np.zeros([n_tickers])
    tally['neutral']=np.zeros([n_tickers])
    tally['negative']=np.zeros([n_tickers])
    tally_df = pd.DataFrame(tally)
    
    ticker_count = 0 
    for i in range(n_tickers*100):
        previous = tally_df.loc[ticker_count, df.loc[i, 'score']]
        tally_df.loc[ticker_count, df.loc[i, 'score']] = previous + 1
        
        if (i+1) % 100 == 0:
            ticker_count = ticker_count+1
            
    return tally_df

def daily_sentiment(df):
    mean_scores = df.groupby(['ticker','date']).mean()
    #optional
    mean_scores = mean_scores.unstack()
    return mean_scores

def plot_sentiment(df):
    # df=df.set_index('tickers').transpose()
    
    # for col in df.columns:
    #     print(col)
    #     plt.pie(
    #     df[col],
    #     labels= df.index.values,
    #     autopct='%1.1f%%',
    #     )

    #     plt.axis('equal')
    #     plt.show()



#List the tickers of the companies you'd like to analyze
tickers=['AMZN', 'GOOG', 'MSFT']              
plot_sentiment(tally_scores(scored_news(tickers)))
tally_scores(scored_news(tickers))

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()








