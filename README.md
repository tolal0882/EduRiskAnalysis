# EduRisk Analysis

EduRisk Analysis is a simple Streamlit web app for a student risk monitoring dashboard. It presents student performance data, summary metrics, and a basic interactive interface for exploring academic risk information.

## Features

- Student dashboard overview
- Summary metrics for score and attendance
- Interactive page navigation using the Streamlit sidebar
- Data table view of student records
- Risk indicators based on low academic performance
- Student data loaded from `students.csv` with Pandas
- Data inspection showing dataset shape, columns, and first five rows
- Clear error message when `students.csv` is missing

## Tech Stack

- Python
- Streamlit
- pandas

## Project Structure

- `app.py` - main Streamlit application
- `data/students.csv` - student records loaded by the app
- `requirements.txt` - Python dependencies
- `styles/` - reusable app styling, charts, tables, and components

## Installation

1. Clone the repository
2. Create a virtual environment
3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

## About this Project

This project is a beginner-friendly lab assignment for a Web App Development for Data Science course.

## License

This project is for educational use.
