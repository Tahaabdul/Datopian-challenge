import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents


def get_table():

    # get the response in the form of html
    wikiurl="https://en.wikipedia.org/wiki/Road_safety_in_Europe"
    table_class="wikitable sortable jquery-tablesorter"
    response=requests.get(wikiurl)
    print(response.status_code) # print the response code from intial get request (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    #finding table from the response with a class of required data table
    eurotable=soup.find('table',{'class':"wikitable sortable"})

    #read our html response from beautifulsoup object as a string/list
    df=pd.read_html(str(eurotable))
    # convert list to dataframe
    df=pd.DataFrame(df[0])

    #intializing a variable Year with constant value as the length of data columns
    Year = pd.Series(["2018" for x in range(len(df.index-1))], index=df.index-1)

    #Drop all unwanted columns by index for (Road Network Length, Number of People Killed per Billion, Number of Seriously Injured)
    df.drop(df.columns[[6, 9, 10]], axis = 1, inplace = True)

    #Renaming all columns as their expected in final output
    df = df.set_axis(["Country", "Area", "Population", "GDP per capita", "Population density", "Vehicle ownership", "Total road deaths", "Road deaths per Million Inhabitants"], axis=1)

    #Inserting a column "Year" with a constant value of "2018"
    df.insert(loc=1, column='Year', value=Year)

    #sorting the data by the death per million inhabitant column excluding the row with total Europe values
    sorted_table = df[0:27].sort_values('Road deaths per Million Inhabitants')

    #appending the row with total Europe values
    df = sorted_table.append(df.loc[28]) 

    #setting our index/first data column to Country 
    df = df.set_index('Country')

    #exporting data as csv into an existing path "datopian-challenge/output-data/"
    df.to_csv("datopian-challenge/output-data/europe-rdsafety.csv", sep=',')
    
    df = df.iloc[0:27]

     #plotting graphs of Road deaths per Million Inhabitants",Vehicle ownership" and Total road deaths for all countries )
    df.plot( y="Road deaths per Million Inhabitants", kind="bar")
    df.plot( y="Vehicle ownership", kind="bar")
    df.plot( y="Total road deaths", kind="bar")
    
    return df

get_table()





