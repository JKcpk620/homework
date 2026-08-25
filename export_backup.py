import os
import sys
import psycopg2
from datetime import datetime
from dotenv import load_dotenv  # 引入 dotenv

# 載入 .env 檔案
load_dotenv()

PROJECT_NAME = "CheungPuiKei_webpage"
EXPORT_LIST = [
    ('export', 'auth_user', 'users_backup.csv'),
    ('export', 'merchants_merchant', 'merchants_backup.csv'),
    ('export', 'f_and_b_f_and_b', 'f_and_b_backup.csv'),
    ('export', 'products_product', 'products_backup.csv'),
]

def export_table_to_csv(table_name, file_name):
    today_str = datetime.now().strftime('%Y%m%d')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'backups', 'export', today_str)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, file_name)

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432')
        )
        with conn.cursor() as cur:
            sql = f"COPY {table_name} TO STDOUT WITH CSV HEADER DELIMITER ','"
            print(f"📋 Exporting {table_name} -> {file_name} ...")
            with open(output_path, 'w', encoding='utf-8') as f:
                cur.copy_expert(sql, f)
            print(f" 🎉 Success！Path: {output_path}")
    except Exception as e:
        print(f" ❌ Fail to export {table_name}: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print(f"🚀 Start batch export task ({len(EXPORT_LIST)} tables)...")
    for action, table_name, file_name in EXPORT_LIST:
        if action == 'export':
            export_table_to_csv(table_name, file_name)
        else:
            print(f"⚠️ Unknown action '{action}' for table {table_name}, skipped.")
    print("\n🏁 All export tasks finished.")
