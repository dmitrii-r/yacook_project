from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def verbose_name(the_object, the_field):
    return the_object._meta.get_field(the_field).verbose_name
