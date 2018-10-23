# Futures-Pairs-Trading
## How to use getData?
### step 1 (# import data)
load data : replace '艾佳-目标产品名单.xlsx' by your own file name, default format is with header

### step 2 (# define target trading time in "openTime")
set your target trading time points : in this example, the selected trading points are 09:00, 10:30, 13:30, 21:00

### step 3 (# domestic and foreign trading time)
input the colume indexs for domestic trading and foreign trading from your excel file

### step 4 (# define new headers)
set your new colume names for target trading times

### step 5 (# write back to file)
set your new file name

## How getData works?
By loading previous data of both domestic and foreign trading periods, the main object of this code is to add new columes (the available pairs trading times) to the origin excel file based on the following conditions.

-1- All products have 0~4 possible times for pairs trading strategy and we need to decide which ones work
-2- Those possible times in our example are 09:00, 10:30, 13:30, 21:00 because these are the most popular open time for domestic futures market
-3- For each product, we need to guarantee that (1) when the domestic market is open, foreign market is also open (which means if the foreign market is not trading, then we are not able to get new information and thus unable to make a strategy); (2) the open time for domestic market should be one of the four possible times

So the idea behind this algorithm, is presented as follows:
With the help of "datetime" in Python, we firtst convert all the data formats in the origin excel to a new format.
Then, for each product (each line), we have a two-layer loops.
For each product, is there a open time that belongs in the list of the 4 possible selections. If so, is that time point also available for trading in the foreign market? If so, we take a record and output that time point.

After processing line by line, we will get the final result of all the available time points in the new excel file.
