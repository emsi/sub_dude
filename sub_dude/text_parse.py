import textwrap


def word_wrap(text, line_length=100):
    """Wraps text to a specified line length"""
    return "\n".join(textwrap.wrap(text, width=line_length))
