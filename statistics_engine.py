import mysql.connector
import pandas as pd

def get_statistics():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dhanya@1992",
        database="smart_water_management"
    )

    query = """
    SELECT
        student_name,
        room_number,
        usage_liters
    FROM water_usage
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if len(df) == 0:
        return None

    stats = {}

    stats["average_usage"] = df["usage_liters"].mean()

    stats["highest_usage_student"] = (
        df.loc[df["usage_liters"].idxmax()]
        ["student_name"]
    )

    stats["highest_usage_value"] = (
        df["usage_liters"].max()
    )

    stats["lowest_usage_student"] = (
        df.loc[df["usage_liters"].idxmin()]
        ["student_name"]
    )

    stats["lowest_usage_value"] = (
        df["usage_liters"].min()
    )

    room_usage = (
        df.groupby("room_number")
        ["usage_liters"]
        .sum()
    )

    stats["highest_usage_room"] = (
        room_usage.idxmax()
    )

    stats["highest_room_usage"] = (
        room_usage.max()
    )

    stats["lowest_usage_room"] = (
        room_usage.idxmin()
    )

    stats["lowest_room_usage"] = (
        room_usage.min()
    )

    return stats