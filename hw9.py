"""This is the final project. For this project, I will read in the Superstore data file from tableau and create a
cross shop report
1- read in and process a file
2- use a dictionary
3- use an if else statement

to run on mac:
python3 hw9.py
"""
#importing modules for pandas to read the input, as well as tabulae and csv to create my two outputs

import pandas as pd
import csv
from tabulate import tabulate

#function to read in the dataframe, this reads in the sample_superstore.csv table, which I downloaded from tableau
#https://community.tableau.com/docs/DOC-1236

def df_in():
    #read in the input file, sample_superstore.xlsx converteted to CSV via excel
    df = pd.read_csv('sample_superstore.csv')
    #cut this down to just the columns I am interested in State, Sales profit
    df2 = df[['State','Sales','Profit']]
    #rename the columns, probably unnecessary
    df2.columns = [['State','Sales','Profit']]
    #return the dataframe
    return df2

#df_in function reads n the dataframe
df_in = df_in()
#convert the data frame to a list
list_in = [df_in.columns.values.tolist()] + df_in.values.tolist()


#initialize values for sales and profit dictionaries
sales_dict = {}
profit_dict = {}
#x is the counter i will increment to read in the list_in list from above. Since the first row is headers, I will skip this
x = 1
while x < len(list_in):
    #I am going to split the list based on commas. Three fields, state, sales, and profit
    y = str(str(list_in[x]).strip()[1:-1])
    z = y.split(',')
    #first attribute in my new list is state
    state = str(z[0])
    #second attribute in my list is sales, since there is a dollar sign and possible commas, I will remove these
    sales1 = str.replace(z[1],'$','')
    sales_str = str.replace(sales1,"'",'')
    #try except to convert the sales and profit to integers. if it fails, we assume they are 0, get rid of garbage data
    try:
        sales = int(sales_str)
    except:
        sales = 0
    profit1 = str.replace(z[2],'$','')
    profit_str = str.replace(profit1,"'",'')
    try:
        profit = int(profit_str)
    except:
        profit = 0
    #calculate sales, if the state is already there, add it to the existing total, otherwise, create a new record
    if state in sales_dict.keys():
        old_sales = sales_dict.get(state)
        new_sales = old_sales + sales
        sales_append = {state: new_sales}
    else:
        sales_append = {state: sales}
    #calculate profit by state, if the state is already there, add it to the exiting total, otherwise, create a new record
    if state in profit_dict.keys():
        old_profit = profit_dict.get(state)
        new_profit = old_profit + profit
        profit_append = {state: new_profit}
    else:
        profit_append = {state: profit}
    #update the sales and profit dictionaries
    sales_dict.update(sales_append)
    profit_dict.update(profit_append)
    #increment the counter
    x = x + 1






#build a list of states from the sales dict
state_list= []
for key, value in sales_dict.items():
    temp = str(key)
    state_list.append(temp)

#build a tabulation list for us to pass into the final tabulate
tabulation=[]
x = 0
while x < len(sales_dict):
    #get state, sales, and profit out of the state_list, match to the sales_dict and profit_dict
    state_out = state_list[x]
    sales_out = str(sales_dict.get(state_out))
    profit_out = str(profit_dict.get(state_out))
    #calculate margin with a try-except. if error, calculate as 0
    try:
        margin = (float(profit_out) / float(sales_out)) * 100
    except:
        margin = 0
    #put the variables in the proper format for output
    margin_out = str('%{:.2f}'.format(margin))
    sales_fmt =  str('${:.2f}'.format(float(sales_out)))
    profit_fmt = str('${:.2f}'.format(float(profit_out)))
    #write out the variables to a variable, and append it to the tabulation list
    record_out = ([str(state_out[1:-1])]+ [sales_fmt]+ [profit_fmt] + [margin_out])
    tabulation.append(record_out)
    x = x + 1

#create the tabulate report using the tabulate function
print(tabulate(tabulation, headers=["State","Sales","Profit","Margin"], tablefmt="github"))
#write the records out to a csv for additioanl output
with open('hw9.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for item in tabulation:
       writer.writerow(item)