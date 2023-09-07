# -*- coding: utf-8 -*-
"""Bigmart_Sales_ Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I7292I339ThVAdMHMiVL6cahuqLGabum
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

df_train = pd.read_csv('Train.csv')
df_test = pd.read_csv('Test.csv')

df_train

df_train.head()

df_train.shape

df_train.describe()

df_train.isnull().sum()

df_test.isnull().sum()

df_train.info()

df_train.describe()

df_train['Item_Weight'].describe()

df_train['Item_Weight'].fillna(df_train['Item_Weight'].mean(),inplace =True)
df_test['Item_Weight'].fillna(df_test['Item_Weight'].mean(),inplace =True)

df_train

df_train.isnull().sum()

df_train['Outlet_Size']

df_train['Outlet_Size'].value_counts()

df_train['Outlet_Size'].fillna(df_train['Outlet_Size'].mode()[0],inplace =True)
df_test['Outlet_Size'].fillna(df_test['Outlet_Size'].mode()[0],inplace =True)

df_train.head()

df_train.isnull().sum()

df_test.isnull().sum()

duplicate = df_train.duplicated()
print(duplicate.sum())
df_train[duplicate]

df_train

"""EDA part"""

sns.pairplot(df_train)
plt.title("Pairplot of Numerical Variables")
plt.show()

# Basic EDA - Correlation heatmap for numerical variables
plt.figure(figsize=(10, 3))
sns.heatmap(df_train.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

cat_vars = ['Item_Fat_Content','Item_Type','Outlet_Size','Outlet_Location_Type','Outlet_Type']
#create figure with subplots
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(20,13))
axs = axs.flatten()

#create barplot for each categorial variables
for i, var in enumerate(cat_vars):
    sns.barplot(x=var, y='Item_Outlet_Sales', data=df_train, ax =axs[i])
    axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation=90)

  #adjust spacing between subplots
fig.tight_layout()
plt.show()

cat_vars=['Item_Fat_Content','Outlet_Size','Outlet_Location_Type','Outlet_Type']
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12,12))

#creating piechart for each categorica variables
for i, var in enumerate(cat_vars):
    if i < len(axs.flat):
    #counting number of occurrences of each category
       cat_counts = df_train[var].value_counts()

       axs.flat[i].pie(cat_counts, labels=cat_counts.index, autopct='%1.1f%%', startangle=90)

       axs.flat[i].set_title(f'{var} Distribution')

fig.tight_layout()
fig.delaxes(axs[1][1])

plt.show()

num_vars = ['Item_Weight','Item_Visibility','Item_MRP','Outlet_Establishment_Year']

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(20,10))
axs = axs.flatten()

for i, var in enumerate(num_vars):
    sns.boxplot(x=var, data=df_train, ax=axs[i])

fig.tight_layout()

plt.show()

num_vars = ['Item_Weight','Item_Visibility','Item_MRP','Outlet_Establishment_Year']

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(20,10))
axs = axs.flatten()

for i, var in enumerate(num_vars):
    sns.violinplot(x=var, data=df_train, ax=axs[i])

fig.tight_layout()
plt.show()

num_vars = ['Item_Weight','Item_Visibility','Item_MRP','Outlet_Establishment_Year']

fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(20,10))
axs = axs.flatten()

for i, var in enumerate(num_vars):
    sns.histplot(x=var, data=df_train, ax=axs[i])

fig.tight_layout()
plt.show()

df_train.info()

!pip install klib

"""EDA using klib

"""

import klib

klib.cat_plot(df_train)

klib.corr_plot(df_train)

klib.dist_plot(df_train)

klib.missingval_plot(df_train)

"""Data Cleaning"""

klib.data_cleaning(df_train) # performs datacleaning (drop duplicates & empty rows/cols, adjust dtypes,...)

klib.clean_column_names(df_train)

klib.convert_datatypes(df_train) # converts existing to more efficient dtypes, also called inside data_cleaning()

df_train.info()

klib.mv_col_handling(df_train) # drops features with high ratio of missing vals based on informational content

df_train = klib.convert_datatypes(df_train)

df_train.info()

df_train

"""label encoding"""

#Preprocessing task before model building

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

df_train = df_train.apply(le.fit_transform)

df_train

"""One Hot ENcoding"""

df_train = pd.get_dummies(df_train, columns = ['item_fat_content','outlet_size','outlet_location_type','outlet_type'])

df_train

"""Modeling

"""

X = df_train.drop('item_outlet_sales' ,axis=1)

Y = df_train['item_outlet_sales']

Y

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=101, test_size = 0.2)

X_train

X.describe()

from sklearn.preprocessing import StandardScaler
sc= StandardScaler()

X_train_std= sc.fit_transform(X_train)

X_test_std= sc.transform(X_test)

X_train_std

X_test_std

Y_train

Y_test





from sklearn.linear_model import LinearRegression
lr= LinearRegression()

lr.fit(X_train_std,Y_train)

X_test.head()

Y_pred_lr=lr.predict(X_test_std)

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print(r2_score(Y_test,Y_pred_lr))
print(mean_absolute_error(Y_test,Y_pred_lr))
print(np.sqrt(mean_squared_error(Y_test,Y_pred_lr)))



from sklearn.ensemble import RandomForestRegressor
rf= RandomForestRegressor(n_estimators=1000)

rf.fit(X_train_std,Y_train)

Y_pred_rf= rf.predict(X_test_std)

print(r2_score(Y_test,Y_pred_rf))
print(mean_absolute_error(Y_test,Y_pred_rf))
print(np.sqrt(mean_squared_error(Y_test,Y_pred_rf)))

#!pip install xgboost

import xgboost as xg

xgb = xg.XGBRegressor(objective ='reg:linear',n_estimators = 10,seed =123)

xgb.fit(X_train_std, Y_train)

#predict the model

Y_pred_xg = xgb.predict(X_test_std)

print(r2_score(Y_test,Y_pred_xg))
print(mean_absolute_error(Y_test,Y_pred_xg))
print(np.sqrt(mean_squared_error(Y_test,Y_pred_xg)))



#Hyperparameter tuning

from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV

# define models and parameters
model = RandomForestRegressor()
n_estimators = [10, 100, 1000]
max_depth=range(1,31)
min_samples_leaf=np.linspace(0.1, 1.0)
max_features=["auto", "sqrt", "log2"]
min_samples_split=np.linspace(0.1, 1.0, 10)

# define grid search
grid = dict(n_estimators=n_estimators)

#cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=101)

grid_search_forest = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1,
                           scoring='r2',error_score=0,verbose=2,cv=2)

grid_search_forest.fit(X_train_std, Y_train)

# summarize results
print(f"Best: {grid_search_forest.best_score_:.3f} using {grid_search_forest.best_params_}")
means = grid_search_forest.cv_results_['mean_test_score']
stds = grid_search_forest.cv_results_['std_test_score']
params = grid_search_forest.cv_results_['params']

for mean, stdev, param in zip(means, stds, params):
    print(f"{mean:.3f} ({stdev:.3f}) with: {param}")

grid_search_forest.best_params_

grid_search_forest.best_score_

Y_pred_rf_grid=grid_search_forest.predict(X_test_std)

r2_score(Y_test,Y_pred_rf_grid)

#saving model

import joblib

joblib.dump(grid_search_forest,r'C:\Users\DELL\OneDrive\Desktop\internship_project\models\random_forest_grid.sav')