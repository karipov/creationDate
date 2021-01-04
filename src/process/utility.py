import html
from datetime import datetime
from aiogram import types


def escape_dict(unsafe: dict) -> dict:
    """
    Escapes HTML in dict values
    """
    for k, v in unsafe.items():
        if isinstance(v, dict):
            unsafe[k] = escape_dict(unsafe[k])
        else:
            if isinstance(v, str):
                unsafe[k] = html.escape(v)

    return unsafe


def tree_display(input_dict: dict, depth: int = 0) -> str:
    """
    Displays the dict in a treefied format

    :param input_dict: python dict to be treefied
    :param depth: depth to start at for the dict
    :return: treefied message
    """

    FINAL_CHAR = "  └ "
    ENTRY_CHAR = "  ├ "
    SKIP_CHAR = "  ┊ "
    KEY_CHAR = ": "
    NEWLINE_CHAR = "\n"

    # if depth == 0:
    #     out_str = "Message\n"
    # else:
    #     out_str = ""
    out_str = ""

    if type(input_dict) is dict:
        final_index = len(input_dict) - 1
        current_index = 0

        for key, value in input_dict.items():
            for _ in range(0, depth):
                out_str += SKIP_CHAR

            if current_index == final_index:
                out_str += FINAL_CHAR
            else:
                out_str += ENTRY_CHAR
                current_index += 1

            if type(value) is dict:
                out_str = (
                    out_str
                    + "<b>"
                    + key
                    + "</b>"
                    + NEWLINE_CHAR
                    + tree_display(value, depth + 1)
                )
            else:
                out_str = (
                    out_str
                    + "<b>"
                    + key
                    + "</b>"
                    + KEY_CHAR
                    + tree_display(value, depth + 1)
                    + NEWLINE_CHAR
                )
    else:
        out_str = str(input_dict)

    return out_str


def clean_message(message: types.Message) -> dict:
    dict_message = message.to_python()

    for key in list(dict_message.keys()):
        if key == "forward_from":
            del dict_message[key]["is_bot"]
            continue
        if key == "from":
            del dict_message[key]["is_bot"]
            continue
        if key == "text":
            continue

        del dict_message[key]

    return dict_message


def time_format(unix_time: int, fmt="%Y-%m-%d") -> str:
    return datetime.utcfromtimestamp(unix_time).strftime(fmt)
