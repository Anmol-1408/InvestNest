from django import template

register = template.Library()

@register.filter
def exclude(tag_list, tag_to_remove):
    return [tag for tag in tag_list if tag != tag_to_remove]
