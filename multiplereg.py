import pandas as pd
from sklearn import linear_model
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')
X = df[['Weight', 'Volume']]
y = df['CO2']

regr = linear_model.LinearRegression()
regr.fit(X,y)
plt.plot(regr)

# predictCO2 = regr.predict([[2300, 1300]])

# print(predictedCO2)
