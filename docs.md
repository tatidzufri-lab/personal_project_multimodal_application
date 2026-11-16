# API CompetitorAI

Описание сервера, к которому обращаются веб-интерфейс и десктоп-приложение. После запуска интерактивная документация доступна на `http://localhost:8000/docs` (Swagger) и `http://localhost:8000/redoc`.

## Содержание

1. [Эндпоинты](#эндпоинты)
2. [Примеры запросов](#примеры-запросов)
3. [Что принимает анализ](#что-принимает-анализ)
4. [Модели данных](#модели-данных)
5. [Коды ответов](#коды-ответов)
6. [Настройки](#настройки)

## Эндпоинты

Базовый адрес: `http://localhost:8000`.

| Метод | Путь | Что делает |
|---|---|---|
| GET | `/` | Веб-интерфейс |
| POST | `/analyze_text` | Анализ текста конкурента |
| POST | `/analyze_image` | Анализ изображения |
| POST | `/parse_demo` | Анализ сайта по ссылке |
| GET | `/history` | Последние запросы |
| DELETE | `/history` | Очистить историю |
| GET | `/health` | Проверка, что сервер работает |
| GET | `/docs`, `/redoc` | Документация API |

## Примеры запросов

### Анализ текста: `POST /analyze_text`

```bash
curl -X POST "http://localhost:8000/analyze_text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Наша компания предлагает решения для бизнеса. Мы работаем на рынке 10 лет и обслуживаем более 1000 клиентов. Быстрая доставка, гарантия качества, индивидуальный подход."}'
```

```json
{
  "success": true,
  "analysis": {
    "strengths": ["Долгий опыт работы на рынке (10 лет)", "Большая клиентская база (1000+ клиентов)"],
    "weaknesses": ["Нет конкретных цен", "Общие формулировки без специфики"],
    "unique_offers": ["Индивидуальный подход к каждому клиенту", "Гарантия качества"],
    "recommendations": ["Добавить цифры и кейсы", "Включить отзывы клиентов"],
    "summary": "Компания делает ставку на опыт, но текст нужно конкретизировать, чтобы он лучше продавал."
  },
  "error": null
}
```

### Анализ изображения: `POST /analyze_image`

```bash
curl -X POST "http://localhost:8000/analyze_image" -F "file=@banner.jpg"
```

```json
{
  "success": true,
  "analysis": {
    "description": "Рекламный баннер с продуктом на синем градиентном фоне, крупный белый заголовок, оранжевая кнопка.",
    "marketing_insights": ["Четкая визуальная иерархия", "Контрастная кнопка сразу заметна"],
    "visual_style_score": 7,
    "visual_style_analysis": "Современный корпоративный стиль, типографика читается, отступы можно улучшить.",
    "recommendations": ["Добавить отзывы или рейтинг", "Увеличить кнопку"]
  },
  "error": null
}
```

### Анализ сайта: `POST /parse_demo`

```bash
curl -X POST "http://localhost:8000/parse_demo" \
  -H "Content-Type: application/json" \
  -d '{"url": "example.com"}'
```

```json
{
  "success": true,
  "data": {
    "url": "https://example.com",
    "title": "Example Domain",
    "h1": "Example Domain",
    "first_paragraph": "This domain is for use in illustrative examples in documents.",
    "analysis": {
      "strengths": ["..."],
      "weaknesses": ["..."],
      "unique_offers": ["..."],
      "recommendations": ["..."],
      "summary": "..."
    },
    "error": null
  },
  "error": null
}
```

### История: `GET /history` и `DELETE /history`

```bash
curl "http://localhost:8000/history"
```

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "timestamp": "2024-01-15T10:30:00",
      "request_type": "text",
      "request_summary": "Наша компания предлагает решения для бизнеса...",
      "response_summary": "Компания делает ставку на опыт..."
    }
  ],
  "total": 1
}
```

```bash
curl -X DELETE "http://localhost:8000/history"
# {"success": true, "message": "История очищена"}
```

### Проверка сервера: `GET /health`

```bash
curl "http://localhost:8000/health"
# {"status": "healthy", "service": "Competitor Monitor", "version": "1.0.0"}
```

## Что принимает анализ

**Текст.** Любой текст конкурента от 10 символов: описание продукта, текст лендинга, рекламное объявление, пост, рассылка.

**Изображения.** JPEG, PNG, GIF и WebP: баннеры, скриншоты сайтов, фото упаковки, креативы для соцсетей. Другие типы файлов сервер отклоняет с кодом 400.

**Сайт.** Если в ссылке нет протокола, сервер добавляет `https://`. Страница открывается в headless Chrome через Selenium, на загрузку дается 10 секунд. Сервер забирает заголовок `<title>`, первый `<h1>` и первый абзац длиннее 50 символов (до 500 символов), снимает скриншот страницы и отдает модели скриншот вместе с текстом.

## Модели данных

```typescript
// Запросы
TextAnalysisRequest { text: string }          // от 10 символов
ParseDemoRequest    { url: string }

// Анализ текста и сайта
CompetitorAnalysis {
  strengths: string[]        // сильные стороны
  weaknesses: string[]       // слабые стороны
  unique_offers: string[]    // уникальные предложения
  recommendations: string[]  // рекомендации
  summary: string            // короткое резюме
}

// Анализ изображения
ImageAnalysis {
  description: string           // что на изображении
  marketing_insights: string[]  // маркетинговые наблюдения
  visual_style_score: number    // оценка от 0 до 10
  visual_style_analysis: string // разбор стиля
  recommendations: string[]     // рекомендации
}

// Запись истории
HistoryItem {
  id: string                // UUID
  timestamp: datetime
  request_type: string      // "text" | "image" | "parse"
  request_summary: string   // кратко о запросе
  response_summary: string  // кратко об ответе
}
```

Все ответы анализа обернуты в `{ success, analysis | data, error }`. Если что-то пошло не так, `success` равен `false`, а причина лежит в `error`.

## Коды ответов

| Код | Когда |
|---|---|
| 200 | Запрос выполнен |
| 400 | Неподдерживаемый тип файла или некорректный запрос |
| 422 | Данные не прошли проверку, например текст короче 10 символов |
| 500 | Внутренняя ошибка сервера |

## Настройки

Переменные окружения в `.env` (образец в `env.example.txt`):

| Переменная | Что задает | По умолчанию |
|---|---|---|
| `PROXY_API_KEY` | Ключ [ProxyAPI](https://proxyapi.ru/) | нет |
| `OPENAI_MODEL` | Модель для текста | `gpt-4o-mini` |
| `OPENAI_VISION_MODEL` | Модель для изображений | `gpt-4o-mini` |
| `HISTORY_FILE` | Файл истории | `history.json`, в Docker `/app/data/history.json` |

Хост и порт сервера (`0.0.0.0:8000`) заданы в `backend/config.py`. Переменные `API_HOST` и `API_PORT` из `env.example.txt` сервер пока не читает.

[ProxyAPI](https://proxyapi.ru/docs/openai-text-generation) дает OpenAI-совместимый доступ из России без VPN и с оплатой в рублях.

История хранит последние 10 запросов в JSON.

## Безопасность

- Ключи держите в `.env`, он уже в `.gitignore`. В коде ключей быть не должно.
- В рабочей среде включите HTTPS и ограничьте CORS своими доменами.
