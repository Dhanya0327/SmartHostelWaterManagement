from statistics_engine import get_statistics

stats = get_statistics()

print("\n===== HOSTEL ANALYSIS =====")

print(
    "Average Usage:",
    round(stats["average_usage"], 2),
    "Litres"
)

print(
    "Highest Usage Student:",
    stats["highest_usage_student"],
    "-",
    stats["highest_usage_value"],
    "Litres"
)

print(
    "Lowest Usage Student:",
    stats["lowest_usage_student"],
    "-",
    stats["lowest_usage_value"],
    "Litres"
)

print(
    "Highest Usage Room:",
    stats["highest_usage_room"],
    "-",
    stats["highest_room_usage"],
    "Litres"
)

print(
    "Lowest Usage Room:",
    stats["lowest_usage_room"],
    "-",
    stats["lowest_room_usage"],
    "Litres"
)