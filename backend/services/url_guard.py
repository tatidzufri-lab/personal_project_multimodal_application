"""Проверка адреса для парсинга: только публичные http(s)-сайты.

Без неё посетитель демо мог заставить Chromium на сервере открыть внутренние адреса:
сервис метаданных облака (169.254.169.254), localhost, частные сети Docker.
"""
import ipaddress
import socket
from typing import Optional
from urllib.parse import urlsplit

# Шаблоны для Chrome DevTools (Network.setBlockedURLs): режут и вложенные запросы страницы
# (iframe, картинки) на IP-литералы частных сетей. Имена, которые резолвятся во внутренние
# адреса, ловит проверка ниже до загрузки и после редиректов.
BLOCKED_URL_PATTERNS = [
    "*://169.254.*", "*://127.*", "*://localhost*", "*://0.*", "*://10.*",
    "*://192.168.*", "*://[::1]*", "*://[fd*", "*://[fe80*",
] + [f"*://172.{i}.*" for i in range(16, 32)]


def _is_public(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)
    return addr.is_global and not addr.is_multicast


def check_public_url(url: str) -> Optional[str]:
    """Возвращает текст ошибки, если адрес не публичный, иначе None."""
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https"):
        return "Поддерживаются только адреса http и https"
    host = parts.hostname
    if not host:
        return "Не указан адрес сайта"
    try:
        port = parts.port
    except ValueError:
        return "Некорректный порт в адресе"
    if port not in (None, 80, 443):
        return "Поддерживаются только стандартные порты 80 и 443"
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return "Не удалось найти сайт по указанному адресу"
    for info in infos:
        if not _is_public(info[4][0]):
            return "Этот адрес недоступен для анализа: разрешены только публичные сайты"
    return None
