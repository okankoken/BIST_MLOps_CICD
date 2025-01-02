import mysql.connector

def save_predictions_to_mysql(stock_name: str, stock_name_full: str, prediction):
    # MySQL baglanti bilgileri
    db_config = {
        'user': 'root',
        'password': 'Ankara06',  # Sifreyi güncelleyin
        'host': '172.18.0.3',  # MySQL container IP'si
        'database': 'mlops_db'
    }

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Tabloyu olusturma
        create_table_query = """
        CREATE TABLE IF NOT EXISTS bist_predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            stock_name VARCHAR(255) NOT NULL,
            stock_name_full VARCHAR(255) NOT NULL,
            prediction FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)

        # Tahminleri ekleme
        insert_query = """
        INSERT INTO bist_predictions (stock_name, stock_name_full, prediction)
        VALUES (%s, %s, %s);
        """
        # Prediction'u Python float'a dönüstür
        cursor.execute(insert_query, (stock_name, stock_name_full, float(prediction)))

        connection.commit()
        print(f"MySQL'e veri eklendi: {stock_name}, {stock_name_full}, {prediction}")

    except mysql.connector.Error as err:
        print(f"MySQL Hatasi: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
