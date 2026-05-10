# 🎬 Netflix Show Insights Dashboard

A premium, interactive Streamlit dashboard designed to explore and analyze Netflix's vast catalog of movies and TV shows. This project enhances data visualization with modern aesthetics and deep-dive features.

## 🚀 Features

-   **Netflix-Inspired UI:** Dark mode aesthetics with vibrant red accents and responsive tabbed navigation.
-   **Interactive Filtering:** Filter content by Type (Movie/TV Show), Release Year, and Maturity Ratings.
-   **Comprehensive Analytics:**
    -   **Overview:** Track trends of content added over time and global distribution.
    -   **Cast & Creators:** Deep dive into the top 10 most featured actors and directors.
    -   **Maturity Trends:** Analyze content volume across different age ratings.
-   **Live Data Explorer:** Search and browse individual titles with details on cast, director, and genres.

## 📊 Sample View

*(The dashboard features a multi-tab interface with high-performance Plotly charts and a custom-styled Streamlit UI.)*

## 🛠️ Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MueezRiz/netflix-dashboard-dashboard.git
    cd netflix-dashboard-dashboard
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install streamlit pandas plotly
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

-   `app.py`: Main Streamlit application with custom CSS and logic.
-   `netflix_cleaned.csv`: Preprocessed dataset used for the dashboard.
-   `netflix_preprocessing.ipynb`: Jupyter notebook containing the data cleaning pipeline.
-   `.gitignore`: Properly configured to exclude virtual environments and cache.

---
Developed as a sample project for Netflix Data Analysis.
