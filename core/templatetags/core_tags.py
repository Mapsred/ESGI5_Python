from django import template

register = template.Library()


@register.filter(name="times_range")
def times_range(number, start=1):
    if (number - start) > 5:
        number = start + 5

    return range(start, number)


@register.filter(name="nl2br")
def nl2br(value):
    print(value)
    return value.replace("\\n", "<br>")


@register.filter(name="type_of")
def type_of(value):
    return type(value)


@register.filter(name="checked_in")
def checked_in(value, container):
    return "checked" if container is not None and value in container else ""


@register.filter(name="boostrap_input")
def boostrap_input(value, col="col-md-6"):
    return value.as_widget(attrs={'class': 'form-control %s' % col})


class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''


@register.tag(name="assign")
def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.

    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}

    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])

    return AssignNode(bits[1], value)
