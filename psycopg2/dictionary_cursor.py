import psycopg2
import psycopg2.extras

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

    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DROP TABLE if exists food")
    cursor.execute("CREATE TABLE food(name text, about text, price float)")

    query = "INSERT INTO food (name, about, price) VALUES (%s, %s, %s)"
    cursor.executemany(query, food)
    connection.commit()

    cursor.execute("SELECT * FROM food;")
    print("FOOD LIST: ")
    for record in cursor:
        print("Product: ", record['name'], " $", record['price'],sep="")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
