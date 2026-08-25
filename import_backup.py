import os
import sys
import psycopg2
from dotenv import load_dotenv


load_dotenv()

IMPORT_LIST = [
    (
        'users_backup.csv', 
        'auth_user', 
        ['id', 'password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined'],
        ['password', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined']
    ),
    (
        'merchants_backup.csv', 
        'merchants_merchant', 
        [
            'id', 'title', 'district', 'address', 'type', 'cuisine_choices', 
            'acommodate', 'has_wifi', 'has_delivery', 'average_spend', 
            'promo_badge_text', 'accept_reservations', 'pre_order', 
            'catering_service', 'contact_number', 'has_Whatspp', 'opening_hours', 
            'closing_hours', 'rating', 'description', 'signature_dish', 
            'sign_dish_photo1', 'sign_dish_photo2', 'sign_dish_photo3', 
            'photo_main', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 
            'photo6', 'is_published', 'list_date'
        ], 
        [
            'title', 'district', 'address', 'type', 'cuisine_choices', 
            'acommodate', 'has_wifi', 'has_delivery', 'average_spend', 
            'promo_badge_text', 'accept_reservations', 'pre_order', 
            'catering_service', 'contact_number', 'has_Whatspp', 'opening_hours', 
            'closing_hours', 'rating', 'description', 'signature_dish', 
            'sign_dish_photo1', 'sign_dish_photo2', 'sign_dish_photo3', 
            'photo_main', 'photo1', 'photo2', 'photo3', 'photo4', 'photo5', 
            'photo6', 'is_published', 'list_date'
        ]
    ),
    (
        'f_and_b_backup.csv', 
        'f_and_b_f_and_b', 
        [
            'id', 'title', 'discription', 'F_or_b', 'cooking_type', 
            'beverage_type', 'veggie', 'halal', 'spicy', 'allegy_ingredient', 
            'price', 'photo_main', 'is_published', 'list_date'
        ],
        [
            'title', 'discription', 'F_or_b', 'cooking_type', 
            'beverage_type', 'veggie', 'halal', 'spicy', 'allegy_ingredient', 
            'price', 'photo_main', 'is_published', 'list_date'
        ]
    ),
    (
        'products_backup.csv', 
        'products_product', 
        [
            'id', 'title', 'discription', 'origin', 'package_size', 
            'type', 'price', 'photo_main', 'is_published', 'list_date'
        ], 
        [
            'title', 'discription', 'origin', 'package_size', 
            'type', 'price', 'photo_main', 'is_published', 'list_date'
        ]
    ),
]

def upsert_csv_to_table(csv_filename, table_name, all_fields, non_pk_fields):
    """
    High-performance CSV Upsert into a PostgreSQL table using psycopg2.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'backups', 'import', csv_filename)
    
    if not os.path.exists(csv_path):
        print(f"  ❌ Error: Source CSV file not found at: {csv_path}")
        return

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
            print(f"  🔄 Creating in-memory temporary table for {table_name}...")
            cur.execute(f"CREATE TEMP TABLE temp_{table_name} AS SELECT * FROM {table_name} WITH NO DATA;")
            
            print(f"  ⚡ Piping {csv_filename} data into temporary table at high speed...")
            
            fields_joined = ", ".join([f'"{f}"' for f in all_fields])
            copy_sql = f"COPY temp_{table_name} ({fields_joined}) FROM STDOUT WITH CSV HEADER DELIMITER ','"
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                cur.copy_expert(copy_sql, f)
            
            fields_str = ", ".join([f'"{f}"' for f in all_fields])
            set_str = ", ".join([f'"{f}" = EXCLUDED."{f}"' for f in non_pk_fields])
            
            upsert_sql = f"""
                INSERT INTO {table_name} ({fields_str})
                SELECT {fields_str} FROM temp_{table_name}
                ON CONFLICT (id) 
                DO UPDATE SET {set_str};
            """
            
            print(f"  💾 Executing data alignment (Updating old records / Inserting new ones)...")
            cur.execute(upsert_sql)
            
            print(f"  🔧 Adjusting auto-increment ID sequences for {table_name}...")
            cur.execute(f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), COALESCE(max(id), 1)) FROM {table_name};")
            
        conn.commit()
        print(f"  🎉 Success! Table '{table_name}' has been safely synchronized.")
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"  ❌ Task execution failed. Transaction safely rolled back. Error: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print(f"🚀 Starting batch import (Upsert) tasks for {len(IMPORT_LIST)} files...")
    
    for csv_file, table, fields, non_pks in IMPORT_LIST:
        print(f"\n▶️ Processing: {csv_file}")
        upsert_csv_to_table(csv_file, table, fields, non_pks)
        
    print("\n🏁 All batch import operations finished.")
