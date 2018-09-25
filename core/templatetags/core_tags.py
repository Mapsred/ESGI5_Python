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
