from abc import ABC
import random


class RandomMessageGenerator(ABC):
    """Random message generator"""

    _titles: [str]

    _texts: [str]

    @classmethod
    def get_title(cls) -> str:
        """Get random message title"""
        return random.choice(cls._titles).upper()

    @classmethod
    def get_text(cls) -> str:
        """Get random message text"""
        return random.choice(cls._texts)
