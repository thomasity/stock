import hashlib

def norm_title(s: str) -> str:
    return " ".join((s or "").lower().split())

class Deduper:
    def __init__(self, max_size=10000):
        self._seen = set()
        self._order = deque()
        self.max_size = max_size

    def key(self, raw: dict) -> str:
        title = norm_title(raw.get("title", ""))
        url = (raw.get("url", "").split("?")[0]).lower()
        src = (raw.get("source", "") or "").lower()
        return hashlib.sha1(f"{title}|{url}|{src}".encode()).hexdigest()

    def is_dup(self, raw: dict) -> bool:
        k = self.key(raw)
        if k in self._seen:
            return True
        self._seen.add(k)
        self._order.append(k)
        if len(self._order) > self.max_size:
            oldest = self._order.popleft()
            self._seen.remove(oldest)
        return False
