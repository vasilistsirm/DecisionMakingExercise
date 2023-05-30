import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error


# Generate the synthetic time series dataset
date_rng = pd.date_range(start='1/1/2018', end='12/31/2022', freq='D')
val = 40 + 15 * np.tile(np.sin(np.linspace(-np.pi, np.pi, 365)), 5)
val = np.append(val, val[1824]) + 5 * np.random.rand(1826)
series = pd.DataFrame({
    'values': val
}, index=pd.DatetimeIndex(date_rng))

# Plot the original time series
series.plot()
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Synthetic Time Series')
plt.show()

# Perform decomposition
decomposition = seasonal_decompose(series, model='additive')

# Plot the trend component
plt.plot(decomposition.trend)
plt.xlabel('Date')
plt.ylabel('Trend')
plt.title('Trend Component')
plt.show()

# Plot the seasonal component
plt.plot(decomposition.seasonal)
plt.xlabel('Date')
plt.ylabel('Seasonality')
plt.title('Seasonal Component')
plt.show()

# Plot the residuals component
plt.plot(decomposition.resid)
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.title('Residuals Component')
plt.show()


# Split data into training and testing sets
train_size = int(len(series) * 0.76)
train_data, test_data = series[:train_size], series[train_size:]

# Train the ARIMA model
model = ARIMA(train_data, order=(1, 0, 1))
model_fit = model.fit()

# Make predictions on the testing set
predictions = model_fit.predict(start=len(train_data), end=len(series) - 1)

# Evaluate the model performance
mse = mean_squared_error(test_data['values'], predictions)
rmse = np.sqrt(mse)
print('Root Mean Squared Error (RMSE):', rmse)
