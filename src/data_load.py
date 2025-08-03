# src/data_load.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_price_data(filepath):
    """Load Brent oil price data from CSV."""
    df = pd.read_csv(filepath, parse_dates=['Date'])
    df = df.sort_values('Date')
    return df

def load_event_data(filepath):
    """Load key events data from CSV."""
    events = pd.read_csv(filepath, parse_dates=['Date'])
    return events

def describe_data(df):
    print(df['Price'].describe())
    print("\nMissing values:", df['Price'].isna().sum())
    print("\nDate Range:", df['Date'].min(), "to", df['Date'].max())

def detect_outliers(df, threshold=0.1):
    df = df.copy()
    df['LogReturn'] = np.log(df['Price']).diff()
    outliers = df[np.abs(df['LogReturn']) > threshold]
    print(f"Detected {len(outliers)} extreme return days (>{threshold})")
    return outliers

def plot_price(df, events=None):
    """Plot oil price over time, with optional events."""
    plt.figure(figsize=(15,5))
    plt.plot(df['Date'], df['Price'], label='Brent Oil Price')
    if events is not None:
        for i, row in events.iterrows():
            plt.axvline(row['Date'], color='grey', linestyle='--', alpha=0.6)
            plt.text(row['Date'], df['Price'].max()*0.95, row['Event'], rotation=90, fontsize=8, alpha=0.7)
    plt.title('Brent Oil Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price (USD/barrel)')
    plt.legend()
    plt.show()

def plot_rolling(df, window=30):
    """Plot rolling mean."""
    rolling_mean = df['Price'].rolling(window=window).mean()
    plt.figure(figsize=(15,5))
    plt.plot(df['Date'], df['Price'], alpha=0.5, label='Price')
    plt.plot(df['Date'], rolling_mean, color='red', label=f'{window}-Day Rolling Mean')
    plt.title(f'Brent Oil Price with {window}-Day Rolling Mean')
    plt.xlabel('Date')
    plt.ylabel('Price (USD/barrel)')
    plt.legend()
    plt.show()
def plot_rolling_volatility(df, window=30):
    df = df.copy()
    df['LogReturn'] = np.log(df['Price']).diff()
    df['RollingVolatility'] = df['LogReturn'].rolling(window).std()

    plt.figure(figsize=(15,4))
    plt.plot(df['Date'], df['RollingVolatility'], label=f'{window}-Day Rolling Std (Volatility)', color='purple')
    plt.title(f'Volatility Clustering Over Time ({window}-Day Rolling)')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    plt.show()

def plot_log_return(df):
    """Plot log returns."""
    df = df.copy()
    df['LogReturn'] = np.log(df['Price']).diff()
    plt.figure(figsize=(15,3))
    plt.plot(df['Date'], df['LogReturn'], color='orange')
    plt.title('Brent Oil Price Log Returns')
    plt.xlabel('Date')
    plt.ylabel('Log Return')
    plt.show()
    return df

def adf_test(series):
    """Perform Augmented Dickey-Fuller test for stationarity."""
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(series.dropna())
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])
    if result[1] < 0.05:
        print('The time series is likely stationary.')
    else:
        print('The time series is likely non-stationary.')
