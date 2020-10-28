# -----------------------------------------------------------------------------     
# Purpose:  CS 122 Mini Project 2
#           Read NYC restaurant inspection data, find mean score and number
#           of unique restaurants per valid zipcode
#
# Author:   Michelle Lai
# Date:     March 2, 2018
# -----------------------------------------------------------------------------

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

def get_combined_zip_mean_size(df):
    """
    Creates a new data frame with the columns, 
    zip code, mean score, and number of resturants
    :param
    df (data frame) data frame with the correct zip codes
    :return: new data frame with the mean score and number 
    of resturants calculated for each zip code
    """
    # group resturants by their zip code
    group_zip = df.groupby('ZIPCODE')
    # find count/size and mean score of each of the zip codes
    group_size = group_zip.size()
    group_mean = group_zip.mean().SCORE

    # put the zip codes, count, and mean into lists
    list_zip = group_size.index.tolist()
    list_mean = group_mean.tolist()
    list_count = group_size.tolist()
    print("Groups for, zip codes: ", len(list_zip), ", mean: ", len(list_mean), ", count: ", len(list_count))

    # put the lists into one dictionary, then put into data frame
    combined = {'CODE': list_zip, 'MEAN': list_mean, 'SIZE': list_count}
    combined_df = pd.DataFrame(data=combined)
    return combined_df


# read csv file
df = pd.read_csv('data.txt', sep="\",\"", engine='python')

# fix naming of columns and data
df.rename(columns = {'"CAMIS':'CAMIS', 'RECORDDATE"':'RECORDDATE'}, inplace = True)  # remove quote on the first and last columns
df['CAMIS'] = df['CAMIS'].str.strip('"')  # remove quote on data of first column
df['RECORDDATE'] = df['RECORDDATE'].str.strip('"')  # remove quote on data of last column
#df.shape  # row, column (531935, 15)

# remove duplicate resturants
df = df.sort_values(by=['INSPDATE'], ascending=False)  # sort by most recent inspection date (highest to lowest date)
df = df.drop_duplicates(subset='CAMIS', keep='first')  # drop duplicate unique resturant identifiers, keep first or most recent entry
print("After removing duplicates: ", df.shape)  # (25232, 15)

# remove zip codes below the minimum, 10001
df_range = df[(df.ZIPCODE >= 10001)]
print("After removing zip codes below minimum: ", df_range.shape) # (25228, 15)

# get the data frame with columns for zipcode (NYC valid), mean score, number of resturants
combined_valid = get_combined_zip_mean_size(df_range)

# filter out zip codes where count < 100
combined_valid = combined_valid[combined_valid.SIZE > 100]
print("After filtering out groups with < 100 resturants: ", combined_valid.shape)
# sort by mean in descending order
combined_valid = combined_valid.sort_values(by=['MEAN'], ascending=False)
print("After removing all invalid resturants: ", sum(combined_valid.SIZE.tolist()))

# create list of tuples for each row in data frame
tuples_valid = [tuple(x) for x in combined_valid.values]
print(tuples_valid)
