# stock-sentiment-analyzer
The *Stock Sentiment Analyzer* scrapes the 100 most recent article headlines for inputted stock tickers from Finviz.com and uses natural language processing to evaluate the sentiment of the headlines.

The natural language processing is performed using *nltk*’s *Vader* module. Each headline is analyzed for its sentiment and assigned a normalized score from -1 to 1 where -1 is the most extreme negative and 1 is the most extreme positive. Values greater than 0.05 were considered positive and values less than -0.05 were considered negative. Values in between were considered neutral headlines. 

The results are outputted to a 

The following libraries were used:
* *urllib* to scrape the data from the finviz website
* *BeautifulSoup* to extract the headlines and dates from the scaped data 
* *nltk* to analyze the sentiment of each headline
* *numpy* to work with date values
* *pandas* to manipulate the tabular data
