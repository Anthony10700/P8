from django import template

register = template.Library()

@register.filter('get_item')
def get_item(dict_data, key):
    """
    usage example {{ your_dict|get_item:your_key }}
    """
    if key:
        return dict_data.get(key)
