import psycopg2

try:
    # You can also explicitly pass parameters like username, password,etc
    # this code assumes PGHOST, PGPASSWORD, PGUSER are set in environment
    connection = psycopg2.connect(database = "postgres")

    cursor = connection.cursor()
    cursor.execute("DROP TABLE if exists food")
    cursor.execute("CREATE TABLE food(name text, about text, price float)")
    cursor.execute("INSERT into food values('banana', 'long yellow sweet fruit', '.50')")
    cursor.execute("INSERT into food values('lemon',  'sour citrus fruit', '1.05')")
    cursor.execute("INSERT into food values('hotdog', 'long thing meat sandwich', '2.50')")
    cursor.execute("INSERT into food values('corndog','carnival food', '3.00')")
    cursor.execute("INSERT into food values('coffee', 'hot beverage', '2.75')")
    cursor.execute("INSERT into food values('hotdog', 'long thing meat sandwich', '2.50')")
    cursor.execute("SELECT * FROM food")

    print(cursor.description)
    print("Row Count: ", cursor.rowcount)

    for record in cursor:
        print (record)


except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
