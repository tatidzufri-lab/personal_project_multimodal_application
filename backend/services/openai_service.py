"""
Сервис для работы с ProxyAPI (OpenAI-совместимый API)
https://proxyapi.ru/docs/openai-text-generation
"""
import base64
import json
import re
import time
import logging
from typing import Optional

from openai import OpenAI

from backend.config import settings
from backend.models.schemas import CompetitorAnalysis, ImageAnalysis

# Логгер для сервиса
logger = logging.getLogger("competitor_monitor.openai")


# Промпты остаются русскими; для английского меняется только язык ответа.
# Так обе версии анализа держатся одних и тех же правил и не расходятся при правках.
_LANG_RULE_EN = (
    "\n\nLANGUAGE: write every string value in the JSON in English, in plain, clear sentences. "
    "Keep the JSON keys exactly as above."
)


def with_language(system_prompt: str, lang: str) -> str:
    if lang != "en":
        return system_prompt
    return system_prompt.replace("- Пиши на русском языке", "- Пиши на английском языке") + _LANG_RULE_EN


class OpenAIService:
    """Сервис для анализа через ProxyAPI"""
    
    def __init__(self):
        logger.info("=" * 50)
        logger.info("Инициализация OpenAI сервиса")
        logger.info(f"  Base URL: {settings.proxy_api_base_url}")
        logger.info(f"  Модель текста: {settings.openai_model}")
        logger.info(f"  Модель vision: {settings.openai_vision_model}")
        logger.info(f"  API ключ: {'*' * 10}...{settings.proxy_api_key[-4:] if settings.proxy_api_key else 'НЕ ЗАДАН'}")
        
        # ProxyAPI - OpenAI-совместимый API для России
        self.client = OpenAI(
            api_key=settings.proxy_api_key,
            base_url=settings.proxy_api_base_url
        )
        self.model = settings.openai_model
        self.vision_model = settings.openai_vision_model
        
        logger.info("OpenAI сервис инициализирован успешно ✓")
        logger.info("=" * 50)
    
    def _parse_json_response(self, content: str) -> dict:
        """Извлечь JSON из ответа модели"""
        logger.debug(f"Парсинг JSON ответа, длина: {len(content)} символов")
        
        # Пробуем найти JSON в markdown блоке
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
        if json_match:
            content = json_match.group(1)
            logger.debug("JSON найден в markdown блоке")
        
        # Пробуем найти JSON объект
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            content = json_match.group(0)
            logger.debug("JSON объект извлечён")
        
        try:
            result = json.loads(content)
            logger.debug(f"JSON успешно распарсен, ключей: {len(result)}")
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"Ошибка парсинга JSON: {e}")
            logger.debug(f"Проблемный контент: {content[:200]}...")
            return {}
    
    async def analyze_text(self, text: str, lang: str = "ru") -> CompetitorAnalysis:
        """Анализ текста конкурента"""
        logger.info("=" * 50)
        logger.info("📝 АНАЛИЗ ТЕКСТА КОНКУРЕНТА")
        logger.info(f"  Длина текста: {len(text)} символов")
        logger.info(f"  Превью: {text[:100]}...")
        logger.info(f"  Модель: {self.model}")
        
        system_prompt = """Ты — эксперт по конкурентному анализу в сфере ретритов в горах. Проанализируй предоставленный контент конкурента (текст/описание/лендинг/пост) и верни структурированный JSON-ответ. Если часть данных отсутствует, делай выводы на основе доступной информации и здравого смысла, без выдумывания фактов — используй формулировки «вероятно», «похоже», «не указано».


Формат ответа (строго JSON):
{
    "strengths": ["сильная сторона 1", "сильная сторона 2", ...],
    "weaknesses": ["слабая сторона 1", "слабая сторона 2", ...],
    "unique_offers": ["уникальное предложение 1", "уникальное предложение 2", ...],
    "recommendations": ["рекомендация 1", "рекомендация 2", ...],
    "design_score": 0,
    "animation_potential": {
        "score": 0,
        "ideas": ["идея анимации 1", "идея анимации 2", ...],
        "notes": "Короткие пояснения: где и зачем анимация уместна (лендинг/соцсети), что она усиливает (доверие/атмосферу/конверсию), и каких ошибок избегать"
    },
    "summary": "Краткое резюме анализа"
}


Правила заполнения:
- Каждый массив должен содержать 3-5 пунктов
- Пиши на русском языке
- Будь конкретен и практичен в рекомендациях
- design_score: целое число от 0 до 10 — оценка визуального стиля (чистота, читабельность, типографика, качество фото/видео, цельность айдентики, соответствие атмосфере горного ретрита)
- animation_potential.score: целое число от 0 до 10 — потенциал анимации/моушена для усиления впечатления и конверсии в нише горного ретрита
- animation_potential.ideas: 3-5 конкретных идей анимации под «ретрит в горах» (например: мягкие переходы, параллакс гор, «дыхание» UI, анимация маршрута/дня, micro-interactions в форме бронирования, короткие лупы тумана/облаков)
- Не добавляй никакого текста вне JSON. Возвращай только валидный JSON без комментариев и без Markdown."""


        start_time = time.time()
        logger.info("  Отправка запроса к API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": with_language(system_prompt, lang)},
                    {"role": "user", "content": f"Проанализируй текст конкурента:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            logger.debug(f"  Использовано токенов: {response.usage.total_tokens if response.usage else 'N/A'}")
            
            data = self._parse_json_response(content)
            
            result = CompetitorAnalysis(
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                unique_offers=data.get("unique_offers", []),
                recommendations=data.get("recommendations", []),
                summary=data.get("summary", "")
            )
            
            logger.info(f"  Результат: {len(result.strengths)} сильных, {len(result.weaknesses)} слабых сторон")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise
    
    async def analyze_image(self, image_base64: str, mime_type: str = "image/jpeg", lang: str = "ru") -> ImageAnalysis:
        """Анализ изображения (баннер, сайт, упаковка)"""
        logger.info("=" * 50)
        logger.info("🖼️ АНАЛИЗ ИЗОБРАЖЕНИЯ")
        logger.info(f"  Размер base64: {len(image_base64)} символов")
        logger.info(f"  MIME тип: {mime_type}")
        logger.info(f"  Модель: {self.vision_model}")
        
        system_prompt = """Ты — эксперт по визуальному маркетингу и дизайну в сфере ретритов в горах. Проанализируй изображение конкурента (баннер, сайт, упаковка, креатив для соцсетей и т.д.) и верни структурированный JSON-ответ. Если каких-то деталей не видно или качество низкое, отмечай это явно и не выдумывай факты (используй «не видно», «не читается», «похоже»).


Формат ответа (строго JSON):
{
    "description": "Детальное описание того, что изображено",
    "marketing_insights": ["инсайт 1", "инсайт 2", ...],
    "visual_style_score": 0,
    "visual_style_analysis": "Анализ визуального стиля конкурента",
    "design_score": 0,
    "animation_potential": {
        "score": 0,
        "ideas": ["идея анимации 1", "идея анимации 2", ...],
        "notes": "Короткие пояснения: где и зачем анимация уместна (лендинг/соцсети), что она усиливает (атмосферу/доверие/конверсию), и каких ошибок избегать"
    },
    "recommendations": ["рекомендация 1", "рекомендация 2", ...]
}


Правила заполнения:
- visual_style_score: целое число от 0 до 10 — оценка визуала по параметрам (цветовая палитра, типографика, композиция, качество фото/видео, UX/UI элементы)
- design_score: целое число от 0 до 10 — оценка визуального стиля именно под нишу «ретрит в горах» (атмосфера природы, ощущение спокойствия/безопасности, премиальность или доступность, цельность айдентики, соответствие ожиданиям аудитории)
- animation_potential.score: целое число от 0 до 10 — потенциал добавления анимации/моушена для усиления впечатления и конверсии
- Каждый массив должен содержать 3-5 пунктов
- marketing_insights: 3-5 практичных маркетинговых наблюдений (что продают, кому, через какие триггеры: природа, перезагрузка, экспертность ведущих, комьюнити, безопасность, программа, размещение, трансфер)
- animation_potential.ideas: 3-5 конкретных идей анимации под «ретрит в горах» (например: мягкие переходы, параллакс гор/облаков, «дыхание» UI, анимация маршрута/дня, micro-interactions в форме бронирования, короткие лупы тумана/снега/костра)
- recommendations: 3-5 конкретных улучшений для повышения ясности оффера и конверсии (CTA, иерархия, доверие, цены/даты, структура блоков, читабельность)
- Не добавляй никакого текста вне JSON. Возвращай только валидный JSON без комментариев и без Markdown."""


        start_time = time.time()
        logger.info("  Отправка запроса к Vision API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {"role": "system", "content": with_language(system_prompt, lang)},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Проанализируй это изображение конкурента с точки зрения маркетинга и дизайна:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            
            data = self._parse_json_response(content)
            
            result = ImageAnalysis(
                description=data.get("description", ""),
                marketing_insights=data.get("marketing_insights", []),
                visual_style_score=data.get("visual_style_score", 5),
                visual_style_analysis=data.get("visual_style_analysis", ""),
                recommendations=data.get("recommendations", [])
            )
            
            logger.info(f"  Результат: оценка стиля {result.visual_style_score}/10")
            logger.info(f"  Инсайтов: {len(result.marketing_insights)}, рекомендаций: {len(result.recommendations)}")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка Vision API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise
    
    async def analyze_parsed_content(
        self, 
        title: Optional[str], 
        h1: Optional[str], 
        paragraph: Optional[str],
        lang: str = "ru",
    ) -> CompetitorAnalysis:
        """Анализ распарсенного контента сайта"""
        logger.info("📄 Анализ распарсенного контента")
        logger.info(f"  Title: {title[:50] if title else 'N/A'}...")
        logger.info(f"  H1: {h1[:50] if h1 else 'N/A'}...")
        logger.info(f"  Абзац: {paragraph[:50] if paragraph else 'N/A'}...")
        
        content_parts = []
        if title:
            content_parts.append(f"Заголовок страницы (title): {title}")
        if h1:
            content_parts.append(f"Главный заголовок (H1): {h1}")
        if paragraph:
            content_parts.append(f"Первый абзац: {paragraph}")
        
        combined_text = "\n\n".join(content_parts)
        
        if not combined_text.strip():
            logger.warning("  ⚠ Контент пустой, возвращаем пустой анализ")
            return CompetitorAnalysis(
                summary="Could not extract any content to analyse" if lang == "en"
                else "Не удалось извлечь контент для анализа"
            )
        
        return await self.analyze_text(combined_text, lang=lang)
    
    async def analyze_website_screenshot(
        self,
        screenshot_base64: str,
        url: str,
        title: Optional[str] = None,
        h1: Optional[str] = None,
        first_paragraph: Optional[str] = None,
        lang: str = "ru",
    ) -> CompetitorAnalysis:
        """Комплексный анализ сайта конкурента по скриншоту"""
        logger.info("=" * 50)
        logger.info("🌐 КОМПЛЕКСНЫЙ АНАЛИЗ САЙТА")
        logger.info(f"  URL: {url}")
        logger.info(f"  Title: {title[:50] if title else 'N/A'}...")
        logger.info(f"  H1: {h1[:50] if h1 else 'N/A'}...")
        logger.info(f"  Размер скриншота: {len(screenshot_base64)} символов base64")
        logger.info(f"  Модель: {self.vision_model}")
        
        # Формируем контекст из извлечённых данных
        context_parts = [f"URL сайта: {url}"]
        if title:
            context_parts.append(f"Title страницы: {title}")
        if h1:
            context_parts.append(f"Главный заголовок (H1): {h1}")
        if first_paragraph:
            context_parts.append(f"Текст на странице: {first_paragraph[:300]}")
        
        context = "\n".join(context_parts)
        logger.debug(f"  Контекст:\n{context}")
        
        system_prompt = """Ты — эксперт по конкурентному анализу и UX/UI дизайну в сфере ретритов в горах. Проанализируй скриншот сайта конкурента и верни структурированный JSON-ответ. Если часть элементов на скриншоте не видна/не читается, отмечай это явно и не выдумывай факты (используй «не видно», «не читается», «вероятно»).


Формат ответа (строго JSON):
{
    "strengths": ["сильная сторона 1", "сильная сторона 2", ...],
    "weaknesses": ["слабая сторона 1", "слабая сторона 2", ...],
    "unique_offers": ["уникальное предложение/фича 1", "уникальное предложение/фича 2", ...],
    "recommendations": ["рекомендация 1", "рекомендация 2", ...],
    "design_score": 0,
    "animation_potential": {
        "score": 0,
        "ideas": ["идея анимации 1", "идея анимации 2", ...],
        "notes": "Короткие пояснения: где и зачем анимация уместна (hero/блоки программы/форма брони/сторис), что она усиливает (атмосферу горного ретрита/доверие/конверсию), и каких ошибок избегать"
    },
    "summary": "Комплексное резюме анализа сайта конкурента"
}


При анализе обращай внимание на:
- Дизайн и визуальный стиль (цвета, шрифты, композиция, фото/видео, цельность айдентики)
- UX/UI: навигация, расположение элементов, заметность CTA, формы/поля, скорость восприятия
- Контент: заголовки, тексты, тональность, призывы к действию, ясность оффера
- Уникальные торговые предложения (УТП) и фичи (программа, ведущие, проживание, трансфер, безопасность, комьюнити)
- Целевая аудитория: кому адресовано, уровень «премиум/доступно», ожидания и триггеры
- Технологичность и современность дизайна (адаптив, доверительные элементы, логика лендинга)


Правила заполнения:
- Каждый массив должен содержать 4-6 конкретных пунктов
- Пиши на русском языке
- Будь конкретен и практичен
- Давай actionable рекомендации (что именно поменять, где именно, и ожидаемый эффект)
- design_score: целое число от 0 до 10 — оценка визуального стиля под нишу «ретрит в горах» (атмосфера природы и спокойствия, ощущение безопасности, читабельность, качество визуала, цельность)
- animation_potential.score: целое число от 0 до 10 — потенциал анимации/моушена для усиления впечатления и конверсии
- animation_potential.ideas: 4-6 идей анимации, релевантных горному ретриту (например: мягкий параллакс гор/облаков в hero, деликатные появления блоков программы по скроллу, анимация маршрута/дня ретрита, micro-interactions в календаре дат и форме бронирования, лупы тумана/костра/снега, «прогресс» заполнения заявки)
- Не добавляй никакого текста вне JSON. Возвращай только валидный JSON без комментариев и без Markdown."""


        start_time = time.time()
        logger.info("  Отправка скриншота в Vision API...")
        
        try:
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {"role": "system", "content": with_language(system_prompt, lang)},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Проведи комплексный конкурентный анализ этого сайта:\n\n{context}"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{screenshot_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )
            
            elapsed = time.time() - start_time
            logger.info(f"  ✓ Ответ получен за {elapsed:.2f} сек")
            
            content = response.choices[0].message.content
            logger.info(f"  Длина ответа: {len(content)} символов")
            
            data = self._parse_json_response(content)
            
            result = CompetitorAnalysis(
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                unique_offers=data.get("unique_offers", []),
                recommendations=data.get("recommendations", []),
                summary=data.get("summary", "")
            )
            
            logger.info(f"  Результат:")
            logger.info(f"    - Сильных сторон: {len(result.strengths)}")
            logger.info(f"    - Слабых сторон: {len(result.weaknesses)}")
            logger.info(f"    - УТП: {len(result.unique_offers)}")
            logger.info(f"    - Рекомендаций: {len(result.recommendations)}")
            logger.info(f"  Резюме: {result.summary[:100]}...")
            logger.info("=" * 50)
            
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"  ✗ Ошибка Vision API за {elapsed:.2f} сек: {e}")
            logger.error("=" * 50)
            raise


# Глобальный экземпляр
logger.info("Создание глобального экземпляра OpenAI сервиса...")
openai_service = OpenAIService()
