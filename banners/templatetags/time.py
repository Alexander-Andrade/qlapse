from django import template
from banners.models import Banner

register = template.Library()

@register.tag(name="current_time")
def current_time():
    pass