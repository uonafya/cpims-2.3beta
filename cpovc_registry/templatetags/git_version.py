"""Method to create template tag."""
from django import template


register = template.Library()


@register.assignment_tag(takes_context=True)
def git_version(context):
    """Hard coded version numbering."""
    try:
        git_short = '1.4.3'
    except Exception, e:
        print str(e)
        return '1.3.6'
    else:
        return git_short
