from datetime import datetime



def msg_to_dict(message: object) -> dict:
    """
    Cleans a message dict to output desired key-values
    """
    message = message.__dict__
    clean = message["json"] # gets rid of pyTelegramBotAPI "null" values

    for key in list(clean.keys()):
        if key == "forward_from":
            del clean[key]["is_bot"]
            # del clean[key]["language_code"]
            continue
        if key == "from":
            del clean[key]["is_bot"]
            del clean[key]["language_code"]
            continue
        if key == "text":
            continue

        del clean[key]

    # misc clean up
    return clean


def cvt_time(unix_time: int, format: str) -> str:
    """
    Convenience function for converting unix time into a human-readable time
    format
    """
    return datetime.utcfromtimestamp(unix_time).strftime(format)


def check_forward(message: object) -> bool:
    """
    Checks if a message has been forwarded or not
    """
    if message.__dict__["json"].get("forward_from", None):
        return True
    else:
        return False


def custom_display(input: dict, depth: int = 0) -> str:
    """
    Displays the dict in a custom, treefied format
    """

    FINAL_CHAR = '  └ '
    ENTRY_CHAR = '  ├ '
    SKIP_CHAR = '  ┊ '
    KEY_CHAR = ': '
    NEWLINE_CHAR = '\n'

    if depth == 0:
        out_str = "Message\n"
    else:
        out_str = ""

    if type(input) is dict:
        final_index = len(input) - 1
        current_index = 0

        for key, value in input.items():
            for indent in range(0, depth):
                out_str += SKIP_CHAR

            if current_index == final_index:
                out_str += FINAL_CHAR
            else:
                out_str += ENTRY_CHAR
                current_index += 1

            if type(value) is dict:
                out_str = out_str \
                        + key \
                        + NEWLINE_CHAR \
                        + custom_display(value, depth+1)
            else:
                out_str = out_str \
                        + key \
                        + KEY_CHAR \
                        + custom_display(value, depth+1) \
                        + NEWLINE_CHAR
    else:
        out_str = str(input)

    return out_str
