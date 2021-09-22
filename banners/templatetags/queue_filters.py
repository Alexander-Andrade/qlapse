from django import template
from datetime import datetime, timezone

register = template.Library()


@register.filter(name='time_passed_since_formatter')
def time_passed_since_formatter(value):
    delta = datetime.now(timezone.utc) - value

    days = delta.days
    seconds = delta.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60

    if days != 0 and hours != 0:
        return f"{abs(days)}d {abs(hours)}h"
    if days != 0:
        return f"{abs(days)}d"
    if hours != 0 and minutes != 0:
        return f"{abs(hours)}h {abs(minutes)}m"
    if hours != 0:
        return f"{abs(hours)}h"
    if minutes != 0:
        return f"{abs(minutes)}m"

    return 'few seconds ago'


@register.filter(name='waiting_time_formatter')
def waiting_time_formatter(waiting_time):
    if waiting_time is None:
        return '∞'

    days = waiting_time.days
    seconds = waiting_time.seconds
    hours = (seconds // 3600) + days * 24
    minutes = (seconds // 60) % 60

    seconds = seconds - hours * 3600 - minutes * 60

    if hours != 0 and minutes != 0:
        return f"{abs(hours)}h {abs(minutes)}m"
    if hours != 0:
        return f"{abs(hours)}h"
    if minutes != 0 and seconds != 0:
        return f"{abs(minutes)}m {abs(seconds)}s"
    if minutes != 0:
        return f"{abs(minutes)}m"
    if seconds != 0:
        return f"{abs(seconds)}s"
