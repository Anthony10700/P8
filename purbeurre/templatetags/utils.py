"""this file contain filters to applicate at the gabarit

    Returns:
        [type]: [description]
    """
from django import template

register = template.Library()


@register.filter('get_item')
def get_item(dict_data, key):
    """
    use example {{ your_dict|get_item:your_key }}
    """
    if key:
        return dict_data.get(key)
