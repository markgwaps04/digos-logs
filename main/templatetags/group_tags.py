from django import template
from modules.helpers import _String
register = template.Library()

@register.filter
def index(indexable, i):
   return indexable[i];

@register.filter
def length(value):
   return len(value);

@register.filter
def roman(value):
   return _String.int_to_roman(value);


@register.filter
def less_zeros(value, max = 4):
   length = len(str(value));
   less = max - length;
   list_value = [0] * less;
   return "".join([str(i) for i in list_value]);


@register.filter
def default(value, default_value):
   return value if value else default_value


@register.filter
def json(value, default_value):
   import json;
   return json.dumps(value);


@register.filter
def before(value, default_value):
   if not len(value) : return "";
   return default_value + str(value);

