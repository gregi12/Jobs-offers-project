# My previuos solution wasn't so good and I took new approach 
import pandas as pd
import numpy as np
df = pd.read_csv('analiza-ofert-final.csv')
df.info()
df.head()

#So firstly I'm deleting columns that won't be usefull
df = df.drop(['related_links','job_id','thumbnail','posted_at'],axis=1)


# In extenions columns there are some valuable informations so I'll try get them in clean form.
import re
clean_text = []
for info in df['extensions']:
    try:
        sampleStr = info
        marker1 = "'"
        marker2 = "'"
        regexPattern = marker1 + '(.+?)' + marker2
        str_found = re.findall(regexPattern, sampleStr)
        clean_text.append(str_found[1:])
        
    except AttributeError:
        str_found = 'Nothing found between two markers'
        
flat_list = [item for sublist in clean_text for item in sublist]
new_dict = (dict((x,flat_list.count(x)) for x in set(flat_list)))

# And sort them to check which are most common ones.
import operator
sorted_d = dict(sorted(new_dict.items(), key=operator.itemgetter(1),reverse=True))


# Eventually ,after quite some time I came up with this.
import re
salary_dict = {}
def look_up(pattern):
    hook = 0
    for lista in df['extensions']:
        
            try:
                sample = ''.join(lista)
                print(sample)
                salary = re.search(pattern,sample)
                salary_dict[hook]= salary.group()
            except:
                hook+=1
                print('Not match',hook)
            else:
                hook += 1


# Variable hook is always the same number as row 
# indexes from dataframe so keys from dictionary are dataframe indexes in the same time


look_up(r'\d+K–\d+K')
look_up(r'\W\d+–\W\d+K')
look_up(r'\W\d+K–\W\d+K')
look_up(r'US\W\d+–US\W\d+')
look_up(r'\W\d\d–\W\d\d')
look_up(r'\d\d.\d\d–\d\d.\d\d')
look_up(r'\d+–\d+\san\shour|\d+–\d+\sa\syear')

#I made list of keys and added to dataframe all salaries that I found 
list_of_keys = list(salary_dict.keys())

for key in list_of_keys:
    try:
        df['salary'][key]=salary_dict[key]
    except:
        print('error')
        continue
        
# Cleaning info about sites 
hook = 0
for string in df['via']:
    try:
        word = string[4:]
        df['via'][hook]= word
    except:
        hook+=1
        print('Not match',hook)
    else:
        hook+=1
        
# More cleaning, deleting duplicated offers


df.drop('date_time',axis=1,inplace=True)
df[df.duplicated(subset=['description','via','company_name','location','extensions'])].shape
no_dup_columns = df.drop_duplicates(subset=['description','via','company_name','location','extensions'])

df = no_dup_columns

# adding some key words to do resarch in description 
key_words = ['developing reports','do reports','sql','database','data managment','junior','gcp',
             'college degree','degree','computer Engineering','reports','expert level']

# diffrent languages,libraries etc.
diffrent_tools = ['tableau','power Bi','powerBI','sql','mySql','pandas','numPy','matplotlib',
                  'seaborn','linux','windows','gcloud','azure','excel','tensorflow','keras',
                  'git','SSRS','SSIS','ETL','Snowflake','UNIX','SSMS','PowerBI','Visual Studio','SharePoint','JIRA','python']

# diffrent skills requirments
diffrent_skills = ['data mining','data Mining','application Design','application design',
                  'business Intelligence','business intelligence','information management',
                   'information Managment','excellent communication','interpersonal skills',
                   'maintain data sets','data base development','maintain databases','Extracting data',
                   'data warehouse','agile','scrum','AGILE','SCRUM','Excellent verbal and written']






key_words.extend(diffrent_tools)
key_words.extend(diffrent_skills)
megalist = []
for word in key_words:
    yol = word.lower()
    megalist.append(yol)
    yol = word.upper()
    megalist.append(yol)
    yol = word.capitalize()
    megalist.append(yol)

megalist.append('NumPy')
megalist.append('SeaBorn')
megalist.append('scikit-learn')
megalist.append(' R ')
megalist.append(' r ')

#So here I'm manipluating data a bit to get all of the unique words in megalist 
x = set(megalist)
megalist = list(x)
megalist.sort()


# And now I looking for all the words from megalist in descriptions
kolejna = []
for desc in df['description']:
    try:
        for phrase in megalist:
            try:
                slowo = re.search(phrase,desc)
                slowo = slowo.group()
                kolejna.append(slowo)
            except:
                continue
    except:
        continue

# 
len(kolejna)
set_kolejna = set(kolejna)
lista_slow = list(set_kolejna)
lista_slow.sort()




#So I made dictionary where all keywords have number of appearances attached to them and sorted 
ostateczny_slownik = (dict((x,kolejna.count(x)) for x in set(kolejna)))

sorted_ostateczny = dict(sorted(ostateczny_slownik.items(), key=operator.itemgetter(1),reverse=True))


# Here I made list of of list with first element being keyword and second being number of appearances

lista_laczna = list([key,value] for key,value in ostateczny_slownik.items())

#Thanks to that I could sum all words regardless of size of  letters

word_count = {}

for sublist in lista_laczna:
    word = sublist[0].lower()
    count = sublist[1]
    
    if word in word_count:
        word_count[word] += count
    else:
        word_count[word] = count
        
# That's all my keywords with their values
        
slownik = dict(sorted(word_count.items(), key=operator.itemgetter(1),reverse=True ))

#database wasn't bestfor analyze cause everywhere 'sql' was there probably was this word also
slownik.pop('database')

# I deleted results with less than 7 apperances and added more sense to my results
def delete_keys(d, limit):
    keys_to_delete = [key for key in d if d[key] < limit]
    for key in keys_to_delete:
        del d[key]
    return d

f = delete_keys(slownik,7)

f['excellent communication'] =54
f.pop('excellent verbal and written')
f.pop('expert level')
df[df['location']=='Anywhere']


df['work_from_home'] = df['work_from_home'].fillna(False)
df.dropna()

#And at the end I made a few plots of this
import seaborn as sns 
import matplotlib.pyplot as plt
some_df = pd.DataFrame(f,index=[word for word in ['keywords']],columns=[word for word in f.keys()])


df_keywords = pd.DataFrame({'keywords':[value for value in slownik.values()]},index=slownik.keys())

# All keywords compared
fig = plt.figure(figsize=(14,6))
axes = fig.add_axes([0,0,1,1])

plt.xticks(rotation=90)
plt.rc('xtick', labelsize=20) 
fontsize =15
plt.title('KEYWORDS \n\nIN DATA ANALYST OFFERS',fontdict={'fontsize': fontsize})
bar = axes.bar(slownik.keys(),df_keywords['keywords'],edgecolor='black')
bar[0].set_color('brown')
bar[1].set_color('r')
bar[2].set_color('g')
bar[3].set_color('yellow')
bar[4].set_color('grey')
bar[5].set_color('grey')
bar[6].set_color('grey')
plt.show()
# Top seven requirements
fig = plt.figure(figsize=(14,6))
axes = fig.add_axes([0,0,1,1])
plt.xticks(rotation=90)
plt.rc('xtick', labelsize=20) 
fontsize =12
plt.title('MOST_WANTED',fontdict={'fontsize': fontsize})
bar = axes.bar(x=['Excel','Degree','SQL','Making reports','SSIS','Tableau','Python'],
               height = [416,340,328,298,224,153,147],color=['brown','red','grey','blue','blue','black','black'])
plt.show()
# Countplot stationary offers with work_from_home
sns.countplot(df['work_from_home'])
plt.show()
#I got 2 full-time sections so I manually summed them up
df['schedule_type'].value_counts()

sns.set_style("whitegrid")
sch_type = sns.barplot(x=['Full-time','Contractor','Part-time','Internship'],y=[467,78,3,2])
sch_type.set(xlabel='schedule-type')
plt.xticks(rotation=90)
plt.show()