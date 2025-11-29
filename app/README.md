# Streamlit App

This Streamlit app demonstrates a simple file uploader and data preview for CSV, Excel, and JSON files.

Prerequisites
- Python 3.8+

Install dependencies and run:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
streamlit run app.py
```

Upload a CSV, Excel (.xls/.xlsx), or JSON file and the app will attempt to parse it into a `pandas` DataFrame, show a preview and basic stats, and allow downloading as CSV.
