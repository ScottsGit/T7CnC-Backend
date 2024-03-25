import pandas as pd
import numpy as np
from typing import List
from app.data_schema import *
from datetime import datetime, timedelta
import random

def extract_data_from_transactions(transactions):
    formatted = []
    
    for trans in transactions:
        # category = trans['category'][1] if trans['category'] and len(trans['category']) > 1 else trans['category'][0]
        if trans['category']:
            category = trans['category'][1] if len(trans['category']) > 1 else trans['category'][0]
        else:
            category = 'None'
            
        formatted.append({"category": str(category), 
                          "date": str(trans['date']), 
                          "name": str(trans['name']), 
                          "amount": str(trans['amount'])})
    return formatted

def extract_data_from_balance(accounts):
    formatted = []
    
    for account in accounts:
        formatted.append({"name":account['name'], 
                        "current":account['balances']['current'], 
                        "type":account['type'],
                        'available':account['balances']['available']}
                        )
    return formatted

def format_net_worth_by_day(transactions) -> pd.DataFrame:
    try:
        data = pd.DataFrame(transactions, columns=['category', 'date', 'name', 'amount'])
    except Exception as e:
        print("An error occurred:", e)
    
    data.drop(["name"], axis=1, inplace=True)    
    data['amount'] = data['amount'].astype(float)
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    data = data.groupby(['date', 'category']).sum().reset_index()
    
    # data['date'] = data['date'].dt.strftime('%y-%m-%d')
    
    # Create and initialize index column
    # data.insert(1, 'Index', range(1, len(data)+1))
    # data.set_index('Index', inplace=True)
    
    data['networth'] = 0.0
    # data.insert(1, 'networth', 0)

    net_worth = 0.0
    for index, row in data.iterrows():
        amount = row['amount']
        if amount < 0:
            net_worth += -amount
            data.at[index, 'networth'] = net_worth
        elif amount > 0:
            net_worth -= amount
            data.at[index, 'networth'] = net_worth
    
    data.drop(["amount", "category"], axis=1, inplace=True)
    
    print("formatted net worth ===============================")
    print(data)
    return data


def format_net_worth_by_month(transactions) -> pd.DataFrame:
    try:
        data = pd.DataFrame(transactions, columns=['category', 'date', 'name', 'amount'])
    except Exception as e:
        print("An error occurred:", e)
        
    print(data.columns)
    data.drop(columns=["name"], inplace=True)    
    data['amount'] = data['amount'].astype(float)
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    data['date'] = data['date'].dt.strftime('%Y-%m')
    data = data.groupby(['date']).sum().reset_index()
    
    # data['date'] = data['date'].dt.strftime('%y-%m')
    
    # Create and initialize index column
    # data.insert(1, 'Index', range(1, len(data)+1))
    # data.set_index('Index', inplace=True)
    
    data['networth'] = 0.0
    # data.insert(1, 'networth', 0)

    net_worth = 0.0
    for index, row in data.iterrows():
        amount = row['amount']
        if amount < 0:
            net_worth += -amount
            data.at[index, 'networth'] = net_worth
        elif amount > 0:
            net_worth -= amount
            data.at[index, 'networth'] = net_worth
    
    data.drop(["amount", "category"], axis=1, inplace=True)
    
    print("formatted net worth ===============================")
    print(data)
    return data




def format_spends_by_name(transactions) -> pd.DataFrame:
    data = pd.DataFrame(transactions)
    # "amount=-4.22 category='Payroll' date=datetime.datetime(2024, 1, 20, 0, 0) name='INTRST PYMNT'"
    
    # Set date format and sort by date
    data.drop(["category"], axis=1, inplace=True)    
    data['amount'] = data['amount'].astype(float)
    data = data[data['amount'] >= 0]
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    data.drop(["date"], axis=1, inplace=True)   
    data = data.groupby(['name']).sum().reset_index()
    # Create and initialize index column
    # data['Index'] = range(1, len(data) + 1)
    # data.set_index('Index', inplace=True)
    
    print("formatted spends ===============================")
    print(data)
    return data

def format_spends_by_category(transactions) -> pd.DataFrame:
    data = pd.DataFrame(transactions)
    # "amount=-4.22 category='Payroll' date=datetime.datetime(2024, 1, 20, 0, 0) name='INTRST PYMNT'"
    
    # Set date format and sort by date
    data.drop(["name"], axis=1, inplace=True)    
    data['amount'] = data['amount'].astype(float)
    data = data[data['amount'] >= 0]
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    data.drop(["date"], axis=1, inplace=True)   
    data = data.groupby(['category']).sum().reset_index()
    # Create and initialize index column
    # data['Index'] = range(1, len(data) + 1)
    # data.set_index('Index', inplace=True)
    
    print("formatted spends ===============================")
    print(data)
    return data


def format_spends_by_date(transactions) -> pd.DataFrame:
    data = pd.DataFrame(transactions)
    # "amount=-4.22 category='Payroll' date=datetime.datetime(2024, 1, 20, 0, 0) name='INTRST PYMNT'"
    
    # Set date format and sort by date
    data.drop(["category", "name"], axis=1, inplace=True)    
    data['amount'] = data['amount'].astype(float)
    data = data[data['amount'] >= 0]
    data['date'] = pd.to_datetime(data['date'])
    data.sort_values(by='date', inplace=True)
    
    data = data.groupby(['date']).sum().reset_index()
    # Create and initialize index column
    # data['Index'] = range(1, len(data) + 1)
    # data.set_index('Index', inplace=True)
    
    print("format_spends_by_date ===============================")
    print(data)
    return data

def add_random_number(x):
    return x + np.random.randint(-34, 43)

def prepare_spends_line_chart(df: pd.DataFrame):
    data = df.copy()
    # Calculate today's date
    today = datetime.today()

    # Calculate the end date for the last 30 days
    last_30_days_end_date = today - timedelta(days=1)  # Yesterday
    # Calculate the start date for the last 30 days
    last_30_days_start_date = last_30_days_end_date - timedelta(days=30)  # 30 days before yesterday

    # Calculate the end date for the 30 days before the last 30 days
    previous_30_days_end_date = last_30_days_start_date
    # Calculate the start date for the 30 days before the last 30 days
    previous_30_days_start_date = previous_30_days_end_date - timedelta(days=30)

    # Filter the DataFrame for the 30 days before the last 30 days
    previous_30_days_data = data[(data['date'] >= previous_30_days_start_date) & (data['date'] <= previous_30_days_end_date)].reset_index(drop=True)
    # previous_30_days_data['amount'] = previous_30_days_data['amount'] - previous_30_days_data['amount'].iloc[0]
    previous_30_days_data['amount'] = previous_30_days_data['amount'].apply(add_random_number)
    
    # Filter the DataFrame for the last 30 days
    last_30_days_data = data[(data['date'] >= last_30_days_start_date) & (data['date'] <= last_30_days_end_date)].reset_index(drop=True)
    # last_30_days_data['amount'] = last_30_days_data['amount'] - last_30_days_data['amount'].iloc[0]
    last_30_days_data['amount'] = last_30_days_data['amount'].apply(add_random_number)
    
    print("previous_30_days_data")
    print(previous_30_days_data)
    print("last_30_days_data")
    print(last_30_days_data)
    
    series = [{
        "name": "Spending Last Month",
        "data": previous_30_days_data['amount'].round(2).to_list()
    },
    {
        "name": "Spending This Month",
        "data": last_30_days_data['amount'].round(2).to_list()
    }]
    
    return {'series': series}




def prepare_networth_line_chart(df: pd.DataFrame):
    print(df)
    data = df.copy()
    
    # Calculate today's date
    today = datetime.today()

    # Calculate the end date for the last 30 days
    last_30_days_end_date = today - timedelta(days=1)  # Yesterday
    # Calculate the start date for the last 30 days
    last_30_days_start_date = last_30_days_end_date - timedelta(days=30)  # 30 days before yesterday

    # Calculate the end date for the 30 days before the last 30 days
    previous_30_days_end_date = last_30_days_start_date
    # Calculate the start date for the 30 days before the last 30 days
    previous_30_days_start_date = previous_30_days_end_date - timedelta(days=30)

    # Filter the DataFrame for the 30 days before the last 30 days
    previous_30_days_data = data[(data['date'] >= previous_30_days_start_date) & (data['date'] <= previous_30_days_end_date)].reset_index(drop=True)
    previous_30_days_data['networth'] = previous_30_days_data['networth'] - previous_30_days_data['networth'].iloc[0]
    previous_30_days_data['networth'] = previous_30_days_data['networth'].apply(add_random_number)
    
    # Filter the DataFrame for the last 30 days
    last_30_days_data = data[(data['date'] >= last_30_days_start_date) & (data['date'] <= last_30_days_end_date)].reset_index(drop=True)
    last_30_days_data['networth'] = last_30_days_data['networth'] - last_30_days_data['networth'].iloc[0] + random.randint(-100, 100)
    last_30_days_data['networth'] = last_30_days_data['networth'].apply(add_random_number)
    
    print("previous_30_days_data")
    print(previous_30_days_data)
    print("last_30_days_data")
    print(last_30_days_data)

    series = [{
        "name": "Spending Last Month",
        "data": previous_30_days_data['networth'].round(2).to_list()
    },
    {
        "name": "Spending This Month",
        "data": last_30_days_data['networth'].round(2).to_list()
    }]
    
    xaxis = {
        "categories": []
    }
    print(series)
    print(xaxis)
    return {'series': series, 'xaxis': xaxis}



def prepare_spends_column_chart(df: pd.DataFrame):
    print("prepare_spends_column_chart")
    data = df.copy()
    networths = []
    
    feed = []
    for index, row in data.iterrows():
        feed.append({
            'y': round(row['networth'], 2),
            'x': row['date']
        })
    

    series = [{
        "name": "Net Worth",
        "data": feed
    }]
    
    print("column chart =====================")
    print(series)
    return {'series': series, 'networths': []}



def prepare_spends_polar_chart_by_category(df: pd.DataFrame):
    print(df)
    data = df.copy()
    print("prepare_spends_polar_chart =========================")
    print(data)
    data = data.groupby('category').sum().reset_index()
    
    series = data['amount'].to_list()
    categories = data['category'].to_list()
    return {'series': series, 'categories': categories}

def prepare_spends_polar_chart_by_name(df: pd.DataFrame):
    print(df)
    data = df.copy()
    print("prepare_spends_polar_chart =========================")
    print(data)
    data = data.groupby('name').sum().reset_index()
    
    series = data['amount'].to_list()
    categories = data['name'].to_list()
    return {'series': series, 'categories': categories}