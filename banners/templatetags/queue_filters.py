from django import template
from datetime import datetime, timezone, timedelta

register = template.Library()


@register.filter(name='time_passed_since')
def time_passed_since(value):
    # breakpoint()
    delta = datetime.now(timezone.utc) - value
    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return "%s %s %s %s" % (
            abs(hours),
            ("hour" if abs(hours) == 1 else "hours"),
            abs(minutes),
            ("minute" if abs(minutes) == 1 else "minutes")
    )
