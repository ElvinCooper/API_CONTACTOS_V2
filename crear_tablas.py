import psycopg2

try:
    conn = psycopg2.connect(
        dbname="mycontacts",
        user="contacts",
        password="KYEpostgres301020",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa")
    conn.close()
except Exception as e:
    print(f"Error: {e}")