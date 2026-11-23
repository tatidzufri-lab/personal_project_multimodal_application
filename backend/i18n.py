"""Английские версии сообщений API.

Сервисы возвращают ошибки по-русски, как и раньше. Если запрос пришел с ?lang=en,
main.py пропускает текст через to_lang(): известные сообщения переводятся,
неизвестные (например, текст ошибки провайдера) остаются как есть.
"""
import re
from typing import Optional

LANGS = ("ru", "en")

_EXACT = {
    "Суточный лимит запросов демо исчерпан. Попробуйте завтра.":
        "The demo's daily request limit is used up. Please try again tomorrow.",
    "Поддерживаются только адреса http и https": "Only http and https addresses are supported",
    "Не указан адрес сайта": "No website address given",
    "Некорректный порт в адресе": "Invalid port in the address",
    "Поддерживаются только стандартные порты 80 и 443": "Only the standard ports 80 and 443 are supported",
    "Не удалось найти сайт по указанному адресу": "Could not find a website at this address",
    "Этот адрес недоступен для анализа: разрешены только публичные сайты":
        "This address can't be analysed: only public websites are allowed",
    "Превышено время ожидания загрузки страницы": "The page took too long to load",
    "Соединение отклонено сервером": "The server refused the connection",
    "Превышено время ожидания соединения": "The connection timed out",
    "Не удалось извлечь контент для анализа": "Could not extract any content to analyse",
}

_PATTERNS = [
    (re.compile(r"^Лимит демо — (\d+) анализов в сутки\. Попробуйте завтра\.$"),
     r"The demo allows \1 analyses per day. Please try again tomorrow."),
    (re.compile(r"^Текст слишком длинный: (\d+) символов, в демо можно до (\d+)$"),
     r"The text is too long: \1 characters, the demo allows up to \2"),
    (re.compile(r"^Файл слишком большой: в демо можно до (\d+) МБ$"),
     r"The file is too large: the demo allows up to \1 MB"),
    (re.compile(r"^Неподдерживаемый тип файла\. Разрешены: (.*)$"),
     r"Unsupported file type. Allowed: \1"),
    (re.compile(r"^Ошибка браузера: (.*)$", re.S), r"Browser error: \1"),
    (re.compile(r"^Ошибка при загрузке страницы: (.*)$", re.S), r"Error while loading the page: \1"),
]


def normalize_lang(value: Optional[str]) -> str:
    return value if value in LANGS else "ru"


def to_lang(message: Optional[str], lang: str) -> Optional[str]:
    if lang != "en" or not message:
        return message
    if message in _EXACT:
        return _EXACT[message]
    for rx, repl in _PATTERNS:
        if rx.match(message):
            return rx.sub(repl, message)
    return message
