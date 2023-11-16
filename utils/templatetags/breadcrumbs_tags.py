from django import template

register = template.Library()


@register.inclusion_tag("breadcrumbs.html", takes_context=True)
def render_breadcrumbs(context):
    return {"breadcrumbs": context.get("breadcrumbs", [])}
