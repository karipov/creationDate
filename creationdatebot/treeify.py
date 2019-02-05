
FINAL_CHAR = '  └ '
ENTRY_CHAR = '  ├ '
SKIP_CHAR = '  ┊ '
KEY_CHAR = ': '
NEWLINE_CHAR = '\n'

def custom_display(input: dict, depth: int = 0) -> str:
    """
    Displays the dict in a custom, treefied format
    """

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
