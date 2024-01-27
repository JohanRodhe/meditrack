from django import template
import calendar
from datetime import datetime

register = template.Library()

@register.filter
def get_days_in_month(month):
    year = datetime.now().year
    _, num_days = calendar.monthrange(year, month)
    return range(1, num_days + 1)