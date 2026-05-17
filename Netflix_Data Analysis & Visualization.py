#!/usr/bin/env python
# coding: utf-8

# ### import lib

# In[3]:


### Import lib

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt



# ### load dataset

# In[10]:


###load dataset

df = pd.read_csv("Self Project/Netflix Dataset.csv")

### show first five rows

df.head()


# ### Dataset info

# In[85]:


#number of rows and column
print("shape of dataset:", df.shape)

#column name
print("\nColumns:\n", df.columns)

#basic info
df.info()


# ### check missing values
# 
# 
# 

# In[27]:


#missing values in each column
df.isnull().sum()


# ### Remove duplicate

# In[35]:


# check duplicate
print("Duplicate rows:", df.duplicated().sum())


# In[39]:


# remove duplicate
df.drop_duplicates(inplace=True)
print("Duplicate remove successfully")


# ### convert realese date into datetime

# In[42]:


# remove extra space

df['Release_Date'] = df['Release_Date'].str.strip()


# In[83]:


# convert to datetime

df['Release_Date'] = pd.to_datetime(
    df['Release_Date'],
    format='%B %d, %Y',
    errors='coerce'
)

# Check datatype
df['Release_Date'].head()


# ### create a new columns year and months

# In[51]:


# Extract year
df['Year_Added'] = df['Release_Date'].dt.year

# Extract month name
df['Month_Added'] = df['Release_Date'].dt.month_name()

df[['Release_Date', 'Year_Added', 'Month_Added']].head()


# ###  Handle missing values

# In[87]:


# Fill missing values
df['Director'].fillna('Unknown', inplace=True)
df['Cast'].fillna('Unknown', inplace=True)
df['Country'].fillna('Unknown', inplace=True)

# Fill missing ratings with mode
df['Rating'].fillna(df['Rating'].mode()[0], inplace=True)

print("Missing Values Handled")


# ### set visualization

# In[57]:


sns.set(style="whitegrid")


# ### Movies and TV shows

# In[60]:


plt.figure(figsize=(6,6))

df['Category'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    colors=['red', 'gray'],
    explode=[0, 0.1]
)

plt.title("Movies vs TV Shows")
plt.ylabel('')
plt.show()


# ### Content growth by year

# In[63]:


content_over_time = df.groupby(
    ['Year_Added', 'Category']
).size().unstack().fillna(0)

content_over_time.plot(
    kind='line',
    figsize=(10,6),
    marker='o'
)

plt.title("Netflix Content Growth")
plt.xlabel("Year")
plt.ylabel("Count")
plt.show()


# ### Top 10 Content Producing Countries

# In[66]:


top_countries = df[df['Country'] != 'Unknown']['Country'] \
    .str.split(', ') \
    .explode() \
    .value_counts() \
    .head(10)

plt.figure(figsize=(10,6))

sns.barplot(
    x=top_countries.values,
    y=top_countries.index,
    palette='Reds_r'
)

plt.title("Top 10 Countries")
plt.xlabel("Number of Shows")
plt.ylabel("Country")
plt.show()


# ### Content Rating Distribution

# In[69]:


plt.figure(figsize=(12,6))

sns.countplot(
    data=df,
    x='Rating',
    order=df['Rating'].value_counts().index,
    palette='viridis'
)

plt.title("Content Rating Distribution")
plt.xticks(rotation=45)
plt.show()


# ### Top 15 Genres

# In[72]:


genres = df['Type'] \
    .str.split(', ') \
    .explode() \
    .value_counts() \
    .head(15)

plt.figure(figsize=(12,6))

sns.barplot(
    x=genres.values,
    y=genres.index,
    palette='magma'
)

plt.title("Top 15 Genres")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.show()


# ### Monthly Content Addition Trend

# In[75]:


month_order = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

plt.figure(figsize=(12,6))

sns.countplot(
    data=df,
    x='Month_Added',
    order=month_order,
    palette='rocket'
)

plt.title("Monthly Content Addition")
plt.xticks(rotation=45)
plt.show()


# ### Business Insights

# In[78]:


total_titles = len(df)

movie_perc = (
    len(df[df['Category'] == 'Movie']) / total_titles
) * 100

tv_perc = (
    len(df[df['Category'] == 'TV Show']) / total_titles
) * 100

print("----- Business Insights -----")

print(f"Movies Percentage: {movie_perc:.1f}%")
print(f"TV Shows Percentage: {tv_perc:.1f}%")

print("\nKey Insights:")
print("1. Netflix contains more Movies than TV Shows.")
print("2. USA is the largest content producer.")
print("3. TV-MA and TV-14 are the most common ratings.")
print("4. Netflix content growth increased rapidly after 2016.")


# ### Save Cleaned Dataset

# In[81]:


df.to_csv("Cleaned_Netflix_Dataset.csv", index=False)

print("Cleaned Dataset Saved Successfully")


# In[ ]:




