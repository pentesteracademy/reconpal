from typing import Union, Dict, Optional

from telegram.ext import MessageFilter
from datetime import datetime, timezone


class DateFilter(MessageFilter):
    def filter(self, message) -> Optional[Union[bool, Dict]]:
        return (datetime.now(timezone.utc) - message.date).days <= 3
