import mysql.connector

# Database Connection

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhanya@1992",
    database="smart_water_management"
)

cursor = conn.cursor()

# -----------------------------
# Check if Submission Exists
# -----------------------------

def submission_exists(form_timestamp):

    sql = """
    SELECT COUNT(*)
    FROM water_usage
    WHERE form_timestamp = %s
    """

    cursor.execute(sql, (form_timestamp,))

    result = cursor.fetchone()

    return result[0] > 0


# -----------------------------
# Save Ticket
# -----------------------------

def save_ticket(room_number, issue):

    sql = """
    INSERT INTO tickets
    (room_number, issue_description)
    VALUES (%s,%s)
    """

    values = (room_number, issue)

    cursor.execute(sql, values)

    conn.commit()

    print("Ticket Saved")


# -----------------------------
# Save Water Usage
# -----------------------------

def save_water_usage(
    student_name,
    room_number,
    hostel_block,
    usage_liters,
    form_timestamp
):

    sql = """
    INSERT INTO water_usage
    (
        student_name,
        room_number,
        hostel_block,
        usage_liters,
        form_timestamp
    )
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        student_name,
        room_number,
        hostel_block,
        usage_liters,
        form_timestamp
    )

    cursor.execute(sql, values)

    conn.commit()

    print(
        f"{student_name} - {usage_liters} Litres Saved"
    )


# -----------------------------
# Read Water Usage Data
# -----------------------------

def get_water_usage():

    cursor.execute(
        "SELECT * FROM water_usage"
    )

    return cursor.fetchall()


# -----------------------------
# Close Database
# -----------------------------

def close_connection():

    cursor.close()
    conn.close()