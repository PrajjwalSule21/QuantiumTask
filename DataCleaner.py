import pandas as pd
import requests
from io import StringIO
import warnings
warnings.filterwarnings("ignore")


def DataGetter(url):
    """
    This function is for fetching the data from the git location
    :param url: It will take the url, which contains the csv file
    :return: Pandas Dataframe
    """
    try:
        given_url = f"{url}?raw=true"  # adding ?raw=True so that we can get data from the GitHub link
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0"}
        req = requests.get(given_url, headers=headers)
        data = StringIO(req.text)

    except Exception as ex:
        print(ex)

    else:
        return pd.read_csv(data, error_bad_lines=False)


def ExtractOnlyPinkMorsel(DataSheet1, DataSheet2, DataSheet3):
    """
    This function is for making a dataframe which consists only Pink Morsel in the product section
    :param datasheet1: dataframe no.1
    :param datasheet2: dataframe no.2
    :param datasheet3: dataframe no.3
    :return: It will return the three independent DataFrames which consists only Pink Morsel.
    """
    try:
        # filtering the dataframes according to 'pink morsel'
        df1 = DataSheet1[DataSheet1['product']=='pink morsel']
        df2 = DataSheet2[DataSheet2['product']=='pink morsel']
        df3 = DataSheet3[DataSheet3['product'] == 'pink morsel']

    except Exception as ex:
        print(ex)

    else:
        return df1, df2, df3



def MakingSales(df1, df2, df3):
    """
    This function is responsible for converting the price and quantity into sales column
    :param df1: DataFrame no.1
    :param df2: DataFrame no.2
    :param df3: DataFrame no.3
    :return: It will return three independent DataFrames which consist the Sales column
    """
    try:
        df1['Sales'] = df1['quantity'] * 3
        df2['Sales'] = df2['quantity'] * 3

        # df1 and df2 only having one value in their price section/column
        # whereas df3 have two values such as $3 and $5

        #these are the temporary dataframes
        df_5 = df3[df3['price'] == '$5.00']
        df_3 = df3[df3['price'] == '$3.00']

        df_5['Sales'] = df_5['quantity'] * 5
        df_3['Sales'] = df_3['quantity'] * 3

        df3 = pd.concat([df_3, df_5])

    except Exception as ex:
        print(ex)

    else:
        return df1, df2, df3

def RemovingUnecessaryCols(df1, df2, df3):
    """
    This fucntion will remove product, price and quantity from the DataFrames
    :param df1: DataFrame no.1
    :param df2: DataFrame no.2
    :param df3: Dataframe no.3
    :return: It will return independent DataFrames which consists only data, region, sales
    """
    try:
        # dropping product, price and quantity from all the dataframes
        df1.drop(columns=['product', 'price', 'quantity'], inplace=True)
        df2.drop(columns=['product', 'price', 'quantity'], inplace=True)
        df3.drop(columns=['product', 'price', 'quantity'], inplace=True)

    except Exception as ex:
        print(ex)

    else:
        return df1, df2, df3


def FormatMatching(df1, df2, df3):
    """
    This function will Match the columns according to output file
    :param df1: DataFrame no.1
    :param df2: DataFrame no.2
    :param df3: DataFrame no.3
    :return: It will return independent DataFrames which matches the output file format.
    """
    try:
        df1 = df1[['Sales','date','region']]
        df1.rename(columns={'date':'Date','region':'Region'}, inplace=True)

        df2 = df2[['Sales', 'date', 'region']]
        df2.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)

        df3 = df3[['Sales', 'date', 'region']]
        df3.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)


    except Exception as ex:
        print(ex)

    else:
        return df1, df2, df3


def GettingOutputFile(df1, df2, df3, name):
    """
    This fucntion will merge all the dataframes into single output file
    :param df1: dataframe no.1
    :param df2: dataframe no.2
    :param df3: dataframe no.3
    :param name: name of output file
    :return: It will save all the dataframes into one output file as csv
    """
    # concat all the files
    try:
        temp_df = pd.concat([df1, df2])
        final_df = pd.concat([temp_df, df3])

    except Exception as ex:
        print(ex)

    else:
        final_df.to_csv(f"{name}.csv", index=False)


if __name__ == "__main__":
    # taking each page url
    url1 = "https://github.com/PrajjwalSule21/quantium-starter-repo/blob/main/data/daily_sales_data_0.csv"
    url2 = "https://github.com/PrajjwalSule21/quantium-starter-repo/blob/main/data/daily_sales_data_1.csv"
    url3 = "https://github.com/PrajjwalSule21/quantium-starter-repo/blob/main/data/daily_sales_data_2.csv"

    # getting the data from GitHub Repo into the each DataSheets
    DataSheet1 = DataGetter(url1)
    DataSheet2 = DataGetter(url2)
    DataSheet3 = DataGetter(url3)

    # Preprocess the DataSheets according to 'Pink Morsel'
    PM_df1, PM_df2, PM_df3 = ExtractOnlyPinkMorsel(DataSheet1, DataSheet2, DataSheet3)

    # Making Sales of day out of Price and Quantity
    Sales_df1, Sales_df2, Sales_df3 = MakingSales(PM_df1, PM_df2, PM_df3)

    # Removing Unecessary Cols
    Remo_df1, Remo_df2, Remo_df3 = RemovingUnecessaryCols(Sales_df1, Sales_df2, Sales_df3)

    # Format matching according to output file
    Dataframe1, Dataframe2, Dataframe3 = FormatMatching(Remo_df1, Remo_df2, Remo_df3)

    # Getting Desired output file
    GettingOutputFile(Dataframe1, Dataframe2, Dataframe3, 'output')













