import pandas as pd
import numpy as np


df = pd.read_csv('analiza-ofert-final.csv')
df.info()

#So firstly I'm deleting columns that won't be usefull
df = df.drop(['related_links','job_id','thumbnail','posted_at'],axis=1)




# In 'extenions' column there are some valuable informations so I'll try get them in clean form.
features = []
for info in df['extensions']:
    arr = info.split(',')
    features.append(arr[1:])
    
import re
clean_words = []
for text in features:
    for feature in text:
        try:
            sampleStr = feature
            # here ' and ' are our two markers 
            # in which string can be found. 
            marker1 = "'"
            marker2 = "'"
            regexPattern = marker1 + '(.+?)' + marker2
            str_found = re.search(regexPattern, sampleStr).group(1)
            clean_words.append(str_found)
            
        except AttributeError:
            # Attribute error is expected if string 
            # is not found between given markers
            str_found = 'Nothing found between two markers'

# Now let's check how many unique values are there 
new_dict = (dict((x,clean_words.count(x)) for x in set(clean_words)))
new_dict

# And sort them to check which are most common ones.
import operator
sorted_d = dict(sorted(new_dict.items(), key=operator.itemgetter(1),reverse=True))


sorted_d

# So here we see that most of jobs are full time, in 1/3 of them no degree is mentioned ,  
# in about 1/4 we have some medical insurance and about 20% of it is WORK_FROM_HOME

#I'll try to plot this

# for now I've chosen just 7 from the top because they are like 93% of data 
# and rest are mostly information about salary so I'm gonna use it later

# data from extenions column cover with data from schedule type, one problem which I don't understand is
# why there came 2 'Full-time' sections from my previous operation although they are spelled exactly the same

# for the moment I decided to not include this 54 "Full-time" units

main_dict = {'Full-time': 459,
 'No_degree_mentioned': 190,
 'Health_insurance': 157,
 'Dental_insurance': 130,
 'Work_from_home': 126,
 'Paid_time_off': 122,
 'Contractor': 83}

df1 = pd.DataFrame([main_dict])
#My first try to visualize wasn't much a succes
import seaborn as sns
import matplotlib.pyplot as plt

df1.plot('bar')
sns.barplot(df1,x=df1.columns,y=df1.values)

# I tried to plot this but it didnt work out in this format so I changed it to form below

df1 = pd.DataFrame([["All-offers",609],['Full-time',459],['No_degree_mentioned',190]
                    ,['Health_insurance',157],['Denatal_insurance',130],['Work_from_home',126],
                    ['Paid_time_off',122],['Contractor',83],['Internship',4]], columns=['features','values'])

# Here we can catch some info about benefits etc.
plt.figure(figsize=(15,6))
sns.barplot(data =df1 ,x=df1['features'],y=df1['values'])

#Let's explore data a bit

for text in df['job_highlights'][100:115]:
    print('\n\n',text, '\n\n\n\n\n\n\n\n')

#Now let's create some key_words lists

# adding some key words to do resarch in description and job highlights
key_words = ['developing reports','do reports','sql','database','data managment',
             'college degree','degree','computer Engineering','reports','expert level']

for word in range(15):
    key_words.append('+{} years'.format(hook))
    hook+=1

# diffrent languages,libraries etc.
diffrent_tools = ['tableu','power Bi','powerBI','sql','mySql','pandas','numPy','matplotlib',
                  'seaborn','linux','windows','gcloud','azure','excel','tensorflow','keras',
                  'git','SSRS','SSIS','ETL','Snowflake','UNIX','SSMS','PowerBI','Visual Studio','SharePoint','JIRA','python','R']

# diffrent skills requirments
diffrent_skills = ['data mining','data Mining','application Design','application design',
                  'business Intelligence','business intelligence','information management',
                   'information Managment','excellent communication','interpersonal skills',
                   'maintain data sets','data base development','maintain databases','Extracting data',
                   'data warehouse','agile','scrum','AGILE','SCRUM','Excellent verbal and written'
                   ]

hook = 0

# so I looked into the data a bit and decied to get informations about salary as I planned before
features[7]
type(features[0])
''.join(features[0])
features[228]

# Eventually ,after quite some time I came up with this.
import re
salary_dict = {}
def look_up(pattern):
    hook = 0
    for text in features:
        try:
            sample = ''.join(text)
            salary = re.search(pattern,sample)
            print(salary)
            salary_dict[hook]= salary.group()
        except:
            hook+=1
            print('Not match',hook)
        else:
            hook += 1


# Variable hook is always the same number as indexes from dataframe 
# so keys from dictonary are also indexes in dataframe


#I manually added some strange results and then I them from my dictionary

look_up(r'\d+–\d+\san\shour')
look_up(r'\d+K–\d+K')
look_up(r'\W\d+–\W\d+K')
look_up(r'\W\d+K–\W\d+K')
look_up(r'US\W\d+–US\W\d+')

for key in [356,392,395,401,412,426,434,437,446,448]:
    salary_dict.pop(key)
    
#And now I'm stacked a bit 
for salary in df['salary']:
    hook=0
    if salary==NaN:
        try:
            salary = salary_dict
        except:
            hook+=1
            print('nana')
        else:
            hook+=1
            continue

#Unfortunetly I can't add values from my dict into dataframe

for hook in range(10):
    x= df['salary'][hook]
    print(type(x))
    print(hook)
    if type(x)==float:
        try:
            x= df['salary'][hook]
            df['salary'][hook] == salary_dict[hook]
        except:
            print('Lipa')
            continue
            

