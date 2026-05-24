"""
HTML шаблон для веб-интерфейса
"""

HTML_TEMPLATE = r'''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Обобщённое уравнение Клейна-Гордона с диссипацией</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script" async></script>
    <style>
        :root {
            --body-bg: {{ theme.body_bg }};
            --container-bg: {{ theme.container_bg }};
            --header-bg: {{ theme.header_bg }};
            --sidebar-bg: {{ theme.sidebar_bg }};
            --main-bg: {{ theme.main_bg }};
            --accent: {{ theme.accent }};
            --accent2: {{ theme.accent2 }};
            --text: {{ theme.text }};
            --text-light: {{ theme.text_light }};
            --border: {{ theme.border }};
            --card-bg: {{ theme.card_bg }};
            --plot-bg: {{ theme.plot_bg }};
            --plot-face: {{ theme.plot_face }};
            --equation-bg: {{ theme.equation_bg }};
            --equation-font-size: {{ equation_font_size }}px;
            --coeff-label-font-size: {{ coeff_label_font_size }}px;
            --section-font-size: {{ section_font_size }}px;
            --label-font-size: {{ label_font_size }}px;
            --input-font-size: {{ input_font_size }}px;
            --label-color: {{ label_color }};
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', 'Times New Roman', Georgia, serif;
            background: var(--body-bg);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: var(--container-bg);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
            position: relative;
        }

        .header {
            background: var(--header-bg);
            color: white;
            padding: 20px 30px;
            text-align: center;
            border-bottom: 2px solid var(--accent);
            position: relative;
        }

        .header h1 {
            font-size: 1.8em;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .header-buttons {
            position: absolute;
            top: 50%;
            right: 30px;
            transform: translateY(-50%);
            display: flex;
            gap: 10px;
            z-index: 10;
        }

        .header-button {
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            font-size: 18px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .header-button:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }

        .equation-container {
            background: var(--equation-bg);
            padding: 5px 20px;
            margin: 20px;
            border-radius: 15px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            position: relative;
        }

        .method-selector {
            margin: 20px;
            padding: 15px 20px;
            background: var(--sidebar-bg);
            border-radius: 12px;
            border: 1px solid var(--accent);
        }

        .method-selector label {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            margin-right: 20px;
        }

        .method-selector input[type="radio"] {
            width: 16px;
            height: 16px;
            cursor: pointer;
            accent-color: var(--accent);
            margin: 0;
        }

        .info-sidebar, .theme-sidebar {
            position: fixed;
            top: 50%;
            right: -400px;
            transform: translateY(-50%);
            width: 320px;
            background: var(--card-bg);
            border-left: 4px solid var(--accent);
            border-radius: 12px 0 0 12px;
            padding: 25px;
            padding-top: 50px;
            box-shadow: -5px 0 20px rgba(0,0,0,0.2);
            transition: right 0.3s ease;
            z-index: 1000;
            max-height: 80vh;
            overflow-y: auto;
        }

        .info-sidebar.show, .theme-sidebar.show {
            right: 0;
        }

        .sidebar-header {
            position: absolute;
            top: 15px;
            left: 20px;
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: var(--text-light);
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }

        .close-btn:hover {
            color: var(--accent);
            background: rgba(0,0,0,0.05);
        }

        .info-sidebar h4, .theme-sidebar h4 {
            color: var(--accent);
            margin-bottom: 15px;
            font-size: 1.2em;
        }

        .info-sidebar p {
            color: var(--text);
            line-height: 1.6;
            margin-bottom: 10px;
        }

        .theme-option {
            padding: 10px 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid var(--border);
            background: var(--sidebar-bg);
        }

        .theme-option:hover {
            background: var(--accent);
            color: white;
            transform: translateX(5px);
        }

        .theme-option.active {
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }

        .theme-option .theme-name {
            font-weight: bold;
            font-size: 0.95em;
        }

        .equation-display {
            font-size: var(--equation-font-size);
            overflow-x: auto;
            padding: 10px;
            min-height: 80px;
        }

        .equation-display mjx-container {
            font-size: 1em !important;
        }

        .equation-display mjx-mover > mjx-script,
        .equation-display mjx-mover mjx-script,
        .equation-display mjx-mover mjx-texatom,
        .equation-display mjx-mover mjx-mi,
        .equation-display mjx-mover mjx-mo,
        .equation-display mjx-mover mjx-msub,
        .equation-display mjx-mover mjx-msubsup {
            color: var(--label-color) !important;
            font-size: var(--coeff-label-font-size) !important;
        }

        .panels-vertical {
            display: flex;
            flex-direction: column;
            gap: 20px;
            padding: 20px;
        }

        .params-panel {
            background: var(--sidebar-bg);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid var(--border);
        }

        .params-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .two-columns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
            align-items: stretch;
        }

        .two-columns .params-section {
            margin-bottom: 0;
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .two-columns .params-section .input-group:last-child {
            margin-bottom: 0;
        }

        .params-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }

        .params-section:last-child {
            margin-bottom: 0;
        }

        .section-label {
            margin: 12px 0 8px 0;
            font-size: var(--label-font-size);
            color: var(--text);
            font-weight: bold;
        }

        .input-group {
            margin-bottom: 12px;
        }

        .input-group label {
            display: block;
            margin-bottom: 4px;
            color: var(--text);
            font-weight: 500;
            font-size: var(--label-font-size);
        }

        .input-group input,
        .input-group select,
        .input-group textarea {
            width: 100%;
            padding: 8px;
            background: var(--sidebar-bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: var(--input-font-size);
            color: var(--text);
            transition: all 0.3s;
            font-family: monospace;
        }

        .input-group textarea {
            resize: vertical;
            min-height: 60px;
        }

        .input-group input:focus,
        .input-group select:focus,
        .input-group textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 5px var(--accent);
        }

        input[type="checkbox"] {
            width: 16px;
            height: 16px;
            cursor: pointer;
            accent-color: var(--accent);
            margin: 0;
        }

        .variables-section {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid var(--border);
            margin-bottom: 20px;
        }

        .variables-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .variables-header h3 {
            color: var(--accent);
            font-size: var(--section-font-size);
            margin: 0;
            border-bottom: none;
            padding-bottom: 0;
        }

        .var-row {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
            align-items: center;
        }

        .var-name {
            flex: 1;
        }

        .var-value {
            flex: 2;
        }

        .var-name input,
        .var-value input {
            width: 100%;
            padding: 6px 8px;
            background: var(--sidebar-bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: var(--input-font-size);
            color: var(--text);
            font-family: monospace;
        }

        .delete-var {
            background: none;
            border: none;
            color: var(--text-light);
            font-size: 18px;
            cursor: pointer;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }

        .delete-var:hover {
            color: var(--accent);
            background: rgba(0,0,0,0.05);
        }

        .add-var-row {
            margin-top: 10px;
            display: flex;
            justify-content: flex-start;
        }

        .add-var-btn {
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 6px 16px;
            font-size: 13px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s ease;
        }

        .add-var-btn:hover {
            transform: scale(1.02);
            background: var(--accent2);
        }

        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }

        .solve-button {
            width: auto;
            min-width: 200px;
            padding: 12px 30px;
            background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }

        .solve-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .solve-button:active {
            transform: translateY(0);
        }

        .solve-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .results-panel {
            background: var(--main-bg);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid var(--border);
            min-height: 400px;
        }

        .results {
            display: none;
        }

        .results.show {
            display: block;
        }

        .search-results {
            margin: 20px auto;
            padding: 15px;
            background: var(--card-bg);
            border-radius: 8px;
            border: 1px solid var(--accent);
            text-align: center;
            max-width: 1400px;
        }

        .search-results p {
            margin: 5px 0;
            font-size: 1em;
        }

        .search-results .result-value {
            font-weight: bold;
            color: var(--accent);
        }

        .results-table {
            margin: 20px auto;
            overflow-x: auto;
            max-width: 1400px;
            width: 100%;
        }

        .results-table table {
            margin: 0 auto;
            border-collapse: collapse;
            font-size: 18px;
            font-family: monospace;
            width: 100%;
        }

        .results-table th,
        .results-table td {
            border: 1px solid var(--border);
            padding: 6px 10px;
            text-align: center;
        }

        .results-table th {
            background: var(--accent);
            color: white;
            font-weight: bold;
            font-size: 18px;
        }

        .results-table td {
            font-size: 16px;
        }

        .results-table tr:nth-child(even) {
            background: var(--card-bg);
        }

        .results-table tr:hover {
            background: rgba(0,0,0,0.05);
        }

        .research-table-container {
            margin-top: 20px;
            overflow-x: auto;
        }

        .research-params-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }

        .research-params-table th,
        .research-params-table td {
            border: 1px solid var(--border);
            padding: 8px 10px;
            text-align: center;
            vertical-align: middle;
        }

        .research-params-table th {
            background: var(--accent);
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        .research-params-table td input {
            width: 100px;
            padding: 4px 6px;
            background: var(--sidebar-bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            font-size: 12px;
            color: var(--text);
            font-family: monospace;
            text-align: center;
        }

        .delete-row-btn {
            background: none;
            border: none;
            color: var(--text-light);
            font-size: 20px;
            cursor: pointer;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
            margin: 0 auto;
        }

        .delete-row-btn:hover {
            color: var(--accent);
            background: rgba(0,0,0,0.05);
        }

        .add-row-btn {
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 8px 20px;
            font-size: 13px;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s ease;
            margin-top: 10px;
        }

        .add-row-btn:hover {
            transform: scale(1.02);
            background: var(--accent2);
        }

        .param-plots {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid var(--accent);
        }

        .param-plots-title {
            color: var(--accent);
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.2em;
        }

        .param-plots-grid {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }

        .param-plots-grid.horizontal {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
            align-items: flex-start;
            gap: 20px;
        }

        .param-plot-container {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            flex: 0 1 auto;
            min-width: 350px;
        }

        .param-plot-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .param-plot-header h4 {
            color: var(--accent);
            margin: 0;
            font-size: 0.9em;
            word-break: break-word;
        }

        .param-plot-container img {
            width: 100%;
            border-radius: 8px;
        }

        .param-plot-controls {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .param-plot-zoom-btn {
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 6px 15px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .param-plot-zoom-btn:hover {
            transform: scale(1.02);
            background: var(--accent2);
        }

        .plot-container {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid var(--border);
            width: 100%;
            max-width: 900px;
            transition: max-width 0.3s ease;
            position: relative;
        }

        .plot-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .plot-header h4 {
            color: var(--accent);
            margin: 0;
            font-size: 0.95em;
        }

        .plot-controls {
            display: flex;
            gap: 8px;
        }

        .plot-zoom-btn {
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 11px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .plot-zoom-btn:hover {
            transform: scale(1.02);
            background: var(--accent2);
        }

        .plot-size-info {
            font-size: 11px;
            color: var(--text-light);
            background: var(--card-bg);
            padding: 4px 8px;
            border-radius: 6px;
        }

        .plot-container img {
            width: 100%;
            border-radius: 8px;
        }

        .plots {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
            margin-bottom: 30px;
        }

        .plots.horizontal {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: flex-start;
            gap: 20px;
            flex-wrap: wrap;
        }

        .plots.horizontal .plot-container {
            flex: 0 1 auto;
            margin: 0;
        }

        .loading {
            text-align: center;
            padding: 50px;
        }

        .spinner {
            border: 4px solid var(--card-bg);
            border-top: 4px solid var(--accent);
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            background: rgba(255,0,0,0.1);
            color: var(--accent);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--accent);
        }

        .empty-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 400px;
            color: var(--text-light);
            text-align: center;
        }

        .empty-state p {
            margin-top: 20px;
            font-size: 1.1em;
        }

        @media (max-width: 1024px) {
            .params-grid {
                grid-template-columns: 1fr;
            }

            .two-columns {
                grid-template-columns: 1fr;
            }

            .plots.horizontal {
                flex-direction: column;
                align-items: center;
            }

            .param-plots-grid.horizontal {
                flex-direction: column;
                align-items: center;
            }

            .param-plot-container {
                min-width: 280px;
            }

            .research-params-table td input {
                width: 70px;
                font-size: 10px;
            }

            .research-params-table th {
                font-size: 11px;
                padding: 6px 4px;
            }

            .results-table {
                font-size: 14px;
            }

            .results-table th,
            .results-table td {
                padding: 4px 6px;
            }

            .results-table th {
                font-size: 14px;
            }

            .results-table td {
                font-size: 12px;
            }

            .info-sidebar, .theme-sidebar {
                width: 90%;
                right: -90%;
            }

            .header-buttons {
                position: static;
                transform: none;
                justify-content: flex-end;
                margin-top: 10px;
            }

            .header {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Обобщённое уравнение Клейна-Гордона с диссипацией</h1>
            <div class="header-buttons">
                <button class="header-button" id="themeButton" onclick="toggleTheme()">🎨</button>
                <button class="header-button" id="infoButton" onclick="toggleInfo()">?</button>
            </div>
        </div>

        <div class="equation-container">
            <div class="equation-display" id="equationDisplay">
                $$ u_{tt} - \overset{k_2}{1} \partial_x^2 u_t + \overset{k_0}{1} u_t - \overset{c^2}{1} \partial_x^2 u + \overset{k_n}{1} u^3 = g(x, t) $$
            </div>
        </div>

        <div class="method-selector">
            <div style="display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
                <span style="font-weight: bold; color: var(--accent);">Выберите метод решения:</span>
                <label>
                    <input type="radio" name="method_type" value="iterative" checked onchange="toggleMethodParams()">
                    <span>Метод простой итерации</span>
                </label>
                <label>
                    <input type="radio" name="method_type" value="linearized" onchange="toggleMethodParams()">
                    <span>Линеаризованный метод</span>
                </label>
                <label>
                    <input type="radio" name="method_type" value="newton" onchange="toggleMethodParams()">
                    <span>Метод Ньютона</span>
                </label>
            </div>
        </div>

        <div id="infoSidebar" class="info-sidebar">
            <div class="sidebar-header">
                <button class="close-btn" onclick="toggleInfo()">×</button>
            </div>
            <h4>Пояснения к приложению</h4>
        
            <div style="margin-bottom: 20px;">
                <p style="font-weight: bold; color: var(--accent);">Ввод математических выражений</p>
                <p>Во все поля ввода (начальные условия, граничные условия, правая часть, точное решение и переменные) можно вводить математические формулы на языке Python/numpy.</p>
                <p style="font-weight: bold; margin-top: 8px;">Поддерживаемые функции и операции:</p>
                <ul style="margin-left: 20px; margin-top: 5px; line-height: 1.5;">
                    <li><strong>Базовые операции:</strong> +, -, *, /, ** (возведение в степень)</li>
                    <li><strong>Тригонометрические:</strong> sin(x), cos(x), tan(x), asin(x), acos(x), atan(x)</li>
                    <li><strong>Гиперболические:</strong> sinh(x), cosh(x), tanh(x)</li>
                    <li><strong>Экспоненты и логарифмы:</strong> exp(x), log(x) (натуральный), log10(x)</li>
                    <li><strong>Корни и модуль:</strong> sqrt(x), abs(x)</li>
                    <li><strong>Константы:</strong> pi, e</li>
                </ul>
            </div>
        
            <div style="margin-bottom: 20px;">
                <p style="font-weight: bold; color: var(--accent);">Пользовательские переменные</p>
                <p>Вы можете создавать <strong>собственные переменные</strong>, которые затем использовать в любых полях ввода. Это удобно для параметризации задачи.</p>
                <p><strong>Как использовать:</strong></p>
                <ol style="margin-left: 20px; margin-top: 5px; line-height: 1.5;">
                    <li>Нажмите кнопку <strong>"+ Добавить переменную"</strong></li>
                    <li>Введите <strong>имя переменной</strong> (например: <code>alpha</code>, <code>beta</code>, <code>omega</code>)</li>
                    <li>Введите <strong>значение</strong> (число или выражение из других переменных)</li>
                    <li>Используйте имя переменной в любом поле ввода (например: <code>alpha*sin(2*pi*x)</code>)</li>
                </ol>
            </div>
        
            <div style="margin-bottom: 20px;">
                <p style="font-weight: bold; color: var(--accent);">Исследование параметров</p>
                <p>Эта функция позволяет <strong>сравнить решения</strong> при разных значениях параметров на одном экране.</p>
                <p><strong>Как использовать:</strong></p>
                <ol style="margin-left: 20px; margin-top: 5px; line-height: 1.5;">
                    <li>Отметьте галочку <strong>"Исследовать разные варианты"</strong></li>
                    <li>В поле <strong>"Названия параметров через запятую"</strong> введите имена параметров, которые хотите менять (например: <code>k0, k2, kn, M, T</code>)</li>
                    <li>Нажмите <strong>"Установить параметры"</strong> — появится таблица</li>
                    <li>Для каждого варианта (строки) заполните значения параметров</li>
                    <li>Нажмите <strong>"Выполнить расчёт"</strong> — приложение решит задачу для каждого варианта и покажет графики</li>
                </ol>
                <p><strong>Какие параметры можно менять:</strong></p>
                <ul style="margin-left: 20px;">
                    <li>Коэффициенты: <code>k0</code>, <code>k2</code>, <code>c2</code>, <code>kn</code></li>
                    <li>Параметры сетки: <code>M</code>, <code>N</code></li>
                    <li>Конечное время: <code>T</code></li>
                    <li>Любые пользовательские переменные</li>
                </ul>
            </div>
        
            <div style="margin-bottom: 20px;">
                <p style="font-weight: bold; color: var(--accent);">Поиск значений</p>
                <p>В параметрах каждого метода есть поля:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>"Найти u(x,T) при x = ..."</strong> — найти значение решения в конечный момент времени в указанной точке x</li>
                    <li><strong>"Найти x при u(x,T) = ..."</strong> — найти координату x, где решение принимает заданное значение</li>
                </ul>
                <p>Результаты поиска отображаются над таблицей.</p>
            </div>
        
            <div style="margin-bottom: 20px;">
                <p style="font-weight: bold; color: var(--accent);">Результаты</p>
                <p>После расчёта отображаются:</p>
                <ul style="margin-left: 20px;">
                    <li><strong>Таблица</strong> — значения решения в выбранных точках по x и t, количество итераций, ошибка</li>
                    <li><strong>График решения</strong> — u(x,T) в конечный момент времени</li>
                    <li><strong>График ошибки</strong> — эволюция L₂-нормы ошибки (при наличии точного решения)</li>
                    <li><strong>График энергии</strong> — только для метода Ньютона</li>
                    <li><strong>Графики исследования параметров</strong> — при включённой опции</li>
                </ul>
                <p>Кнопками <strong>🔍 Увеличить/Уменьшить</strong> можно менять размер всех графиков одновременно.</p>
            </div>
        
            <div style="margin-bottom: 10px;">
                <p style="font-weight: bold; color: var(--accent);">Примечания</p>
                <ul style="margin-left: 20px;">
                    <li>При большом количестве узлов (M, N > 200) расчёт может занять время</li>
                    <li>Метод Ньютона даёт более быструю сходимость, но требует хорошего начального приближения</li>
                    <li>Если точное решение не задано, график ошибки не отображается</li>
                    <li>При ошибках ввода проверьте синтаксис математических выражений</li>
                </ul>
            </div>
        </div>

        <div id="themeSidebar" class="theme-sidebar">
            <div class="sidebar-header">
                <button class="close-btn" onclick="toggleTheme()">×</button>
            </div>
            <h4>Тема оформления</h4>
            {% for key, theme in themes.items() %}
            <div class="theme-option" data-theme="{{ key }}" onclick="selectTheme('{{ key }}')">
                <div class="theme-name">{{ theme.name }}</div>
            </div>
            {% endfor %}
        </div>

        <div class="panels-vertical">
            <div class="params-panel">
                <div class="params-grid">
                    <!-- ЛЕВАЯ КОЛОНКА -->
                    <div>
                        <div class="variables-section" id="variablesSection">
                            <div class="variables-header">
                                <h3>Пользовательские переменные (при наличии)</h3>
                            </div>
                            <div id="variablesList"></div>
                            <div class="add-var-row">
                                <button class="add-var-btn" onclick="addVariable()">+ Добавить переменную</button>
                            </div>
                        </div>

                        <div class="two-columns">
                            <div class="params-section">
                                <h3>Геометрия и сетка</h3>
                                <div class="input-group">
                                    <label>левая граница по x</label>
                                    <input type="number" id="x_left" value="0" step="0.1">
                                </div>
                                <div class="input-group">
                                    <label>правая граница по x</label>
                                    <input type="number" id="x_right" value="1" step="0.1">
                                </div>
                                <div class="input-group">
                                    <label>T (конечное время)</label>
                                    <input type="number" id="T" value="1" step="0.1">
                                </div>
                                <div class="input-group">
                                    <label>M (узлы по x)</label>
                                    <input type="number" id="M" value="100" step="10">
                                </div>
                                <div class="input-group">
                                    <label>N (узлы по t)</label>
                                    <input type="number" id="N" value="100" step="10">
                                </div>
                            </div>

                            <div class="params-section">
                                <h3>Коэффициенты</h3>
                                <div class="input-group">
                                    <label>k₀ (коэффициент диссипации)</label>
                                    <input type="number" id="k0" value="1" step="0.1" min="0" oninput="updateEquation()">
                                </div>
                                <div class="input-group">
                                    <label>k₂ (коэффициент диссипации)</label>
                                    <input type="number" id="k2" value="1" step="0.1" min="0" oninput="updateEquation()">
                                </div>
                                <div class="input-group">
                                    <label>c² (скорость распространения)</label>
                                    <input type="number" id="c2" value="1" step="0.1" min="0.1" oninput="updateEquation()">
                                </div>
                                <div class="input-group">
                                    <label>kₙ (коэффициент нелинейности)</label>
                                    <input type="number" id="kn" value="1" step="0.1" min="0" oninput="updateEquation()">
                                </div>
                            </div>
                        </div>

                        <div class="params-section" id="iterativeParams">
                            <h3>Параметры решения (метод простой итерации)</h3>
                            <div class="input-group">
                                <label>Тип нелинейности f(u)</label>
                                <select id="nonlinear_type" onchange="updateEquation()">
                                    <option value="cubic">Кубическая: u³</option>
                                    <option value="sin">Синус: sin(u)</option>
                                    <option value="sinh">Гиперболический синус: sinh(u)</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label>Максимум итераций</label>
                                <input type="number" id="max_iter" value="50" min="10" max="200">
                            </div>
                            <div class="input-group">
                                <label>Допустимая погрешность (ε = 10ⁿ)</label>
                                <input type="number" id="tol_exp" value="-8" min="-15" max="-2" step="1">
                            </div>
                            <div class="input-group">
                                <label>Количество выводимых x значений</label>
                                <input type="number" id="num_x_output" value="5" min="2" max="20" step="1">
                            </div>
                            <div class="input-group">
                                <label>Количество выводимых t значений</label>
                                <input type="number" id="num_t_output" value="11" min="2" max="30" step="1">
                            </div>
                            <div class="input-group">
                                <label>Найти u(x,T) при x = ... (необязательно)</label>
                                <input type="text" id="find_u_at_x" placeholder="например: 0.25 или 0.5" style="font-family: monospace;">
                            </div>
                            <div class="input-group">
                                <label>Найти x при u(x,T) = ... (необязательно)</label>
                                <input type="text" id="find_x_at_u" placeholder="например: 0.5 или -0.5" style="font-family: monospace;">
                            </div>
                        </div>

                        <div class="params-section" id="linearizedParams" style="display: none;">
                            <h3>Параметры решения (линеаризованный метод)</h3>
                            <div class="input-group">
                                <label>Количество выводимых x значений</label>
                                <input type="number" id="num_x_output_lin" value="5" min="2" max="20" step="1">
                            </div>
                            <div class="input-group">
                                <label>Количество выводимых t значений</label>
                                <input type="number" id="num_t_output_lin" value="11" min="2" max="30" step="1">
                            </div>
                            <div class="input-group">
                                <label>Найти u(x,T) при x = ... (необязательно)</label>
                                <input type="text" id="find_u_at_x_lin" placeholder="например: 0.25 или 0.5" style="font-family: monospace;">
                            </div>
                            <div class="input-group">
                                <label>Найти x при u(x,T) = ... (необязательно)</label>
                                <input type="text" id="find_x_at_u_lin" placeholder="например: 0.5 или -0.5" style="font-family: monospace;">
                            </div>
                        </div>

                        <div class="params-section" id="newtonParams" style="display: none;">
                            <h3>Параметры решения (метод Ньютона)</h3>
                            <div class="input-group">
                                <label>Максимум итераций Ньютона</label>
                                <input type="number" id="newton_max_iter" value="30" min="5" max="100">
                            </div>
                            <div class="input-group">
                                <label>Допустимая погрешность Ньютона (ε = 10ⁿ)</label>
                                <input type="number" id="newton_tol_exp" value="-8" min="-15" max="-2" step="1">
                            </div>
                            <div class="input-group">
                                <label>Количество выводимых x значений</label>
                                <input type="number" id="num_x_output_newton" value="5" min="2" max="20" step="1">
                            </div>
                            <div class="input-group">
                                <label>Количество выводимых t значений</label>
                                <input type="number" id="num_t_output_newton" value="11" min="2" max="30" step="1">
                            </div>
                            <div class="input-group">
                                <label>Найти u(x,T) при x = ... (необязательно)</label>
                                <input type="text" id="find_u_at_x_newton" placeholder="например: 0.25 или 0.5" style="font-family: monospace;">
                            </div>
                            <div class="input-group">
                                <label>Найти x при u(x,T) = ... (необязательно)</label>
                                <input type="text" id="find_x_at_u_newton" placeholder="например: 0.5 или -0.5" style="font-family: monospace;">
                            </div>
                        </div>
                    </div>

                    <!-- ПРАВАЯ КОЛОНКА -->
                    <div>
                        <div class="params-section">
                            <h3>Начальные и граничные условия</h3>

                            <div class="section-label">Начальные условия</div>
                            <div class="input-group">
                                <label>u(x,0) = η(x)</label>
                                <textarea id="ic" rows="2" placeholder="sin(2*pi*x)">sin(2*pi*x)</textarea>
                            </div>
                            <div class="input-group">
                                <label>∂ₜu(x,0) = μ(x)</label>
                                <textarea id="ic_deriv" rows="2" placeholder="-sin(2*pi*x)">-sin(2*pi*x)</textarea>
                            </div>

                            <div class="section-label">Граничные условия</div>
                            <div class="input-group">
                                <label>u(0,t) = g₀(t)</label>
                                <textarea id="bc_left" rows="2" placeholder="0">0</textarea>
                            </div>
                            <div class="input-group">
                                <label>u(1,t) = g₁(t)</label>
                                <textarea id="bc_right" rows="2" placeholder="0">0</textarea>
                            </div>
                        </div>

                        <div class="params-section">
                            <h3>Правая часть уравнения</h3>
                            <div class="input-group">
                                <label>g(x,t)</label>
                                <textarea id="source" rows="3" placeholder="(1 - k0 + 4*pi**2*(c2 - k2))*sin(2*pi*x)*exp(-t) + kn*sin(2*pi*x)**3*exp(-3*t)">(1 - k0 + 4*pi**2*(c2 - k2))*sin(2*pi*x)*exp(-t) + kn*sin(2*pi*x)**3*exp(-3*t)</textarea>
                            </div>
                        </div>

                        <div class="params-section">
                            <h3>Точное решение (при наличии)</h3>
                            <div class="input-group" id="exactSolutionGroup">
                                <label>u_exact(x,t)</label>
                                <textarea id="exact_solution" rows="3" placeholder="sin(2*pi*x)*exp(-t)">sin(2*pi*x)*exp(-t)</textarea>
                            </div>
                            <div style="margin-top: 10px;">
                                <label style="display: inline-flex; align-items: center; gap: 6px; cursor: pointer;">
                                    <input type="checkbox" id="noExactSolution" onchange="toggleExactSolution()">
                                    <span style="font-size: var(--label-font-size);">Точного решения нет</span>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Секция исследования параметров - табличный вид -->
                <div class="params-section" id="researchSection" style="margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3>Исследование параметров</h3>
                        <label style="display: inline-flex; align-items: center; gap: 8px; cursor: pointer;">
                            <input type="checkbox" id="enableResearch" onchange="toggleResearch()">
                            <span style="font-size: var(--label-font-size);">Исследовать разные варианты</span>
                        </label>
                    </div>
                    <div id="researchParams" style="display: none;">
                        <div class="research-table-container">
                            <table class="research-params-table" id="researchParamsTable">
                                <thead>
                                    <tr id="researchHeaderRow">
                                        <th style="width: 60px;">№</th>
                                        <th id="paramNamesHeader">Параметры (введите названия переменных)</th>
                                        <th style="width: 50px;"></th>
                                    </tr>
                                </thead>
                                <tbody id="researchParamsBody">
                                    <tr class="param-header-row">
                                        <td colspan="3" style="background: var(--sidebar-bg); padding: 8px;">
                                            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                                                <input type="text" id="paramNamesInput" placeholder="Названия параметров через запятую" style="flex: 2; padding: 6px 8px; background: var(--sidebar-bg); border: 1px solid var(--border); border-radius: 4px; font-family: monospace;">
                                                <button class="add-row-btn" onclick="updateParamNames()" style="margin: 0;">Установить параметры</button>
                                            </div>
                                            <div style="font-size: 12px; color: var(--text-light); margin-top: 5px;">
                                                Пример: alfa, k0, k2, kn, T, N
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="add-row-container" style="margin-top: 10px; display: flex; gap: 10px; justify-content: center;">
                            <button class="add-row-btn" onclick="addResearchRow()">+ Добавить вариант</button>
                        </div>
                    </div>
                </div>

                <div class="button-container">
                    <button class="solve-button" id="solveBtn" onclick="solve()">
                        Выполнить расчёт
                    </button>
                </div>
            </div>

            <div class="results-panel">
                <div id="emptyState" class="empty-state">
                    <p>Здесь будут отображаться результаты расчёта</p>
                </div>

                <div id="results" class="results">
                    <div id="searchResults" class="search-results" style="display: none;"></div>
                    <div id="resultsTable" class="results-table"></div>
                    <div id="plotControls" class="plot-controls" style="display: none;">
                        <button class="plot-zoom-btn" onclick="zoomMainPlots('in')">🔍 Увеличить</button>
                        <button class="plot-zoom-btn" onclick="zoomMainPlots('out')">🔍 Уменьшить</button>
                        <button class="plot-zoom-btn" onclick="resetMainPlotsSize()">⟳ Сбросить</button>
                        <span class="plot-size-info" id="plotSizeInfo">Текущий размер: 900px</span>
                    </div>
                    <div class="plots" id="plots"></div>
                    <div id="researchPlots" class="param-plots" style="display: none;"></div>
                </div>

                <div id="loading" class="loading" style="display: none;">
                    <div class="spinner"></div>
                    <p>Выполняется численное решение...</p>
                </div>

                <div id="error" class="error" style="display: none;"></div>
            </div>
        </div>
    </div>

    <script>
        let customVariables = [];
        let researchParamNames = [];
        let researchRows = [];
        let currentMainPlotWidth = 900;
        let currentParamPlotWidth = 500;
        let researchInitialized = false;

        function toggleMethodParams() {
            const methodRadios = document.querySelectorAll('input[name="method_type"]');
            let method = 'iterative';
            for (let radio of methodRadios) {
                if (radio.checked) {
                    method = radio.value;
                    break;
                }
            }

            const iterativeDiv = document.getElementById('iterativeParams');
            const linearizedDiv = document.getElementById('linearizedParams');
            const newtonDiv = document.getElementById('newtonParams');

            iterativeDiv.style.display = 'none';
            linearizedDiv.style.display = 'none';
            newtonDiv.style.display = 'none';

            if (method === 'iterative') {
                iterativeDiv.style.display = 'block';
            } else if (method === 'linearized') {
                linearizedDiv.style.display = 'block';
            } else if (method === 'newton') {
                newtonDiv.style.display = 'block';
            }

            updateEquation();
        }

        function updateVariableInputs() {
            const container = document.getElementById('variablesList');
            if (!container) return;

            container.innerHTML = '';
            customVariables.forEach((variable, index) => {
                const row = document.createElement('div');
                row.className = 'var-row';
                row.innerHTML = `
                    <div class="var-name">
                        <input type="text" placeholder="Имя (например: a, b, c1)" value="${escapeHtml(variable.name)}" onchange="updateVariableName(${index}, this.value)">
                    </div>
                    <div class="var-value">
                        <input type="text" placeholder="Значение" value="${escapeHtml(variable.value)}" onchange="updateVariableValue(${index}, this.value)">
                    </div>
                    <button class="delete-var" onclick="deleteVariable(${index})">×</button>
                `;
                container.appendChild(row);
            });
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, '&amp;')
                       .replace(/</g, '&lt;')
                       .replace(/>/g, '&gt;')
                       .replace(/"/g, '&quot;')
                       .replace(/'/g, '&#39;');
        }

        function addVariable() {
            customVariables.push({ name: '', value: '' });
            updateVariableInputs();
        }

        function deleteVariable(index) {
            customVariables.splice(index, 1);
            updateVariableInputs();
        }

        function updateVariableName(index, newName) {
            customVariables[index].name = newName;
        }

        function updateVariableValue(index, newValue) {
            customVariables[index].value = newValue;
        }

        function getCustomVariablesDict() {
            const dict = {};
            customVariables.forEach(v => {
                if (v.name && v.name.trim() !== '' && v.value && v.value.trim() !== '') {
                    dict[v.name.trim()] = v.value.trim();
                }
            });
            return dict;
        }

        function toggleInfo() {
            document.getElementById('infoSidebar').classList.toggle('show');
        }

        function toggleTheme() {
            document.getElementById('themeSidebar').classList.toggle('show');
        }

        function selectTheme(themeKey) {
            window.location.href = '/set_theme/' + themeKey;
        }

        function toggleExactSolution() {
            const isChecked = document.getElementById('noExactSolution').checked;
            const exactGroup = document.getElementById('exactSolutionGroup');
            exactGroup.style.display = isChecked ? 'none' : 'block';
        }

        function updateEquation() {
            const k0 = document.getElementById('k0').value;
            const k2 = document.getElementById('k2').value;
            const c2 = document.getElementById('c2').value;
            const kn = document.getElementById('kn').value;

            const methodRadios = document.querySelectorAll('input[name="method_type"]');
            let method = 'iterative';
            for (let radio of methodRadios) {
                if (radio.checked) {
                    method = radio.value;
                    break;
                }
            }

            let f_u = '';
            if (method === 'iterative') {
                const nonlinear_type = document.getElementById('nonlinear_type').value;
                if (nonlinear_type === 'cubic') f_u = 'u^3';
                else if (nonlinear_type === 'sin') f_u = '\\sin(u)';
                else f_u = '\\sinh(u)';
            } else {
                f_u = 'u^3';
                if (document.getElementById('nonlinear_type')) {
                    document.getElementById('nonlinear_type').value = 'cubic';
                }
            }

            const equation = `u_{tt} - \\overset{k_2}{${k2}} \\partial_x^2 u_t + \\overset{k_0}{${k0}} u_t - \\overset{c^2}{${c2}} \\partial_x^2 u + \\overset{k_n}{${kn}} ${f_u} = g(x, t)`;

            document.getElementById('equationDisplay').innerHTML = `$$ ${equation} $$`;
            if (window.MathJax) MathJax.typesetPromise();
        }

        function toggleResearch() {
            const isChecked = document.getElementById('enableResearch').checked;
            const researchDiv = document.getElementById('researchParams');
            researchDiv.style.display = isChecked ? 'block' : 'none';
            if (isChecked && !researchInitialized) {
                researchInitialized = true;
                renderResearchTable();
            }
        }

        function updateParamNames() {
            const input = document.getElementById('paramNamesInput');
            const namesStr = input.value.trim();
            if (namesStr) {
                researchParamNames = namesStr.split(',').map(n => n.trim()).filter(n => n);
                renderResearchTable();
                if (researchRows.length === 0) {
                    addResearchRow();
                }
            }
        }

        function renderResearchTable() {
            const tbody = document.getElementById('researchParamsBody');
            if (!tbody) return;

            const rowsToRemove = [];
            for (let i = 0; i < tbody.children.length; i++) {
                const row = tbody.children[i];
                if (row.classList && !row.classList.contains('param-header-row')) {
                    rowsToRemove.push(row);
                }
            }
            rowsToRemove.forEach(row => row.remove());

            if (researchParamNames.length === 0) {
                const emptyRow = document.createElement('tr');
                emptyRow.className = 'empty-params-row';
                emptyRow.innerHTML = `
                    <td colspan="3" style="text-align: center; padding: 20px; color: var(--text-light);">
                        Введите названия параметров для исследования
                    </td>
                `;
                tbody.appendChild(emptyRow);
                return;
            }

            researchRows.forEach((row, idx) => {
                const tr = document.createElement('tr');
                tr.className = 'research-row';
                tr.innerHTML = `
                    <td style="text-align: center; vertical-align: middle;">${idx + 1}</td>
                    <td style="padding: 8px;">
                        <div style="display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;">
                            ${researchParamNames.map((param, pIdx) => `
                                <div style="min-width: 80px; text-align: center;">
                                    <div style="font-size: 11px; color: var(--accent); margin-bottom: 2px;">${escapeHtml(param)}</div>
                                    <input type="text" class="param-value-input" data-row="${idx}" data-param="${pIdx}" value="${escapeHtml(row.values[pIdx] || '')}" style="width: 100px; padding: 4px 6px; background: var(--sidebar-bg); border: 1px solid var(--border); border-radius: 4px; font-family: monospace; font-size: 12px; text-align: center;">
                                </div>
                            `).join('')}
                        </div>
                    </td>
                    <td style="text-align: center; vertical-align: middle;">
                        <button class="delete-row-btn" onclick="deleteResearchRow(${idx})">×</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            document.querySelectorAll('.param-value-input').forEach(input => {
                input.removeEventListener('change', handleParamValueChange);
                input.addEventListener('change', handleParamValueChange);
            });
        }

        function handleParamValueChange(e) {
            const row = parseInt(e.target.dataset.row);
            const param = parseInt(e.target.dataset.param);
            if (!isNaN(row) && !isNaN(param) && researchRows[row]) {
                researchRows[row].values[param] = e.target.value;
            }
        }

        function addResearchRow() {
            if (researchParamNames.length === 0) {
                const tbody = document.getElementById('researchParamsBody');
                if (tbody) {
                    const emptyRow = tbody.querySelector('.empty-params-row');
                    if (emptyRow) emptyRow.remove();
                }
                return;
            }
            const values = new Array(researchParamNames.length).fill('');
            researchRows.push({ values: values });
            renderResearchTable();
        }

        function deleteResearchRow(index) {
            researchRows.splice(index, 1);
            renderResearchTable();
        }

        function getResearchParamsArray() {
            const rows = [];
            for (let i = 0; i < researchRows.length; i++) {
                const rowValues = [];
                for (let j = 0; j < researchParamNames.length; j++) {
                    const val = researchRows[i].values[j];
                    if (val && val.trim() !== '') {
                        const num = parseFloat(val);
                        rowValues.push(isNaN(num) ? val : num);
                    } else {
                        rowValues.push(null);
                    }
                }
                rows.push(rowValues);
            }
            return { names: researchParamNames, rows: rows };
        }

        function zoomMainPlots(direction) {
            if (direction === 'in') {
                currentMainPlotWidth = Math.min(currentMainPlotWidth + 50, 1600);
            } else {
                currentMainPlotWidth = Math.max(currentMainPlotWidth - 50, 400);
            }

            const plotContainers = document.querySelectorAll('.plot-container');
            plotContainers.forEach(container => {
                container.style.maxWidth = currentMainPlotWidth + 'px';
                container.style.width = '100%';
            });

            document.getElementById('plotSizeInfo').textContent = `Текущий размер: ${currentMainPlotWidth}px`;
            updateMainPlotsLayout();
        }

        function resetMainPlotsSize() {
            currentMainPlotWidth = 900;
            const plotContainers = document.querySelectorAll('.plot-container');
            plotContainers.forEach(container => {
                container.style.maxWidth = '900px';
                container.style.width = '100%';
            });
            document.getElementById('plotSizeInfo').textContent = `Текущий размер: 900px`;
            updateMainPlotsLayout();
        }

        function updateMainPlotsLayout() {
            const plotsDiv = document.getElementById('plots');
            const plotContainers = document.querySelectorAll('.plot-container');
            const containerWidth = document.querySelector('.results-panel').clientWidth;

            if (plotContainers.length >= 2) {
                if (containerWidth >= currentMainPlotWidth * 2 + 50) {
                    plotsDiv.classList.add('horizontal');
                } else {
                    plotsDiv.classList.remove('horizontal');
                }
            } else {
                plotsDiv.classList.remove('horizontal');
            }
        }

        function zoomParamPlots(direction) {
            if (direction === 'in') {
                currentParamPlotWidth = Math.min(currentParamPlotWidth + 50, 1200);
            } else {
                currentParamPlotWidth = Math.max(currentParamPlotWidth - 50, 300);
            }

            const plotContainers = document.querySelectorAll('.param-plot-container');
            plotContainers.forEach(container => {
                container.style.maxWidth = currentParamPlotWidth + 'px';
                container.style.width = '100%';
            });

            const sizeInfo = document.getElementById('paramPlotSizeInfo');
            if (sizeInfo) sizeInfo.textContent = `Текущий размер: ${currentParamPlotWidth}px`;
            updateParamPlotsLayout();
        }

        function resetParamPlotsSize() {
            currentParamPlotWidth = 500;
            const plotContainers = document.querySelectorAll('.param-plot-container');
            plotContainers.forEach(container => {
                container.style.maxWidth = '500px';
                container.style.width = '100%';
            });
            const sizeInfo = document.getElementById('paramPlotSizeInfo');
            if (sizeInfo) sizeInfo.textContent = `Текущий размер: 500px`;
            updateParamPlotsLayout();
        }

        function updateParamPlotsLayout() {
            const plotsDiv = document.getElementById('researchPlotsGrid');
            if (!plotsDiv) return;
            const containerWidth = document.querySelector('.results-panel').clientWidth;
            const plotsCount = document.querySelectorAll('.param-plot-container').length;

            if (plotsCount > 0 && containerWidth >= currentParamPlotWidth * 2 + 50) {
                plotsDiv.classList.add('horizontal');
            } else {
                plotsDiv.classList.remove('horizontal');
            }
        }

        window.addEventListener('resize', function() {
            updateMainPlotsLayout();
            updateParamPlotsLayout();
        });

        async function solve() {
            document.getElementById('emptyState').style.display = 'none';
            document.getElementById('results').classList.remove('show');
            document.getElementById('error').style.display = 'none';
            document.getElementById('loading').style.display = 'block';

            const btn = document.getElementById('solveBtn');
            btn.disabled = true;
            btn.textContent = 'Расчёт...';

            const customVars = getCustomVariablesDict();
            const noExactSolution = document.getElementById('noExactSolution').checked;
            const enableResearch = document.getElementById('enableResearch').checked;
            const researchData = enableResearch ? getResearchParamsArray() : { names: [], rows: [] };

            const methodRadios = document.querySelectorAll('input[name="method_type"]');
            let method = 'iterative';
            for (let radio of methodRadios) {
                if (radio.checked) {
                    method = radio.value;
                    break;
                }
            }

            const baseData = {
                x_left: parseFloat(document.getElementById('x_left').value),
                x_right: parseFloat(document.getElementById('x_right').value),
                T: parseFloat(document.getElementById('T').value),
                M: parseInt(document.getElementById('M').value),
                N: parseInt(document.getElementById('N').value),
                c2: parseFloat(document.getElementById('c2').value),
                k2: parseFloat(document.getElementById('k2').value),
                k0: parseFloat(document.getElementById('k0').value),
                kn: parseFloat(document.getElementById('kn').value),
                ic: document.getElementById('ic').value,
                ic_deriv: document.getElementById('ic_deriv').value,
                bc_left: document.getElementById('bc_left').value,
                bc_right: document.getElementById('bc_right').value,
                exact_solution: document.getElementById('exact_solution').value,
                source: document.getElementById('source').value,
                custom_variables: customVars,
                no_exact_solution: noExactSolution,
                enable_research: enableResearch,
                research_param_names: researchData.names,
                research_rows: researchData.rows,
                method: method
            };

            if (method === 'iterative') {
                baseData.nonlinear_type = document.getElementById('nonlinear_type').value;
                baseData.max_iter = parseInt(document.getElementById('max_iter').value);
                baseData.tol_exp = parseInt(document.getElementById('tol_exp').value);
                baseData.num_x_output = parseInt(document.getElementById('num_x_output').value);
                baseData.num_t_output = parseInt(document.getElementById('num_t_output').value);
                baseData.find_u_at_x = document.getElementById('find_u_at_x').value;
                baseData.find_x_at_u = document.getElementById('find_x_at_u').value;
            } else if (method === 'linearized') {
                baseData.num_x_output = parseInt(document.getElementById('num_x_output_lin').value);
                baseData.num_t_output = parseInt(document.getElementById('num_t_output_lin').value);
                baseData.find_u_at_x = document.getElementById('find_u_at_x_lin').value;
                baseData.find_x_at_u = document.getElementById('find_x_at_u_lin').value;
            } else if (method === 'newton') {
                baseData.newton_max_iter = parseInt(document.getElementById('newton_max_iter').value);
                baseData.newton_tol_exp = parseInt(document.getElementById('newton_tol_exp').value);
                baseData.num_x_output = parseInt(document.getElementById('num_x_output_newton').value);
                baseData.num_t_output = parseInt(document.getElementById('num_t_output_newton').value);
                baseData.find_u_at_x = document.getElementById('find_u_at_x_newton').value;
                baseData.find_x_at_u = document.getElementById('find_x_at_u_newton').value;
            }

            try {
                const response = await fetch('/solve', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(baseData)
                });

                if (!response.ok) {
                    const err = await response.json();
                    throw new Error(err.error || 'Ошибка сервера');
                }

                const result = await response.json();

                if (result.search_results_html) {
                    document.getElementById('searchResults').innerHTML = result.search_results_html;
                    document.getElementById('searchResults').style.display = 'block';
                } else {
                    document.getElementById('searchResults').style.display = 'none';
                }

                if (result.table_html) {
                    document.getElementById('resultsTable').innerHTML = result.table_html;
                }

                const plotsDiv = document.getElementById('plots');
                plotsDiv.innerHTML = `
                    <div class="plot-container" style="max-width: 900px;">
                        <div class="plot-header">
                            <h4>Численное решение u(x,T)</h4>
                        </div>
                        <img src="data:image/png;base64,${result.plot_solution}" alt="Решение">
                    </div>
                `;

                if (result.plot_error) {
                    const errorContainer = document.createElement('div');
                    errorContainer.className = 'plot-container';
                    errorContainer.style.maxWidth = '900px';
                    errorContainer.innerHTML = `
                        <div class="plot-header">
                            <h4>Эволюция L₂ ошибки</h4>
                        </div>
                        <img src="data:image/png;base64,${result.plot_error}" alt="Ошибка">
                    `;
                    plotsDiv.appendChild(errorContainer);
                }

                if (result.plot_energy) {
                    const energyContainer = document.createElement('div');
                    energyContainer.className = 'plot-container';
                    energyContainer.style.maxWidth = '900px';
                    energyContainer.innerHTML = `
                        <div class="plot-header">
                            <h4>Эволюция энергии</h4>
                        </div>
                        <img src="data:image/png;base64,${result.plot_energy}" alt="Энергия">
                    `;
                    plotsDiv.appendChild(energyContainer);
                }

                document.getElementById('plotControls').style.display = 'flex';
                updateMainPlotsLayout();

                if (result.research_plots && result.research_plots.length > 0) {
                    const researchDiv = document.getElementById('researchPlots');
                    let researchHtml = `
                        <div class="param-plots-title">Исследование параметров</div>
                        <div class="param-plot-controls">
                            <button class="param-plot-zoom-btn" onclick="zoomParamPlots('in')">🔍 Увеличить все</button>
                            <button class="param-plot-zoom-btn" onclick="zoomParamPlots('out')">🔍 Уменьшить все</button>
                            <button class="param-plot-zoom-btn" onclick="resetParamPlotsSize()">⟳ Сбросить размер</button>
                            <span class="plot-size-info" id="paramPlotSizeInfo">Текущий размер: 500px</span>
                        </div>
                        <div id="researchPlotsGrid" class="param-plots-grid">
                    `;

                    result.research_plots.forEach((plot, idx) => {
                        researchHtml += `
                            <div class="param-plot-container" style="max-width: 500px;">
                                <div class="param-plot-header">
                                    <h4>${escapeHtml(plot.title)}</h4>
                                </div>
                                <img src="data:image/png;base64,${plot.image}" alt="Исследование">
                            </div>
                        `;
                    });

                    researchHtml += `</div>`;
                    researchDiv.innerHTML = researchHtml;
                    researchDiv.style.display = 'block';
                    updateParamPlotsLayout();
                } else {
                    document.getElementById('researchPlots').style.display = 'none';
                }

                document.getElementById('results').classList.add('show');

            } catch (error) {
                document.getElementById('error').style.display = 'block';
                document.getElementById('error').textContent = '❌ ' + error.message;
                document.getElementById('emptyState').style.display = 'flex';
            } finally {
                document.getElementById('loading').style.display = 'none';
                btn.disabled = false;
                btn.textContent = 'Выполнить расчёт';
            }
        }

        document.addEventListener('DOMContentLoaded', function() {
            updateEquation();
            updateVariableInputs();
            toggleMethodParams();
        });
    </script>
</body>
</html>
'''