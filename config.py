"""
Конфигурация приложения: темы оформления и настройки шрифтов
"""
THEMES = {
    'classic': {
        'name': 'Голубой',
        'body_bg': '#f0f2f5',
        'container_bg': '#ffffff',
        'header_bg': 'linear-gradient(135deg, #1f77b4 0%, #2c3e50 100%)',
        'sidebar_bg': '#f8f9fa',
        'main_bg': '#ffffff',
        'accent': '#1f77b4',
        'accent2': '#2c3e50',
        'text': '#333',
        'text_light': '#666',
        'border': '#dee2e6',
        'card_bg': '#f8f9fa',
        'plot_bg': '#ffffff',
        'plot_face': '#ffffff',
        'equation_bg': '#f8f9fa'
    },
    'paper': {
        'name': 'Научный журнал',
        'body_bg': '#f5f0e8',
        'container_bg': '#fafaf5',
        'header_bg': 'linear-gradient(135deg, #8b7355 0%, #6b5b45 100%)',
        'sidebar_bg': '#f5f0e8',
        'main_bg': '#fafaf5',
        'accent': '#8b7355',
        'accent2': '#a0522d',
        'text': '#2c1810',
        'text_light': '#5c4033',
        'border': '#d4c5a9',
        'card_bg': '#f5f0e8',
        'plot_bg': '#fafaf5',
        'plot_face': '#f5f0e8',
        'equation_bg': '#fafaf5'
    },
    'neon': {
        'name': 'Розовенький',
        'body_bg': 'linear-gradient(135deg, #ffe4ec 0%, #ffb6c1 50%, #ff69b4 100%)',
        'container_bg': 'rgba(255, 240, 245, 0.95)',
        'header_bg': 'linear-gradient(135deg, #ff69b4 0%, #ff1493 50%, #c71585 100%)',
        'sidebar_bg': 'rgba(255, 228, 241, 0.9)',
        'main_bg': 'rgba(255, 248, 250, 0.95)',
        'accent': '#ff1493',
        'accent2': '#ff69b4',
        'text': '#000000',
        'text_light': '#333333',
        'border': '#ff69b4',
        'card_bg': 'rgba(255, 255, 255, 0.85)',
        'plot_bg': 'rgba(255, 255, 255, 0.9)',
        'plot_face': '#ffffff',
        'equation_bg': 'rgba(255, 240, 245, 0.9)'
    }
}

EQUATION_FONT_SIZE = 35
COEFF_LABEL_FONT_SIZE = 18
SECTION_FONT_SIZE = 20
LABEL_FONT_SIZE = 16
INPUT_FONT_SIZE = 14
LABEL_COLOR = '#999999'