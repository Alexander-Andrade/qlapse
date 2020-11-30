import datetime
from django import template

register = template.Library()
from banners.models import Banner, QueueItem

@register.simple_tag(takes_context=True) #, name="current_time"
def current_time(context, format_string):
    context['time'] = QueueItem.objects.get(created_at=created_at)
    context['current_time'] = datetime.datetime.now().strftime(self.format_string)
    return current_time(current_time, format_string)
