from google_sheet_reader import read_google_sheet
from water_calculator import calculate_water_usage
from issue_detector import detect_issues
from ticket_manager import create_ticket

from database import (
    save_water_usage,
    save_ticket,
    submission_exists
)

# Read data from Google Sheet
df = read_google_sheet()

# Process every form submission
for index, row in df.iterrows():

    # Form Timestamp
    timestamp = str(row["Timestamp"])

    # Skip if already processed
    if submission_exists(timestamp):
        print(
            f"Skipping existing submission: {timestamp}"
        )
        continue

    room_number = row["2. Room Number"]
    hostel_block = row["3. Hostel Block"]

    students = [1, 2, 3]

    for student in students:

        name_col = f"Student {student} Name (Optional)"

        # Skip empty student names
        if str(row[name_col]).strip() == "":
            continue

        student_name = row[name_col]

        wash_duration = float(
            row[f"Student {student}: Wash Basin Duration (average minutes per use)"]
        )

        wash_count = float(
            row[f"Student {student}: Wash Basin Count (times per day)"]
        )

        shower_duration = float(
            row[f"Student {student}: Shower Duration (average minutes per use)"]
        )

        shower_count = float(
            row[f"Student {student}: Shower Count (times per day)"]
        )

        flush_count = float(
            row[f"Student {student}: Flush Count (times per day)"]
        )

        # Calculate Water Usage
        total_usage = calculate_water_usage(
            wash_duration,
            wash_count,
            shower_duration,
            shower_count,
            flush_count
        )

        # Save Water Usage
        save_water_usage(
            student_name,
            room_number,
            hostel_block,
            total_usage,
            timestamp
        )

        print("\n====================================")
        print("Student Name :", student_name)
        print("Room Number  :", room_number)
        print("Hostel Block :", hostel_block)
        print("Water Usage  :", total_usage, "Litres")

        # Issue Detection
        room_limit = 135

        issues = detect_issues(
            total_usage,
            room_limit,
            shower_duration,
            wash_duration
        )

        if len(issues) > 0:

            print("\nIssues Found:")

            for issue in issues:

                print("-", issue)

                ticket = create_ticket(
                    room_number,
                    issue
                )

                save_ticket(
                    ticket["room_number"],
                    ticket["issue"]
                )

                print("Ticket Created")

        else:

            print("\nNo Issues Found")

        print("====================================")

print("\nAll New Form Responses Processed Successfully!")