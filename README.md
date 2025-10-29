# 🧹 Data Cleaner App

A simple yet powerful **data preprocessing web app** built with [Shiny for Python](https://shiny.posit.co/py/).  

It allows users to upload CSV files, clean missing values, transform columns, and download the cleaned dataset — all interactively.

---

🧠 This project was created as a personal learning exercise during my second year of studying Artificial Intelligence, to practice building maintainable and testable data tools.

---

## 🚀 Features

- 📁 Upload CSV files easily
- 🧮 Handle missing values with multiple strategies:
  - Replace with zero
  - Replace with column mean or median
  - Drop rows with missing values
- 📊 Normalize or standardize numeric columns
- 🔍 Quick data analysis (column types, missing counts, unique values)
- 💾 Download the cleaned dataset
- 🌗 Light/Dark mode interface

---

## 🧰 Tech Stack

| Component            | Description              |
| -------------------- | ------------------------ |
| **Python**           | Core language            |
| **Shiny for Python** | Web interface framework  |
| **Pandas & NumPy**   | Data manipulation        |
| **Scikit-learn**     | Scaling & transformation |
| **Pytest**           | Unit testing framework   |

---

## 🧪 Testing

All core data utilities are tested with `pytest` to ensure correctness and reliability.

```bash
pytest -v
```
---

✅ All 9 tests passed — including handling of edge cases for missing values and transformations.

---

## 🖥️ Run Locally

1. Clone the repository
```bash
git clone https://github.com/kimianili00/data-cleaner-app.git
cd data-cleaner-app

2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows


3. Install dependencies
pip install -r requirements.txt


4. Run the app
python -m src.app
```
---

Then open your browser at http://localhost:8000

---

## 🧩 Project Structure
```bash
data_cleaner_app/
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── ui_layout.py
│   ├── server_logic.py
│   └── data_utils.py
│
├── tests/
│   ├── __init__.py
│   └── test_data_utils.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```
---

## 📄 License

This project is released under the MIT License.

---

## ✨ Author

Kimia Nili
📧 Kimianili00@gmail.com
💼 [Linkedin](https://www.linkedin.com/in/kimia-nili-826b0038b/)
🧠 Focused on building clean, maintainable, and test-driven data tools.

