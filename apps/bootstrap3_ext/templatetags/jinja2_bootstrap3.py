from coffin.template import Library
from jinja2 import Markup as mark_safe

from bootstrap3.forms import render_form


register = Library()

@register.object()
def bootstrap_form(*args, **kwargs):
    return mark_safe(render_form(*args, **kwargs))
