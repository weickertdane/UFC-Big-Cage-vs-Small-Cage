from turtle import color
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup 

#csv edits inb Excel
# - dropped multiple columns 
# - converted (rounds, minutes, seconds) to 'Duration' (seconds)
 

#turn csv into dataframe
    
# making dataframe 
df = pd.read_csv("ufc_fight_results as of 9-2.csv") 
   
#Filtering 

df_filtered_3 = df[df['fight_duration'] <= 900] # create df for 3 round fights only
df_filtered_title = df_filtered_3[~df_filtered_3['weight_class'].str.contains('Title', na=False)]  #filter by does not contain 'Title'

df_filtered_catch = df_filtered_title[~df_filtered_title['weight_class'].str.contains('Catch', na=False)]  #filter by does not contain 'Catch'

df_clean = df_filtered_catch # contains all small and big cage fights since may 9th, 2020. only 5 round fights in data set are non-title main events that ended before the conclusion of round 3 (very small number, possibly zero)

count = (df_clean.value_counts('weight_class'))  # counts number of fights per weight class


#get average with two conditions
avg_if = df_clean.query('weight_class == "Middleweight Bout" & big_or_small == "big"')['fight_duration'].mean()
#print(avg_if)

#create data frame for results (data to be graphed)
#Getting Average Fight Duration by Weight Class and Cage Size

#classes = ['Flyweight Bout', 'Bantamweight Bout', 'Featherweight Bout', 'Lightweight Bout', 'Welterweight Bout', 'Middleweight Bout', 'Light Heavyweight Bout', 'Heavyweight Bout', "Women's Strawweight Bout", "Women's Flyweight Bout", "Women's Bantamweight Bout", "Women's Featherweight Bout"]
classes_no_w = ['Flyweight Bout', 'Bantamweight Bout', 'Featherweight Bout', 'Lightweight Bout', 'Welterweight Bout', 'Middleweight Bout', 'Light Heavyweight Bout', 'Heavyweight Bout'] 

res_df = pd.DataFrame(classes_no_w, columns =['weight_class'])
res_df['big_cage_avg'] = ''
res_df['small_cage_avg'] = ''

b = 'big_cage_avg'
sm = 'small_cage_avg'


#for big cag
res_df.at[0,b] = df_clean.query('weight_class == "Flyweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[1,b] = df_clean.query('weight_class == "Bantamweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[2,b] = df_clean.query('weight_class == "Featherweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[3,b] = df_clean.query('weight_class == "Lightweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[4,b] = df_clean.query('weight_class == "Welterweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[5,b] = df_clean.query('weight_class == "Middleweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[6,b] = df_clean.query('weight_class == "Light Heavyweight Bout" & big_or_small == "big"')['fight_duration'].mean()
res_df.at[7,b] = df_clean.query('weight_class == "Heavyweight Bout" & big_or_small == "big"')['fight_duration'].mean()

#unresolved  issue with apostrophes in Women's weight_class
#res_df.at[8,b] = df_clean.query("weight_class == 'Women's Strawweight Bout' & big_or_small == 'big'")['fight_duration'].mean()
#res_df.at[9,b] = df_clean.query("weight_class == 'Women's Flyweight Bout' & big_or_small == 'big'")['fight_duration'].mean()
#res_df.at[10,b] = df_clean.query("weight_class == 'Women's Bantamweight Bout' & big_or_small == 'big'")['fight_duration'].mean()
#res_df.at[11,b] = df_clean.query("weight_class == 'Women's Featherweight Bout' & big_or_small == 'big'")['fight_duration'].mean()

#for small cage

res_df.at[0,sm] = df_clean.query('weight_class == "Flyweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[1,sm] = df_clean.query('weight_class == "Bantamweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[2,sm] = df_clean.query('weight_class == "Featherweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[3,sm] = df_clean.query('weight_class == "Lightweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[4,sm] = df_clean.query('weight_class == "Welterweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[5,sm] = df_clean.query('weight_class == "Middleweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[6,sm] = df_clean.query('weight_class == "Light Heavyweight Bout" & big_or_small == "small"')['fight_duration'].mean()
res_df.at[7,sm] = df_clean.query('weight_class == "Heavyweight Bout" & big_or_small == "small"')['fight_duration'].mean()

#unresolved  issue with apostrophes in Women's weight_class
#res_df.at[8,sm] = df_clean.query("weight_class == 'Women's Strawweight Bout' & big_or_small == 'small'")['fight_duration'].mean()
#res_df.at[9,sm] = df_clean.query("weight_class == 'Women's Flyweight Bout' & big_or_small == 'small'")['fight_duration'].mean()
#res_df.at[10,sm] = df_clean.query("weight_class == 'Women's Bantamweight Bout' & big_or_small == 'small'")['fight_duration'].mean()
#res_df.at[11,sm] = df_clean.query("weight_class == 'Women's Featherweight Bout' & big_or_small == 'small'")['fight_duration'].mean()


#get difference in seconds between small cage and big cage

res_df['seconds_change'] = res_df['small_cage_avg'] - res_df['big_cage_avg'] # add seconds_change column
res_df['percent_change'] = res_df['seconds_change'] / res_df['big_cage_avg'] #add percent_change column 

#get number of bouts in dataset by weight class
nb = 'number_of_bouts'
res_df.at[0,nb] = df_clean.query('weight_class == "Flyweight Bout"')['weight_class'].count()
res_df.at[1,nb] = df_clean.query('weight_class == "Bantamweight Bout"')['weight_class'].count()
res_df.at[2,nb] = df_clean.query('weight_class == "Featherweight Bout"')['weight_class'].count()
res_df.at[3,nb] = df_clean.query('weight_class == "Lightweight Bout"')['weight_class'].count()
res_df.at[4,nb] = df_clean.query('weight_class == "Welterweight Bout"')['weight_class'].count()
res_df.at[5,nb] = df_clean.query('weight_class == "Middleweight Bout"')['weight_class'].count()
res_df.at[6,nb] = df_clean.query('weight_class == "Light Heavyweight Bout"')['weight_class'].count()
res_df.at[7,nb] = df_clean.query('weight_class == "Heavyweight Bout"')['weight_class'].count()


# res_df now contains correct data for graphing 

#generate bar chart with % changes like Excel (practice)
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick


weight_classes = ['FlyW', 'BW', 'FW', 'LW', 'WW', 'MW', 'LHW', 'HW']
y_pos = np.arange(len(weight_classes))
p_c = res_df['percent_change']*100

plt.bar(y_pos, p_c, align='center', alpha=0.5)
plt.xticks(y_pos, weight_classes)
plt.ylabel('percent_change as %')
plt.title('Fight Duration Change For Small Cage vs Big Cage')
#plt.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=None, symbol='%', is_latex=False))

plt.show()
