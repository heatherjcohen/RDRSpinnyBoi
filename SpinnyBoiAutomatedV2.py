
# coding: utf-8

# In[11]:


import pandas as pd 
from datetime import datetime
#from __future__ import with_statement                                                            
import contextlib 
try: 
    from urllib.parse import urlencode           
except ImportError: 
    from urllib import urlencode 
try: 
    from urllib.request import urlopen 
except ImportError: 
    from urllib2 import urlopen  
import sys 

import random 
import tweepy
import json
import numpy as np
import os 
import os.path
from os import path
#I am the RDR Spinny Boi
#First, import all the libraries


# In[1]:


#ACCESS_TOKEN_SECRET


# In[13]:


get_ipython().magic('store -r CONSUMER_KEY')
get_ipython().magic('store -r CONSUMER_SECRET')
get_ipython().magic('store -r ACCESS_TOKEN')
get_ipython().magic('store -r ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)



# In[14]:


#Get the data set

def get_recommendations(url, columns):
    df = pd.read_csv(url, header=None, names=columns)
#add tiny links
    def make_tiny(urllist):
        tinycolumn = []
        for url in urllist:
            tinycolumn.append(tiny(url))
        df['Tiny']= tinycolumn
  
    def tiny(url): 
        request_url = ('http://tinyurl.com/api-create.php?' + urlencode({'url':url}))     
        with contextlib.closing(urlopen(request_url)) as response:                       
            return response.read().decode('utf-8 ')                                       


    make_tiny(df['Link'])
    #print(df.head())
    #Spin the wheel
    return df


    
spinnydf =get_recommendations("https://docs.google.com/spreadsheets/d/e/2PACX-1vTWc2VxHamAlR4RQK2GiDg6eVGiWa-azbIssCeSwxMnOOuqv200oZoIgxF4LWcAWHOAVBugXLUbQx9E/pub?output=csv", ['Title', 'Genre', 'Genre Number', 'Link'])


# In[15]:


#get last x mentions
#def get_mentions(x):
#result_list = api.mentions_timeline(count=x)
#status = result_list[0]
# json_str = json.dumps(status._json)
#  json =json.loads(json_str)
#   twitteruser = json['user']['screen_name']
#    twitteruser


# In[16]:


Tweets = pd.DataFrame()
Tweets


# In[41]:




def get_mentions(x):
    df =  pd.DataFrame(columns=['Tweet ID', 'User', 'Created At', 'Text'])
    result_list = api.mentions_timeline(count=x)
    for i in range(len(result_list)):
        status = result_list[i]
        #print(i)
    #print(status)
        json_str = json.dumps(status._json)
        text =json.loads(json_str)
    #print(text)
        twitteruser = text['user']['screen_name']
        tweetid = text['id']
        tweettime = text['created_at']
        tweettext = text['text']
        ##add in stuff to detect what tweet says here
        #don't print, make a dataframe indexed on tweet id 
        #print(twitteruser, tweetid, tweettime, tweettext)
        data = {'Tweet ID':tweetid, 'User': twitteruser, 'Created At':tweettime, 'Text':tweettext}
        df = df.append(data, ignore_index=True)
        
    return df

#now = get_mentions(10)
#now


# In[18]:



#Tweets = pd.DataFrame()
#now = get_mentions(10)
#history =pd.read_csv('history.csv')
#new = np.setdiff1d(now['Tweet ID'],history['Tweet ID'])
#not_replied_to2 = now[now['Tweet ID'].isin(new)]  


# In[19]:




def spinthewheel(df, not_replied_to):
   winners = pd.DataFrame( columns = ['Title', 'Genre']) 
   if len(not_replied_to) > 0:
       for thing in range(len(not_replied_to)):
           spin = random.randint(1,12)
           spin2 = random.randint(0,(len(df[df['Genre Number']==spin])-1))
           #print(spin, spin2)
           winner = df[df['Genre Number']==spin].iloc[spin2]
           winner['Title'] = winner['Title'].title()
           winner['Genre'] =winner['Genre'].title()
           winners = winners.append(winner,ignore_index=True)
   #print(winner)
   #print("-------------")
   #print("You got " + winnerGenre)
   #print("Why not try "+ winnerTitle)
   #print("Found at: "+ winnerTiny )

   return winners
   

   

#Win = spinthewheel(spinnydf, not_replied_to2)
#print(Win)


# In[20]:


#for thing in range(len(not_replied_to)):
  #  which_answer = random.randint(0,3)
    #a = '@%s You got %s. Why not try out %s? They can be found at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
    #b = '@%s What a stroke of luck! You got %s. That’s incredible. I cannot believe it. Wait. Wait there’s more!! It’s %s at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
    #c = '@%s The Spirit of Radio has granted you… %s! And the show you should try is %s at coordinates: %s '% (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
    #d = '@%s the Fates have revealed your genre shall be %s and take the form of %s whose digital form can be found at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
    #answers = [a,b,c,d]
    #print(thing)
    #print(answers[which_answer])

      


# In[ ]:


recon = ['recommend', 'recommendation']
thnxbb = ['thanks', 'thank you', 'thxs', 'thx']
        if any(x in tweettext.lower() for x in recon):

            data = {'Tweet ID':tweetid, 'User': twitteruser, 'Created At':tweettime, 'Text':tweettext}
            recommend = recommend.append(data, ignore_index=True)
        elif any(x in tweettext.lower() for x in thnxbb):
            data = {'Tweet ID':tweetid, 'User': twitteruser, 'Created At':tweettime, 'Text':tweettext}
            thank = thank.append(data, ignore_index=True)
        else:
            data = {'Tweet ID':tweetid, 'User': twitteruser, 'Created At':tweettime, 'Text':tweettext}
            etc = etc.append(data, ignore_index=True)
  
    return recommend, thank, etc


# In[21]:


#### update to take the three data frames, recommend, thanks, and etc and respond to each differently

#### test with alex 





def reply_and_update(Win, history, now, new, not_replied_to):
    if len(not_replied_to) > 0:
        for thing in range(len(not_replied_to)):
            #update to have options and pick a random way to respond
            print("I am responding to "+ str(thing+1)+" tweet of " +str(len(not_replied_to)) + " tweets")
            ##add in different answer logic here
            recon = ['recommend', 'recommendation']
            thnxbb = ['thanks', 'thank you', 'thxs', 'thx']
            if any(x in not_replied_to['Text'][thing].lower() for x in recon): 
                which_answer = random.randint(0,3)
                a = '@%s You got %s. Why not try out %s? They can be found at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
                b = '@%s What a stroke of luck! You got %s. That’s incredible. I cannot believe it. Wait. Wait there’s more!! It’s %s at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
                c = '@%s The Spirit of Radio has granted you… %s! And the show you should try is %s at coordinates: %s '% (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
                d = '@%s the Fates have revealed your genre shall be %s and take the form of %s whose digital form can be found at %s ' % (not_replied_to['User'][thing],Win.iloc[thing]['Genre'],Win.iloc[thing]['Title'],Win.iloc[thing]['Tiny'])
                answers = [a,b,c,d]
                api.update_status(answers[which_answer])
            #api.update_status("@"+not_replied_to['User'][thing]+" You got " + Win.iloc[thing]['Genre'] +". Why not try out "+ Win.iloc[thing]['Title']+ "? They can be found at: " + Win.iloc[thing]['Tiny'], not_replied_to['Tweet ID'][thing])
                history = history.append(not_replied_to, ignore_index=True)
                history.loc[history['Tweet ID'] ==not_replied_to['Tweet ID'][thing] , 'Responded'] = 'Yes'
                
            elif any(x in not_replied_to['Text'][thing].lower() for x in thnxbb):
                which_answer = random.randint(0,3)
                a = '@%s You are very welcome' % (not_replied_to['User'][thing])
                b = '@%s Happy to help :D' % (not_replied_to['User'][thing])
                c = '@%s Cheerio!' % (not_replied_to['User'][thing])
                d = '@%s Happy to share the podcast love' % (not_replied_to['User'][thing])
                answers = [a,b,c,d]
                api.update_status(answers[which_answer])
            #api.update_status("@"+not_replied_to['User'][thing]+" You got " + Win.iloc[thing]['Genre'] +". Why not try out "+ Win.iloc[thing]['Title']+ "? They can be found at: " + Win.iloc[thing]['Tiny'], not_replied_to['Tweet ID'][thing])
                history = history.append(not_replied_to, ignore_index=True)
                history.loc[history['Tweet ID'] ==not_replied_to['Tweet ID'][thing] , 'Responded'] = 'Yes'
            else:
                api.update_status("@%s Sorry,I didn't understand that. Try 'recommend' !"% (not_replied_to['User'][thing]))
                history = history.append(not_replied_to, ignore_index=True)
                
            print(history)
            history.to_csv('history.csv')
                
            #print(history)
    else:
        print("Nothing to tweet")
    



# In[26]:


def do_the_thing():
    spinnydf =get_recommendations("https://docs.google.com/spreadsheets/d/e/2PACX-1vTWc2VxHamAlR4RQK2GiDg6eVGiWa-azbIssCeSwxMnOOuqv200oZoIgxF4LWcAWHOAVBugXLUbQx9E/pub?output=csv", ['Title', 'Genre', 'Genre Number', 'Link'])
    #print(spinnydf)
    
    #-----------------------------------#
    #change order to spin after length and pick that many winners
    #add in alternate phrasing 
    Tweets = pd.DataFrame()
    now = get_mentions(10)
    if path.exists("history.csv"):
        history =pd.read_csv('history.csv')
    else:
        hcolumn_names = ['Tweet ID', 'User', 'Created At', 'Text']
        history = pd.DataFrame(columns = hcolumn_names)
        history.to_csv('history.csv')
    new = np.setdiff1d(now['Tweet ID'],history['Tweet ID'])
    not_replied_to = now[now['Tweet ID'].isin(new)]
    print(not_replied_to)
    Win2 = spinthewheel(spinnydf, not_replied_to)
    
    #print(not_replied_to)
    history2 =pd.read_csv('history.csv')
    

    reply_and_update(Win2,history2, now, new, not_replied_to)




# In[28]:


do_the_thing()


# In[43]:


history2 =pd.read_csv('history.csv')


# In[44]:


history2

