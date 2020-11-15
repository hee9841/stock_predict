#!/usr/bin/env python
# coding: utf-8

# In[15]:

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense,LSTM,Dropout, Activation

import datetime


# In[16]:


dataset = pd.read_csv('../dataset/005930.KS.csv', sep=',')

data = dataset.dropna()


# In[75]:


df=data[['Close']]
df.shape
df=np.array(df)


# In[97]:


new_windows = df[-10:]


# In[102]:



for p in new_windows:
    tandardized_window = ((p - np.mean(new_windows)) / (np.std(new_windows)))
    standardized_data.append(tandardized_window)

print(standardized_data)


# In[109]:


windows = np.array(standardized_data)


# In[115]:


windows = np.array(standardized_data)

x = windows
x = np.reshape(x,(1,x.shape[0], x.shape[1]))
x.shape


# In[116]:


seed = 0
np.random.seed(seed)
tf.random.set_seed(3)


# In[117]:


model = load_model('./test5_model.h5')


# In[118]:


yesterday_close_input = x

pre_close_temp = model.predict(yesterday_close_input)
pre_close =  (pre_close_temp * np.std(new_windows)) + np.mean(new_windows)


# In[120]:


print("다음 종가 : %0.2f 원" %pre_close)
