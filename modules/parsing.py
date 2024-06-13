import json
from typing import Dict, List
from abc import ABC, abstractmethod


class ParseMessage(ABC):
    @abstractmethod
    def get_data(self, message:str) -> Dict[str, str]:
        pass


class TelegramParseMessage(ParseMessage):
    def get_data(self, message:str) -> Dict[str, str]:
        """ Get dict with dt_from dt_upto group_type from message """
        result = json.loads(message)

        return result
