from django import template

register = template.Library()

@register.filter
def filter_statut(queryset, statut):
    return queryset.filter(statut=statut).count() 