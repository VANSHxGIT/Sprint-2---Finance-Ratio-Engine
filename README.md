# 📈 Finance Ratio Engine (Sprint 2)

A Python project for calculating and analyzing financial ratios for Nifty 100 companies.

## 🚀 Features
- **Core Analytics**: Calculation engine for key financial metrics.
- **Data Management**: Uses SQLite (`nifty100.db`) for robust data handling.
- **Database Inspection**: Built-in script to verify database integrity and view tables.

## 🛠️ Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```
2. **Activate the virtual environment:**
   - **Windows:** `.venv\Scripts\activate`
   - **Linux/Mac:** `source .venv/bin/activate`
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure
- `src/`: Core analytics and calculation engine.
- `tests/`: Unit tests (run with `pytest`).
- `data/` & `database/`: Data sources and SQLite databases (e.g., `nifty100.db`).
- `outputs/`: Generated analysis and log files.

## 💡 Usage

### Run the Core Engine
Execute the main application to generate financial ratios:
```bash
python run_ratio_engine.py
```

### Inspect the Database
To view the tables and row counts inside the local SQLite database:
```bash
python inspect_db.py
```

### Run Tests
To ensure everything is working correctly, run the test suite:
```bash
pytest
```
