import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv("HousePrice.csv")
x = df.iloc[:, 1:2].values
y = df.iloc[:, 2].values

poly = PolynomialFeatures(degree=3)
poly_x = poly.fit_transform(x)

regressor = LinearRegression()
regressor.fit(poly_x, y)

plt.scatter(x, y, color='red')
plt.plot(x, regressor.predict(poly.fit_transform(x)), color='blue')
plt.show()
