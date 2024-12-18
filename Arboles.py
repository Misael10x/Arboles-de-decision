#!/usr/bin/env python
# coding: utf-8

# # Arboles de Decisión: Caso Práctico
# 
# En este caso de uso práctico se pretende resolver un problema de detección de malware en dispositivos Android mediante el análisis del tráfico de red que genera el dispositivo mediante el uso de árboles de decisión.
# 

# ## DataSet: Detección de malware en Android.

# The sophisticated and advanced Android malware is able to identify the presence of the emulator used by the malware analyst and in response, alter its behaviour to evade detection. To overcome this issue, we installed the Android applications on the real device and captured its network traffic. 
# 
# CICAAGM dataset is captured by installing the Android apps on the real smartphones semi-automated. The dataset is generated from 1,900 applications with the following three categories:
# 1. Adware (250 apps)
# 
#     Airpush: Designed to deliver unsolicited advertisements to the user’s systems for information stealing.
# 
#     Dowgin: Designed as an advertisement library that can also steal the user’s information.
# 
#     Kemoge: Designed to take over a user’s Android device. This adware is a hybrid of botnet and disguises itself as popular apps via repackaging.
# # ### Buscando correlaciones.

# In[10]:


# Copiar el DataSet y transformar la variable de salida a numérica para calcular las correlaciones.
X = df.copy()
X['calss'] = X['calss'].factorize()[0]


# In[11]:


# Calcular las correlaciones
corr_matrix = X.corr()
corr_matrix["calss"].sort_values(ascending = False)


# In[12]:


X.corr()


# In[13]:


# Se puede llegar a valorar y quedarnos con aquellas que tienen mayor correlación.
corr_matrix[corr_matrix["calss"] > 0.05]


# # 3.- División del DataSet.

# In[14]:


# Dividir el Dataset
train_set, val_set, test_set = train_val_test_split(X)


# In[15]:


X_train, y_train = remove_labels(train_set, 'calss')
X_val, y_val = remove_labels(val_set, 'calss')
X_test, y_test = remove_labels(test_set, 'calss')

#     Mobidash: Designed to display ads and to compromise user’s personal information.
# 
#     Shuanet: Similar to Kemoge, Shuanet is also designed to take over a user’s device.
# 
# 2. General Malware (150 apps)
# 
#     AVpass: Designed to be distributed in the guise of a Clock app.
# 
#     FakeAV: Designed as a scam that tricks user to purchase a full version of the software in order to re-mediate non-existing infections.
# 
#     FakeFlash/FakePlayer: Designed as a fake Flash app in order to direct users to a website (after successfully installed).
# 
#     GGtracker: Designed for SMS fraud (sends SMS messages to a premium-rate number) and information stealing.
# 
#     Penetho: Designed as a fake service (hacktool for Android devices that can be used to crack the WiFi password). The malware is also able to infect the user’s computer via infected email attachment, fake updates, external media and infected documents.
# 
# 3. Benign (1,500 apps)
# 
#     2015 GooglePlay market (top free popular and top free new)
# 
#     2016 GooglePlay market (top free popular and top free new)
# 
# License
# 
# The CICAAGM dataset consists of the following items is publicly available for researchers.
# 
#     .pcap files – the network traffic of both the malware and benign (20% malware and 80% benign)
# 
#     .csv files - the list of extracted network traffic features generated by the CIC-flowmeter
# 
# If you are using our dataset, you should cite our related paper that outlines the details of the dataset and its underlying principles:
# 
#     Arash Habibi Lashkari, Andi Fitriah A. Kadir, Hugo Gonzalez, Kenneth Fon Mbah and Ali A. Ghorbani, “Towards a Network-Based Framework for Android Malware Detection and Characterization”, In the proceeding of the 15th International Conference on Privacy, Security and Trust, PST, Calgary, Canada, 2017.
# 

# # Imports

# In[1]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import confusion_matrix, recall_score, f1_score, precision_score
from pandas import DataFrame


# # Funciones auxiliares

# In[2]:


# Construcción de una función que realize el particionado completo.
def train_val_test_split(df, rstate=42, shuffle=True, stratify=None):
    strat = df[stratify] if stratify else None 
    train_set, test_set = train_test_split(
        df, test_size = 0.4, random_state = rstate, shuffle = shuffle, stratify = strat)
    strat = train_test[stratify] if stratify else None
    val_set, test_set = train_test_split(
        test_set, test_size=0.5, random_state = rstate, shuffle=shuffle, stratify = strat)
    return (train_set, val_set, test_set)


# In[3]:


def remove_labels(df, label_name):
    X = df.drop(label_name, axis = 1)
    y = df[label_name].copy()
    return(X, y)


# In[4]:


def evaluate_result(y_pred, y, y_prep_pred, y_prep, metric):
    print(metric.__name__, "WITHOUT preparation:", metric(y_pred, y, average='weighted'))
    print(metric.__name__, "WITH preparation:", metric(y_prep_pred, y_prep, average='weighted'))


# # 1.- Lectura del DataSet

# In[5]:


df = pd.read_csv('AndroiDataSet/AndroidAdware2017/TotalFeatures-ISCXFlowMeter.csv')


# In[6]:


df


# # 2.- Visualización del DataSet.

# In[7]:


df.head(10)


# In[8]:


df.info()


# In[9]:


df["calss"].value_counts()


# ### Buscando correlaciones.

# In[10]:


# Copiar el DataSet y transformar la variable de salida a numérica para calcular las correlaciones.
X = df.copy()
X['calss'] = X['calss'].factorize()[0]


# In[11]:


# Calcular las correlaciones
corr_matrix = X.corr()
corr_matrix["calss"].sort_values(ascending = False)


# In[12]:


X.corr()


# In[13]:


# Se puede llegar a valorar y quedarnos con aquellas que tienen mayor correlación.
corr_matrix[corr_matrix["calss"] > 0.05]


# # 3.- División del DataSet.

# In[14]:


# Dividir el Dataset
train_set, val_set, test_set = train_val_test_split(X)


# In[15]:


X_train, y_train = remove_labels(train_set, 'calss')
X_val, y_val = remove_labels(val_set, 'calss')
X_test, y_test = remove_labels(test_set, 'calss')


# # 4.- Escalado del Dataset.
# 
# Es importante comprender que los arboles de decisión son algoritmos que **no requieren demasiada preparación de los datos** concretamente, no requieren realizar escalado y normalización. En este ejercicio se realiza el escalado al DataSet y se comparan los resultados con el DataSet sin escalar. De esta manera se demuestra como aplicar preprocesamientos como el escalado puede afectar el rendimiento del problema o del módelo.

# In[16]:


scaler = RobustScaler()
X_train_scaled = scaler.fit_transform(X_train)


# In[17]:


scaler = RobustScaler()
X_test_scaled = scaler.fit_transform(X_test)


# In[18]:


scaler = RobustScaler()
X_val_scaled = scaler.fit_transform(X_val)


# In[19]:


# Realizar la transformación a un DataFrame de pandas
X_train_scaled = DataFrame(X_train_scaled, columns = X_train.columns, index=X_train.index)
X_train_scaled.head(10)


# In[20]:


X_train_scaled.describe()


# # 5.- Árbol de Decisión.

# In[21]:


from sklearn.tree import DecisionTreeClassifier

MAX_DEPTH = 20

# Módelo entrenado con el DataSet sin escalar
clf_tree = DecisionTreeClassifier(max_depth = MAX_DEPTH, random_state = 42)
clf_tree.fit(X_train, y_train)


# In[22]:


# Módelo entrenado con el DataSet escalado
clf_tree_scaled = DecisionTreeClassifier(max_depth = MAX_DEPTH, random_state = 42)
clf_tree_scaled.fit(X_train_scaled, y_train)


# Comenzar prediciendo con el propio DataSet con el que se ha entrenado el algoritmo (train_set), suele ser interesante para comprobar si se esta produciendo overfiting.

# In[23]:


# Predecir con el DataSet de entrenamiento
y_train_pred = clf_tree.predict(X_train)
y_train_prep_pred = clf_tree_scaled.predict(X_train_scaled)


# In[24]:


# Comprobar resultados entre el escalado y sin escalar
evaluate_result(y_train_pred, y_train, y_train_prep_pred, y_train, f1_score)


# # 6.- Visualizando el Limite de desicion

# In[25]:


# Se reduce el numero de atributos del conjunto de DataSet para visualizarlo mejor


# In[26]:


X_train_reduced = X_train[['min_flowpktl', 'flow_fin']]


# In[27]:


# Se genera un modelo con el DataSet reducido.
clf_tree_reduced = DecisionTreeClassifier(max_depth=2, random_state = 42)
clf_tree_reduced.fit(X_train_reduced, y_train)


# In[28]:


# Representar gŕaficamente el límite de decisión construido
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

def plot_decision_boundary(clf, X, y, plot_training = True, resolution = 1000):
    mins = X.min(axis = 0) - 1
    maxs = X.max(axis = 0) + 1
    x1, x2 = np.meshgrid(np.linspace(mins[0], maxs[0], resolution),
                         np.linspace(mins[1], maxs[1], resolution))
    X_new = np.c_[x1.ravel(), x2.ravel()]
    y_pred = clf.predict(X_new).reshape(x1.shape)
    custom_cmap = ListedColormap(['#fafab0', '#9898ff', '#a0faa0'])
    plt.contourf(x1, x2, y_pred, alpha = 0.3, cmap = custom_cmap)
    custom_cmap2 = ListedColormap(['#7d7d58', '#4c4c7f', '#507d50'])
    plt.contourf(x1, x2, y_pred, cmap = custom_cmap2, alpha = 0.8)
    if plot_training:
        plt.plot(X[:, 0][y==0], X[:, 1][y==0], "yo", label="normal")
        plt.plot(X[:, 0][y==1], X[:, 1][y==1], "bs", label="adware")
        plt.plot(X[:, 0][y==2], X[:, 1][y==2], "g^", label="malware")
        plt.axis([mins[0], maxs[0], mins[1], maxs[1]])
        plt.xlabel('min_flowpktl', fontsize = 14)
        plt.ylabel('flow_fin', fontsize = 14, rotation = 90)
        
plt.figure(figsize = (12,6))
plot_decision_boundary(clf_tree_reduced, X_train_reduced.values, y_train)
plt.show()


# In[29]:


# Pintar el arbol para compararlo con la representacion grafica anterior
from graphviz import Source
from sklearn.tree import export_graphviz
import os

export_graphviz(
    clf_tree_reduced,
    out_file = "android_malware.dot",
    feature_names = X_train_reduced.columns,
    class_names = ["bening", "adware", "malware"],
    rounded = True,
    filled = True
)
Source.from_file("android_malware.dot")
