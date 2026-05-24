# GameMatch

Сайт подбора игр по характеристикам ПК на **Flask** (Python). Готов к деплою на **Vercel**.

## Возможности

- Форма: CPU, GPU, RAM, тип накопителя
- 24 популярные игры с минимальными и рекомендуемыми требованиями
- Результат: «на высоких», «на средних», «только минимум» или «не потянет»

## Локальный запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Откройте http://127.0.0.1:5000

Или через Vercel CLI (рекомендуется перед деплоем):

```bash
npm i -g vercel
vercel dev
```

## Деплой на Vercel

**Важно:** `app.py`, `pyproject.toml` и `requirements.txt` должны быть в **корне** репозитория, а не во вложенной папке (например `Q/`).

1. Загрузите проект в GitHub — файлы в корне, без лишней вложенной папки.
2. На [vercel.com](https://vercel.com) → **Add New Project** → импортируйте репозиторий.
3. **Framework Preset:** Other (или Flask, если есть).
4. **Root Directory:** оставьте пустым (`.`), если код в корне. Если код уже в подпапке `Q` — укажите `Q`.
5. Нажмите **Deploy**.

### Если сборка ~25 ms и сайт не открывается

Это значит, Vercel не нашёл Flask-приложение. Проверьте:

| Проблема | Решение |
|----------|---------|
| Код в папке `Q/`, а не в корне | **Settings → Root Directory → `Q`** и Redeploy, **или** перенесите файлы в корень репозитория |
| Нет `app.py` в корне (или в Root Directory) | Должен быть файл с `app = Flask(__name__)` |
| Загружен только README | Запушьте весь проект: `app.py`, `templates/`, `public/`, `data/`, `services/` |
| В репозитории есть `__pycache__` | Удалите и добавьте в `.gitignore` |

Через CLI:

```bash
vercel
```

### Структура для Vercel

| Файл / папка      | Назначение                          |
|-------------------|-------------------------------------|
| `app.py`          | Точка входа Flask (`app`)           |
| `requirements.txt`| Зависимости Python                  |
| `templates/`      | HTML-шаблоны Jinja2                 |
| `public/css/`     | Статика (CSS) — раздаётся с CDN     |

Статические файлы лежат в `public/`, как требует [документация Vercel для Flask](https://vercel.com/docs/frameworks/backend/flask).

## Стек

- Python 3.12+
- Flask 3.1
- Jinja2 templates
