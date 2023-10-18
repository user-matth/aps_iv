from django import template
import base64

register = template.Library()

@register.filter
def binary_to_base64(binary_data):
    return base64.b64encode(binary_data).decode()
