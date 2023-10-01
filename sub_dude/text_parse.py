import textwrap


def word_wrap(text, line_length=100):
    """Wraps text to a specified line length"""
    # replace all " \\n " with "\n" to avoid word_wrap splitting on those
    text = text.replace(" \\n ", "\n")
    return "\n".join(textwrap.wrap(text, width=line_length))
