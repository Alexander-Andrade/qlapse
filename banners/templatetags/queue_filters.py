from django import template
from datetime import datetime, timezone, timedelta

register = template.Library()


@register.filter(name='time_passed_since')
def time_passed_since(value):
    delta = datetime.now(timezone.utc) - value

    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return "%s%s %s%s %s%s" % (
            abs(days),
            "d",
            abs(hours),
            "h",
            abs(minutes),
            "m"
    )
