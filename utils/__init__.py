import re


def text(*args, sep: str = '\n') -> str:
    return sep.join(args)


def split_words(input_string: str) -> list[str]:
    values = re.split(r'[,;\s]+', input_string)
    values = [value.replace('_', '').replace('-', '') for value in values if value.strip()]
    return values
