"""Лимиты публичного демо: суточные счётчики платных вызовов (всего и по IP).

Хранятся в JSON рядом с историей (в контейнере — примонтированный том /app/data),
поэтому переживают пересборку. Сутки — по UTC.
"""
import json
import logging
import os
import threading
from datetime import datetime, timezone
from typing import Optional

from backend.config import settings

logger = logging.getLogger("competitor_monitor.limits")


class DemoQuota:
    def __init__(self, path: str, max_per_day: int, max_per_ip_day: int) -> None:
        self.path = path
        self.max_per_day = max_per_day
        self.max_per_ip_day = max_per_ip_day
        self._lock = threading.Lock()

    def _today(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def _read(self) -> dict:
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("date") == self._today():
                return data
        except (OSError, ValueError):
            pass
        return {"date": self._today(), "total": 0, "by_ip": {}}

    def try_acquire(self, ip: str) -> Optional[str]:
        """Засчитывает платный вызов. Возвращает текст ошибки, если лимит исчерпан, иначе None."""
        with self._lock:
            data = self._read()
            if self.max_per_day > 0 and data["total"] >= self.max_per_day:
                logger.warning("Суточный лимит демо исчерпан (%s)", self.max_per_day)
                return "Суточный лимит запросов демо исчерпан. Попробуйте завтра."
            used = data["by_ip"].get(ip, 0)
            if self.max_per_ip_day > 0 and used >= self.max_per_ip_day:
                logger.info("Лимит демо на IP исчерпан")
                return f"Лимит демо — {self.max_per_ip_day} анализов в сутки. Попробуйте завтра."
            data["total"] += 1
            data["by_ip"][ip] = used + 1
            try:
                os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
                with open(self.path, "w", encoding="utf-8") as f:
                    json.dump(data, f)
            except OSError:
                logger.exception("Не удалось записать счётчик %s", self.path)
            return None


demo_quota = DemoQuota(settings.usage_file, settings.demo_max_per_day, settings.demo_max_per_ip_day)
