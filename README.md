# Анализатор сложности текста

Веб-сервис для анализа сложности текста с использованием базовых NLP-метрик и визуализации. Разработан с использованием Django и Pandas.

**Demo:** (https://text-complexity-analyzer.onrender.com)

## Технологии
*   **Python 3.10+**
*   **Django 6.0**
*   **Pandas** (Text analysis)
*   **Matplotlib** (Data visualization)
*   **Bootstrap 5** (UI Framework)

## Возможности
1.  **Каталог текстов**: просмотр текстов по категориям.
2.  **Анализ сложности:**: автоматический подсчёт количества слов и предложений.
3.  **Визуализация:**: гистограмма распределения длины слов для каждого текста.
4.  **Управление**:добавление новых текстов с тегами и категориями.

## Скриншоты
<img width="1470" height="831" alt="image" src="https://github.com/user-attachments/assets/b9012c29-d1bc-4a9a-9365-7740b9d11dc5" />
<img width="1470" height="831" alt="image" src="https://github.com/user-attachments/assets/492e8f70-5655-4f03-972c-c758cf994667" />

- **Dashboard**:список всех текстов.
- **Analysis View**:отображение текста и графика Matplotlib.

## Запуск проекта локально

1.  **Клонировать репозиторий:**
    ```bash
    git clone https://github.com/yourusername/text_complexity_analyzer.git
    cd text_complexity_analyzer
    ```

2.  **Создать и активировать виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Установить зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Применить миграции и загрузить тестовые данные:**
    ```bash
    python manage.py migrate
    python manage.py seed_data
    ```

5.  **Запустить сервер:**
    ```bash
    python manage.py runserver
    ```

6.  **Открыть приложение:**
    Open (https://text-complexity-analyzer.onrender.com)
