import psycopg2

food = (
    ('banana', 'long yellow sweet fruit', '.50'),
    ('lemon',  'sour citrus fruit', '1.05'),
    ('hotdog', 'long thing meat sandwich', '2.50'),
    ('corndog','carnival food', '3.00'),
    ('coffee', 'hot beverage', '2.75'),
    ('hotdog', 'long thing meat sandwich', '2.50')
)
 
try:
    connection = psycopg2.connect(database = "postgres")

    cursor = connection.cursor()
    cursor.execute("DROP TABLE if exists food")
    cursor.execute("CREATE TABLE food(name text, about text, price float)")

    query = "INSERT INTO food (name, about, price) VALUES (%s, %s, %s)"
    cursor.executemany(query, food)
    connection.commit()

    cursor.execute("SELECT * FROM food")
    print("SELECT * FROM food;")
    for record in cursor:
        print (record)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
