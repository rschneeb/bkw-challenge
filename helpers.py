import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

def load_and_split_data(path:str) -> tuple:
    data = pd.read_csv(path, parse_dates=['Time_UTC'])
    train = data[(data['Time_UTC'] < datetime(2021, 1, 1))]
    test = data[(data['Time_UTC'] >= datetime(2021, 1, 1))]
    train_time = train['Time_UTC']
    test_time = test['Time_UTC']
    train = train.drop(columns=['Time_UTC'])
    test = test.drop(columns=['Time_UTC'])
    return train, test, train_time, test_time

def split_data(data:pd.DataFrame):
    """Splits data"""
    train = data[(data['Time_UTC'] < datetime(2021, 1, 1))]
    test = data[(data['Time_UTC'] >= datetime(2021, 1, 1))]
    train_time = train['Time_UTC']
    test_time = test['Time_UTC']
    train = train.drop(columns=['Time_UTC'])
    test = test.drop(columns=['Time_UTC'])
    return train, test, train_time, test_time

def plot_actual_and_prediction(time_axis:pd.Series, actual_values:pd.Series, prediction:pd.Series):
    MAE = np.mean(np.abs(actual_values - prediction)).round(2)

    # Create an interactive line chart with Plotly
    fig = go.Figure()

    # Add test_target line
    fig.add_trace(go.Scatter(x=time_axis, y=actual_values, mode='lines', name='Preis'))

    # Add predictions line
    fig.add_trace(go.Scatter(x=time_axis, y=prediction, mode='lines', name='Vorhergesagter Preis'))

    # Update layout for interactivity
    fig.update_layout(
        title=f"Realer vs vorhergesagter Preis, MAE: {MAE}",
        xaxis_title="Datum",
        yaxis_title="Preis [EUR]",
        hovermode="closest",
        width=1080,
        height=720
    )

    # Show the plot
    fig.show()

def lag_data(data:pd.DataFrame, lag_hours:int, columns_to_lag:list=['Generation_Solar', 'Price', 'Generation_Gas', 'Generation_WindOffshore', 'Generation_WindOnshore', 'Load']):
    """Creates lagged data."""
    lag_hours = 24

    lagged_dfs = []
    for hour in range(1, lag_hours+1):
        lagged_data = data[columns_to_lag].copy().shift(hour)
        lagged_data.columns = [f"{column}_lag_{hour}" for column in lagged_data.columns]
        lagged_dfs.append(lagged_data)
    lagged_data = pd.concat(lagged_dfs, axis="columns")

    lagged_data = pd.concat((data, lagged_data), axis="columns")

    # drop rows with na
    lagged_data = lagged_data.dropna()

    return lagged_data