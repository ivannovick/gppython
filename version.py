import psycopg2

try:
    # You can also explicitly pass parameters like username, password,etc
    # this code assumes PGHOST, PGPASSWORD, PGUSER are set in environment
    connection = psycopg2.connect(database = "postgres")

    cursor = connection.cursor()

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("VERSION: ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
