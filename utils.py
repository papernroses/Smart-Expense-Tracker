import pandas as pd
import os

DATA_PATH = "data/expenses.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame(columns=["date", "amount", "category", "description"])
    return pd.read_csv(DATA_PATH)

def save_expense(date, amount, category, description):
    df = load_data()
    new_row = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_PATH, index=False)

def category_summary(df):
    return df.groupby("category")["amount"].sum()

def monthly_summary(df):
    df["date"] = pd.to_datetime(df["date"])
    return df.groupby(df["date"].dt.to_period("M"))["amount"].sum()