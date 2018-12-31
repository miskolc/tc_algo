import pandas
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pandas.read_csv('HousePrice.csv')
df = df[['Price (Older)', 'Price (New)']]
X = df[['Price (Older)']]
Y = df[['Price (New)']]

xTrain, xTest, yTrain, yTest = train_test_split(X, Y)
Lreg = LinearRegression().fit(xTrain, yTrain)
#   formula=(W1*x+b)
print('Coef(W1):', Lreg.coef_)
print('Intercept(W0/b):', Lreg.intercept_)
W1 = Lreg.coef_
b = Lreg.intercept_

plt.scatter(X, Y)
plt.plot(X, W1 * X + b, 'r-')
plt.show()
