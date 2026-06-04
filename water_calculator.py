def calculate_water_usage(
    wash_duration,
    wash_count,
    shower_duration,
    shower_count,
    flush_count
):
    wash_water = wash_duration * wash_count * 5
    shower_water = shower_duration * shower_count * 8
    flush_water = flush_count * 6

    total_water = wash_water + shower_water + flush_water

    return total_water