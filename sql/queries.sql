import pandas as pd
import sqlite3
import re
import os

def normalize_year(year_val) -> str:
    """
    Standardises year labels to 'YYYY-MM' format.
    Handles inputs like 'Mar-23', 'March-2023', '2023', 'FY23', 'Dec-22'.
    """
    if pd.isna(year_val):
        return year_val
        
    year_str = str(year_val).strip()
    
    # Extract the year part (2 or 4 digits)
    match = re.search(r'(\d{2,4})', year_str)
    if not match:
        return year_str
        
    year_num = match.group(1)
    if len(year_num) == 2:
        year_num = "20" + year_num  # Convert '23' to '2023'
        
    # Default to March unless specified otherwise
    month = "03"
    if "Dec" in year_str or "dec" in year_str.lower():
        month = "12"
    elif "Jun" in year_str or "jun" in year_str.lower():
        month = "06"
        
    return f"{year_num}-{month}"

def build_data_foundation():
    """
    Reads core Excel files, applies ETL transformations, 
    and loads them into the nifty100.db SQLite database.
    """
    db_name = 'nifty100.db'
    conn = sqlite3.connect(db_name)
    
    # Dictionary mapping table names to source files
    core_files = {
        'companies': 'companies.xlsx',
        'profitandloss': 'profitandloss.xlsx',
        'balancesheet': 'balancesheet.xlsx',
        'cashflow': 'cashflow.xlsx',
        'analysis': 'analysis.xlsx',
        'documents': 'documents.xlsx',
        'prosandcons': 'prosandcons.xlsx'
    }
    
    # Track load metrics for audit
    audit_log = []

    for table_name, file_path in core_files.items():
        if not os.path.exists(file_path):
            print(f"Warning: {file_path} not found. Skipping.")
            continue
            
        # 1. Excel loader with header=1 support for all core datasets
        df = pd.read_excel(file_path, header=1)
        initial_rows = len(df)
        
        # 2. Ticker Normaliser: company_id.str.strip().str.upper()
        if 'company_id' in df.columns:
            df['company_id'] = df['company_id'].astype(str).str.strip().str.upper()
        elif table_name == 'companies' and 'id' in df.columns:
            # For companies table, the ticker is in the 'id' column
            df['id'] = df['id'].astype(str).str.strip().str.upper()

        # 3. Year Normaliser & Deduplication
        if table_name == 'documents' and 'Year' in df.columns:
            # Special case for documents.xlsx: Year is calendar year, cast to int
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
            df.drop_duplicates(subset=['company_id', 'Year'], keep='last', inplace=True)
            
        elif 'year' in df.columns:
            # Standard time-series tables (P&L, Balance Sheet, Cash Flow)
            df['year'] = df['year'].apply(normalize_year)
            # Remove duplicate (company_id, year) pairs
            df.drop_duplicates(subset=['company_id', 'year'], keep='last', inplace=True)
            
        # Handle snapshot tables deduplication
        if table_name == 'companies':
            df.drop_duplicates(subset=['id'], keep='last', inplace=True)
        elif table_name == 'analysis':
            df.drop_duplicates(subset=['company_id'], keep='last', inplace=True)
            
        final_rows = len(df)
        rejected_rows = initial_rows - final_rows
        
        # 4. SQLite Loader
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        audit_log.append({
            'table': table_name,
            'rows_in': initial_rows,
            'rows_out': final_rows,
            'rejected': rejected_rows
        })
        print(f"Loaded {table_name}: {final_rows} rows inserted.")

    # Generate load audit log
    audit_df = pd.DataFrame(audit_log)
    audit_df.to_csv('load_audit.csv', index=False)
    print("\nData pipeline completed. Audit log saved to load_audit.csv.")
    
    conn.close()

if __name__ == "__main__":
    build_data_foundation()