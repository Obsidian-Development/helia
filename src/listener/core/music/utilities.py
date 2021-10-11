def parse_duration(duration: int) -> str:
    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    duration = []
    if days > 0:
        duration.append(f"{days}d")
    if hours > 0:
        duration.append(f"{hours}h")
    if minutes > 0:
        duration.append(f"{minutes}m")
    if seconds > 0:
        duration.append(f"{seconds}s")

    return " : ".join(duration)
