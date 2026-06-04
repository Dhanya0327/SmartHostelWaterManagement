import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_tomorrow_usage():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhanya@1992",
        database="smart_water_management"
    )

    query = """
    SELECT usage_liters
    FROM water_usage
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if len(df) < 2:
        return None

    X = np.arange(len(df)).reshape(-1, 1)
    y = df["usage_liters"]

    model = LinearRegression()
    model.fit(X, y)

    tomorrow = model.predict([[len(df)]])[0]

    return round(tomorrow, 2)