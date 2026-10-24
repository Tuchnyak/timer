def format_time(seconds: int) -> str:
    minutes, secs = divmod(seconds, 60) if seconds >= 0 else (0, 0)
    return f"{minutes:02d}:{secs:02d}"


