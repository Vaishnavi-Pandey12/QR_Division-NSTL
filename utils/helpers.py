def to_display_date(value):
    return value.strftime("%d %b %Y") if hasattr(value, "strftime") else value
