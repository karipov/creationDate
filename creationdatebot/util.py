

def clean_dict(dictionary: dict) -> dict:
    """
    Cleans a message dict to output desired key-values
    """
    clean = dictionary["json"] # gets rid of pyTelegramBotAPI "null" values
    # clean_keys = list(clean.keys()) # prevent runtime error due to dict changing size


    for key in list(clean.keys()):
        if key == "from":
            continue

        if key == "forward_from":
            continue

        if key == "text":
            continue

        del clean[key]

    return clean



def cvt_time(unix_time: int, format: str) -> str:
    """
    Convenience function for converting unix time into a human-readable time
    format
    """
    pass


def check_forward(message: object) -> bool:
    """
    Checks if a message has been forwarded or not
    """
    pass
