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

1. Загрузите проект в GitHub (или используйте папку локально).
2. На [vercel.com](https://vercel.com) → **Add New Project** → импортируйте репозиторий.
3. Vercel автоматически определит Flask по `app.py` и `requirements.txt`.
4. Нажмите **Deploy**.

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
