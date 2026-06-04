import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

from prediction_engine import predict_tomorrow_usage

# Page Configuration
st.set_page_config(
    page_title="Smart Hostel Water Management",
    layout="wide"
)


st.markdown("""
<style>

.main {
    background-color: #F4F8FB;
}

[data-testid="stMetric"]{
    background: linear-gradient(135deg,#ffffff,#f8fbff);
    border-radius:15px;
    padding:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(
90deg,
#1565C0,
#26A69A
);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
margin-bottom:25px;
">

<h1>
💧 Smart Hostel Water Management System
</h1>

<h3>
Real-Time Water Monitoring & Analytics Dashboard
</h3>

</div>
""", unsafe_allow_html=True)
# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhanya@1992",
    database="smart_water_management"
)

# Read Water Usage Data
query = """
SELECT *
FROM water_usage
"""

df = pd.read_sql(query, conn)

conn.close()

# =========================
# OVERVIEW
# =========================

st.header("📋 Overview")



col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👨‍🎓 Students", len(df))

with col2:
    st.metric("🚪 Rooms", df["room_number"].nunique())

with col3:
    st.metric(
        "💧 Total Usage",
        f"{df['usage_liters'].sum():.0f} L"
    )

with col4:
    st.metric(
        "📊 Avg Usage",
        f"{df['usage_liters'].mean():.0f} L"
    )

# =========================
# WATER USAGE RECORDS
# =========================

st.subheader("💧 Water Usage Records")

st.dataframe(df)

# =========================
# STUDENT ANALYSIS
# =========================

st.header("👤 Student Analysis")

highest_student = df.loc[
    df["usage_liters"].idxmax()
]

lowest_student = df.loc[
    df["usage_liters"].idxmin()
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Highest Usage Student",
        highest_student["student_name"]
    )

with col2:
    st.metric(
        "Highest Usage",
        f"{highest_student['usage_liters']} L"
    )

with col3:
    st.metric(
        "Lowest Usage Student",
        lowest_student["student_name"]
    )

with col4:
    st.metric(
        "Lowest Usage",
        f"{lowest_student['usage_liters']} L"
    )

student_usage = df[
    [
        "student_name",
        "room_number",
        "usage_liters"
    ]
]

st.dataframe(student_usage)

# =========================
# ROOM ANALYSIS
# =========================

st.header("🚪 Room-wise Analysis")

room_usage = (
    df.groupby("room_number")
    ["usage_liters"]
    .sum()
    .reset_index()
)

st.dataframe(room_usage)

highest_room = room_usage.loc[
    room_usage["usage_liters"].idxmax()
]

lowest_room = room_usage.loc[
    room_usage["usage_liters"].idxmin()
]

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Highest Usage Room",
        highest_room["room_number"]
    )

with col2:
    st.metric(
        "Lowest Usage Room",
        lowest_room["room_number"]
    )

# =========================
# CHARTS
# =========================

st.header("📊 Water Usage Charts")

fig1 = px.bar(
    room_usage,
    x="room_number",
    y="usage_liters",
    color="room_number",
    text="usage_liters",
    title="Room-wise Water Usage"
)

fig1.update_layout(
    template="plotly_white",
    height=500
)
fig3 = px.pie(
    room_usage,
    names="room_number",
    values="usage_liters",
    hole=0.55,
    title="Room Usage Distribution"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)
st.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.bar(
    df,
    x="student_name",
    y="usage_liters",
    color="student_name",
    text="usage_liters",
    title="Student-wise Water Usage"
)

fig2.update_layout(
    template="plotly_white",
    height=500
)
st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================
# HOSTEL SUMMARY
# =========================

st.header("🏠 Hostel Summary")

st.write(
    f"Total Hostel Water Consumption: "
    f"{round(df['usage_liters'].sum(), 2)} Litres"
)

st.write(
    f"Average Student Consumption: "
    f"{round(df['usage_liters'].mean(), 2)} Litres"
)

st.write(
    f"Highest Usage Student: "
    f"{highest_student['student_name']}"
)

st.write(
    f"Highest Usage Room: "
    f"{highest_room['room_number']}"
)
# =========================
# TICKET DASHBOARD
# =========================

st.header("🎫 Warden Ticket Dashboard")


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhanya@1992",
    database="smart_water_management"
)

ticket_query = """
SELECT *
FROM tickets
"""

tickets_df = pd.read_sql(
    ticket_query,
    conn
)

conn.close()
col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Assigned",
    len(
        tickets_df[
            tickets_df["status"]=="Assigned"
        ]
    )
)

col2.metric(
    "In Progress",
    len(
        tickets_df[
            tickets_df["status"]=="In Progress"
        ]
    )
)

col3.metric(
    "Resolved",
    len(
        tickets_df[
            tickets_df["status"]=="Resolved"
        ]
    )
)

col4.metric(
    "Closed",
    len(
        tickets_df[
            tickets_df["status"]=="Closed"
        ]
    )
)

st.subheader("Current Tickets")

st.dataframe(tickets_df)

if len(tickets_df) > 0:

    ticket_ids = tickets_df["ticket_id"].tolist()

    selected_ticket = st.selectbox(
        "Select Ticket",
        ticket_ids
    )

    new_status = st.selectbox(
        "Update Status",
        [
            "Assigned",
            "In Progress",
            "Resolved",
            "Closed"
        ]
    )

    if st.button("Update Ticket Status"):

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Dhanya@1992",
            database="smart_water_management"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE tickets
            SET status=%s
            WHERE ticket_id=%s
            """,
            (
                new_status,
                selected_ticket
            )
        )

        conn.commit()

        conn.close()

        st.success(
            "Ticket Updated Successfully"
        )
    
        st.header("📈 Water Usage Prediction")

prediction = predict_tomorrow_usage()

if prediction:

    st.metric(
        "Predicted Next Usage",
        f"{prediction} Litres"
    )

else:

    st.warning(
        "Not enough data for prediction"
    )