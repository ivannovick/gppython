import psycopg2

try:
    connection = psycopg2.connect(database = "postgres")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE if exists food")
    cursor.execute("CREATE TABLE food(name text, about text, price float)")

    cursor.execute("""INSERT INTO food (name, about, price) 
                      VALUES (%s, %s, %s)
                   """, 
                   ('lemon',  'sour citrus fruit', 1.05))

    connection.commit()

    cursor.execute("SELECT * FROM food;")
    print("FOOD LIST: ")
    for record in cursor:
        print(record)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
