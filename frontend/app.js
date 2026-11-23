/**
 * Competitor Monitor - Frontend Application
 * Мониторинг конкурентов - MVP ассистент
 */

// === Языки интерфейса ===
// Выбор: ?lang=en|ru в адресе → сохраненный выбор → язык браузера → ru.
// Тот же язык уходит в API (?lang=), и модель отвечает на нем.
const I18N = {
    ru: {
        doc_title: 'Мониторинг конкурентов | AI Ассистент',
        nav_text: 'Анализ текста', nav_image: 'Анализ изображений', nav_parse: 'Парсинг сайта', nav_history: 'История',
        status: 'Система активна',
        page_title: 'Мониторинг конкурентов', page_subtitle: 'AI-ассистент для анализа конкурентной среды',
        text_h2: 'Анализ текста конкурента',
        text_sub: 'Вставьте текст с сайта конкурента, из рекламы или описания продукта',
        text_label: 'Текст для анализа',
        text_placeholder: 'Вставьте текст конкурента для анализа...\n\nНапример: описание продукта, текст с лендинга, рекламное объявление...',
        analyze: 'Проанализировать',
        image_sub: 'Загрузите скриншот сайта, баннер или фото упаковки конкурента',
        drop: 'Перетащите изображение или <span>выберите файл</span>',
        image_formats: 'PNG, JPG, GIF, WEBP до 5 МБ',
        parse_h2: 'Парсинг сайта конкурента',
        parse_sub: 'Введите URL сайта для автоматического извлечения и анализа контента',
        parse_label: 'URL сайта', parse_btn: 'Парсить и анализировать',
        history_h2: 'История запросов', history_sub: 'Последние 10 запросов к системе',
        history_empty: 'История пуста', clear: 'Очистить',
        results_h2: 'Результаты анализа', loading: 'Анализирую данные...',
        strengths: 'Сильные стороны', weaknesses: 'Слабые стороны', unique: 'Уникальные предложения',
        recommendations: 'Рекомендации', summary: 'Резюме', image_description: 'Описание изображения',
        visual_score: 'Оценка визуального стиля', insights: 'Маркетинговые инсайты',
        not_found: 'Не найден', first_paragraph: 'Первый абзац:',
        type_text: 'Анализ текста', type_image: 'Анализ изображения', type_parse: 'Парсинг сайта',
        err_short_text: 'Введите текст минимум 10 символов для анализа',
        err_analysis: 'Произошла ошибка при анализе',
        err_image_analysis: 'Произошла ошибка при анализе изображения',
        err_connection: 'Ошибка соединения с сервером',
        err_choose_image: 'Выберите изображение для анализа',
        err_enter_url: 'Введите URL сайта для парсинга',
        err_parse: 'Не удалось распарсить сайт',
        confirm_clear: 'Вы уверены, что хотите очистить историю?',
        locale: 'ru-RU'
    },
    en: {
        doc_title: 'Competitor Monitoring | AI Assistant',
        nav_text: 'Text analysis', nav_image: 'Image analysis', nav_parse: 'Website parsing', nav_history: 'History',
        status: 'System online',
        page_title: 'Competitor monitoring', page_subtitle: 'An AI assistant for analysing your competitors',
        text_h2: 'Competitor text analysis',
        text_sub: 'Paste text from a competitor’s website, an ad or a product description',
        text_label: 'Text to analyse',
        text_placeholder: 'Paste a competitor’s text here...\n\nFor example: a product description, landing page copy, an ad...',
        analyze: 'Analyse',
        image_sub: 'Upload a website screenshot, a banner or a photo of a competitor’s packaging',
        drop: 'Drag an image here or <span>choose a file</span>',
        image_formats: 'PNG, JPG, GIF, WEBP up to 5 MB',
        parse_h2: 'Competitor website parsing',
        parse_sub: 'Enter a website URL to extract and analyse its content automatically',
        parse_label: 'Website URL', parse_btn: 'Parse and analyse',
        history_h2: 'Request history', history_sub: 'The last 10 requests to the system',
        history_empty: 'No history yet', clear: 'Clear',
        results_h2: 'Analysis results', loading: 'Analysing...',
        strengths: 'Strengths', weaknesses: 'Weaknesses', unique: 'Unique offers',
        recommendations: 'Recommendations', summary: 'Summary', image_description: 'Image description',
        visual_score: 'Visual style score', insights: 'Marketing insights',
        not_found: 'Not found', first_paragraph: 'First paragraph:',
        type_text: 'Text analysis', type_image: 'Image analysis', type_parse: 'Website parsing',
        err_short_text: 'Enter at least 10 characters of text to analyse',
        err_analysis: 'Something went wrong during the analysis',
        err_image_analysis: 'Something went wrong while analysing the image',
        err_connection: 'Could not connect to the server',
        err_choose_image: 'Choose an image to analyse',
        err_enter_url: 'Enter a website URL to parse',
        err_parse: 'Could not parse the website',
        confirm_clear: 'Are you sure you want to clear the history?',
        locale: 'en-GB'
    }
};

function detectLang() {
    const fromUrl = new URLSearchParams(location.search).get('lang');
    if (fromUrl === 'ru' || fromUrl === 'en') {
        try { localStorage.setItem('lang', fromUrl); } catch (e) {}
        return fromUrl;
    }
    try {
        const saved = localStorage.getItem('lang');
        if (saved === 'ru' || saved === 'en') return saved;
    } catch (e) {}
    const nav = (navigator.language || 'ru').toLowerCase();
    return /^(ru|uk|be|kk)/.test(nav) ? 'ru' : 'en';
}

let LANG = detectLang();
const t = (key) => (I18N[LANG] && I18N[LANG][key]) || I18N.ru[key] || key;

function applyI18n() {
    document.documentElement.lang = LANG;
    document.title = t('doc_title');
    document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    document.querySelectorAll('[data-i18n-html]').forEach(el => { el.innerHTML = t(el.dataset.i18nHtml); });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === LANG);
        btn.setAttribute('aria-pressed', btn.dataset.lang === LANG ? 'true' : 'false');
    });
}

function setLang(lang) {
    LANG = lang;
    try { localStorage.setItem('lang', lang); } catch (e) {}
    const url = new URL(location.href);
    url.searchParams.set('lang', lang);
    history.replaceState(null, '', url);
    applyI18n();
    ui.hideResults();
    if (state.currentTab === 'history') ui.loadHistory();
}

// === State ===
const state = {
    currentTab: 'text',
    selectedImage: null,
    isLoading: false
};

// === DOM Elements ===
const elements = {
    // Navigation
    navButtons: document.querySelectorAll('.nav-btn'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Text analysis
    competitorText: document.getElementById('competitor-text'),
    analyzeTextBtn: document.getElementById('analyze-text-btn'),
    
    // Image analysis
    uploadZone: document.getElementById('upload-zone'),
    imageInput: document.getElementById('image-input'),
    previewContainer: document.getElementById('preview-container'),
    imagePreview: document.getElementById('image-preview'),
    removeImageBtn: document.getElementById('remove-image'),
    analyzeImageBtn: document.getElementById('analyze-image-btn'),
    
    // Parse demo
    urlInput: document.getElementById('url-input'),
    parseBtn: document.getElementById('parse-btn'),
    
    // History
    historyList: document.getElementById('history-list'),
    clearHistoryBtn: document.getElementById('clear-history-btn'),
    
    // Results
    resultsSection: document.getElementById('results-section'),
    resultsContent: document.getElementById('results-content'),
    closeResultsBtn: document.getElementById('close-results'),
    
    // Loading
    loadingOverlay: document.getElementById('loading-overlay')
};

// === API Functions ===
const api = {
    baseUrl: '',
    
    async analyzeText(text) {
        const response = await fetch(`${this.baseUrl}/analyze_text?lang=${LANG}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        return response.json();
    },
    
    async analyzeImage(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.baseUrl}/analyze_image?lang=${LANG}`, {
            method: 'POST',
            body: formData
        });
        return response.json();
    },
    
    async parseDemo(url) {
        const response = await fetch(`${this.baseUrl}/parse_demo?lang=${LANG}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        return response.json();
    },
    
    async getHistory() {
        const response = await fetch(`${this.baseUrl}/history`);
        return response.json();
    },
    
    async clearHistory() {
        const response = await fetch(`${this.baseUrl}/history`, {
            method: 'DELETE'
        });
        return response.json();
    }
};

// === UI Functions ===
const ui = {
    showLoading() {
        state.isLoading = true;
        elements.loadingOverlay.style.display = 'flex';
    },
    
    hideLoading() {
        state.isLoading = false;
        elements.loadingOverlay.style.display = 'none';
    },
    
    showTab(tabId) {
        state.currentTab = tabId;
        
        // Update navigation
        elements.navButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });
        
        // Update content
        elements.tabContents.forEach(content => {
            content.classList.toggle('active', content.id === `${tabId}-tab`);
        });
        
        // Load history if needed
        if (tabId === 'history') {
            this.loadHistory();
        }
    },
    
    showResults(html) {
        elements.resultsContent.innerHTML = html;
        elements.resultsSection.hidden = false;
        elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
    },
    
    hideResults() {
        elements.resultsSection.hidden = true;
    },
    
    showError(message) {
        const html = `
            <div class="error-message">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                <span>${message}</span>
            </div>
        `;
        this.showResults(html);
    },
    
    renderTextAnalysis(analysis) {
        return `
            ${this.renderResultBlock(t('strengths'), analysis.strengths, 'strengths')}
            ${this.renderResultBlock(t('weaknesses'), analysis.weaknesses, 'weaknesses')}
            ${this.renderResultBlock(t('unique'), analysis.unique_offers, 'unique')}
            ${this.renderResultBlock(t('recommendations'), analysis.recommendations, 'recommendations')}
            ${analysis.summary ? `
                <div class="result-block result-summary">
                    <h3>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                        </svg>
                        ${t('summary')}
                    </h3>
                    <p>${analysis.summary}</p>
                </div>
            ` : ''}
        `;
    },
    
    renderImageAnalysis(analysis) {
        const scorePercent = (analysis.visual_style_score / 10) * 100;
        
        return `
            <div class="result-block">
                <h3>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    ${t('image_description')}
                </h3>
                <p>${analysis.description}</p>
            </div>
            
            <div class="result-block">
                <h3>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
                    </svg>
                    ${t('visual_score')}
                </h3>
                <div class="score-display">
                    <span class="score-value">${analysis.visual_style_score}/10</span>
                    <div class="score-bar">
                        <div class="score-fill" style="width: ${scorePercent}%"></div>
                    </div>
                </div>
                <p>${analysis.visual_style_analysis}</p>
            </div>
            
            ${this.renderResultBlock(t('insights'), analysis.marketing_insights, 'insights')}
            ${this.renderResultBlock(t('recommendations'), analysis.recommendations, 'recommendations')}
        `;
    },
    
    renderParsedContent(data) {
        const parsed = data;
        
        return `
            <div class="parsed-content">
                <div class="label">URL:</div>
                <div class="value">${parsed.url}</div>
                
                <div class="label">Title:</div>
                <div class="value">${parsed.title || t('not_found')}</div>
                
                <div class="label">H1:</div>
                <div class="value">${parsed.h1 || t('not_found')}</div>
                
                <div class="label">${t('first_paragraph')}</div>
                <div class="value">${parsed.first_paragraph || t('not_found')}</div>
            </div>
            
            ${parsed.analysis ? this.renderTextAnalysis(parsed.analysis) : ''}
        `;
    },
    
    renderResultBlock(title, items, type) {
        if (!items || items.length === 0) return '';
        
        const icons = {
            strengths: '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
            weaknesses: '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>',
            unique: '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
            recommendations: '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
            insights: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>'
        };
        
        return `
            <div class="result-block">
                <h3>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        ${icons[type] || icons.recommendations}
                    </svg>
                    ${title}
                </h3>
                <ul>
                    ${items.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
        `;
    },
    
    async loadHistory() {
        try {
            const data = await api.getHistory();
            this.renderHistory(data.items);
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    },
    
    renderHistory(items) {
        if (!items || items.length === 0) {
            elements.historyList.innerHTML = `
                <div class="history-empty">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    <p>${t('history_empty')}</p>
                </div>
            `;
            return;
        }
        
        const icons = {
            text: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
            image: '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>',
            parse: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
        };
        
        const typeLabels = {
            text: t('type_text'),
            image: t('type_image'),
            parse: t('type_parse')
        };
        
        elements.historyList.innerHTML = items.map(item => {
            const date = new Date(item.timestamp);
            const timeStr = date.toLocaleString(t('locale'), {
                day: '2-digit',
                month: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            return `
                <div class="history-item">
                    <div class="history-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            ${icons[item.request_type] || icons.text}
                        </svg>
                    </div>
                    <div class="history-content">
                        <div class="history-type">${typeLabels[item.request_type] || item.request_type}</div>
                        <div class="history-summary">${item.request_summary}</div>
                    </div>
                    <div class="history-time">${timeStr}</div>
                </div>
            `;
        }).join('');
    }
};

// === Event Handlers ===
const handlers = {
    // Navigation
    handleNavClick(e) {
        const btn = e.target.closest('.nav-btn');
        if (btn) {
            ui.showTab(btn.dataset.tab);
        }
    },
    
    // Text analysis
    async handleAnalyzeText() {
        const text = elements.competitorText.value.trim();
        
        if (text.length < 10) {
            ui.showError(t('err_short_text'));
            return;
        }
        
        ui.showLoading();
        
        try {
            const result = await api.analyzeText(text);
            
            if (result.success && result.analysis) {
                ui.showResults(ui.renderTextAnalysis(result.analysis));
            } else {
                ui.showError(result.error || t('err_analysis'));
            }
        } catch (error) {
            ui.showError(t('err_connection'));
            console.error(error);
        } finally {
            ui.hideLoading();
        }
    },
    
    // Image upload
    handleUploadClick() {
        elements.imageInput.click();
    },
    
    handleImageSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processImage(file);
        }
    },
    
    handleDragOver(e) {
        e.preventDefault();
        elements.uploadZone.classList.add('dragover');
    },
    
    handleDragLeave(e) {
        e.preventDefault();
        elements.uploadZone.classList.remove('dragover');
    },
    
    handleDrop(e) {
        e.preventDefault();
        elements.uploadZone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            this.processImage(file);
        }
    },
    
    processImage(file) {
        state.selectedImage = file;
        
        const reader = new FileReader();
        reader.onload = (e) => {
            elements.imagePreview.src = e.target.result;
            elements.previewContainer.hidden = false;
            elements.uploadZone.querySelector('.upload-content').hidden = true;
            elements.analyzeImageBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    },
    
    handleRemoveImage() {
        state.selectedImage = null;
        elements.imageInput.value = '';
        elements.imagePreview.src = '';
        elements.previewContainer.hidden = true;
        elements.uploadZone.querySelector('.upload-content').hidden = false;
        elements.analyzeImageBtn.disabled = true;
    },
    
    async handleAnalyzeImage() {
        if (!state.selectedImage) {
            ui.showError(t('err_choose_image'));
            return;
        }
        
        ui.showLoading();
        
        try {
            const result = await api.analyzeImage(state.selectedImage);
            
            if (result.success && result.analysis) {
                ui.showResults(ui.renderImageAnalysis(result.analysis));
            } else {
                ui.showError(result.error || t('err_image_analysis'));
            }
        } catch (error) {
            ui.showError(t('err_connection'));
            console.error(error);
        } finally {
            ui.hideLoading();
        }
    },
    
    // Parse demo
    async handleParse() {
        let url = elements.urlInput.value.trim();
        
        if (!url) {
            ui.showError(t('err_enter_url'));
            return;
        }
        
        // Add protocol if missing
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        
        ui.showLoading();
        
        try {
            const result = await api.parseDemo(url);
            
            if (result.success && result.data) {
                ui.showResults(ui.renderParsedContent(result.data));
            } else {
                ui.showError(result.error || t('err_parse'));
            }
        } catch (error) {
            ui.showError(t('err_connection'));
            console.error(error);
        } finally {
            ui.hideLoading();
        }
    },
    
    // History
    async handleClearHistory() {
        if (!confirm(t('confirm_clear'))) {
            return;
        }
        
        try {
            await api.clearHistory();
            ui.renderHistory([]);
        } catch (error) {
            console.error('Failed to clear history:', error);
        }
    },
    
    // Results
    handleCloseResults() {
        ui.hideResults();
    }
};

// === Initialize ===
function init() {
    applyI18n();
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => setLang(btn.dataset.lang));
    });

    // Navigation
    elements.navButtons.forEach(btn => {
        btn.addEventListener('click', handlers.handleNavClick.bind(handlers));
    });
    
    // Text analysis
    elements.analyzeTextBtn.addEventListener('click', handlers.handleAnalyzeText.bind(handlers));
    
    // Image upload
    elements.uploadZone.addEventListener('click', handlers.handleUploadClick.bind(handlers));
    elements.imageInput.addEventListener('change', handlers.handleImageSelect.bind(handlers));
    elements.uploadZone.addEventListener('dragover', handlers.handleDragOver.bind(handlers));
    elements.uploadZone.addEventListener('dragleave', handlers.handleDragLeave.bind(handlers));
    elements.uploadZone.addEventListener('drop', handlers.handleDrop.bind(handlers));
    elements.removeImageBtn.addEventListener('click', handlers.handleRemoveImage.bind(handlers));
    elements.analyzeImageBtn.addEventListener('click', handlers.handleAnalyzeImage.bind(handlers));
    
    // Parse demo
    elements.parseBtn.addEventListener('click', handlers.handleParse.bind(handlers));
    elements.urlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handlers.handleParse.call(handlers);
    });
    
    // History
    elements.clearHistoryBtn.addEventListener('click', handlers.handleClearHistory.bind(handlers));
    
    // Results
    elements.closeResultsBtn.addEventListener('click', handlers.handleCloseResults.bind(handlers));
    
    // Show default tab
    ui.showTab('text');
}

// Start app
document.addEventListener('DOMContentLoaded', init);

