import time
from collections import defaultdict
from threading import Lock

from config import RATE_LIMIT_REQUESTS, RATE_LIMIT_SECONDS


class RateLimiter:
    def __init__(self):
        self.calls = defaultdict(list)
        self.lock = Lock()

    def allow(self, user_id: int) -> bool:
        now = time.time()
        window = RATE_LIMIT_SECONDS
        max_calls = RATE_LIMIT_REQUESTS
        with self.lock:
            lst = self.calls[user_id]
            # remove old
            while lst and lst[0] <= now - window:
                lst.pop(0)
            if len(lst) >= max_calls:
                return False
            lst.append(now)
            return True
