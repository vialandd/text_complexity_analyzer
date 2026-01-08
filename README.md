# Text Complexity Analyzer

A web-based service for analyzing text complexity using basic NLP metrics and visualization. Built with Django and Pandas.

**Live Demo:** [Link to your PythonAnywhere app]

## Technologies
*   **Python 3.10+**
*   **Django 6.0**
*   **Pandas** (Text analysis)
*   **Matplotlib** (Data visualization)
*   **Bootstrap 5** (UI Framework)

## Features
1.  **Text Catalog**: Browse texts by category.
2.  **Complexity Analysis**: Automatic calculation of word count and sentence count.
3.  **Visualization**: Histogram of word length distribution for each text.
4.  **Management**: Add new texts with tags and categories.

## Screenshots

*(Placeholder for screenshots)*
- **Dashboard**: Lists all texts.
- **Analysis View**: Shows text content and Matplotlib graph.

## How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/text_complexity_analyzer.git
    cd text_complexity_analyzer
    ```

2.  **Set up Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations and Seed Data:**
    ```bash
    python manage.py migrate
    python manage.py seed_data
    ```

5.  **Run Server:**
    ```bash
    python manage.py runserver
    ```

6.  **Access App:**
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000)
