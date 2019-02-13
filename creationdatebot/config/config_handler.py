from pathlib import Path

from configparser import ConfigParser
from json import load


class Config():
    def __init__(self,
                 settings: str = "setup.json",
                 dir: str = "creationdatebot/config"):
        self.dir = dir

        self.SETTINGS = self._unpack_settings()
        self.REPLIES = self._unpack_replies()


    def _unpack_settings(self, settings: str = "setup.json") -> dict:
        """
        Unpacks JSON settings file into a python dict
        """
        settings_path = Path.cwd().joinpath(self.dir, settings)

        with open(settings_path) as string_data:
            config = load(string_data)

        return config


    def _unpack_replies(self, replies: str = "replies.json") -> dict:
        """
        Unpacks JSON replies file into a python dict
        """
        replies_path = Path.cwd().joinpath(self.dir, replies)

        with open(replies_path) as string_data:
            replies = load(string_data)

        return replies
