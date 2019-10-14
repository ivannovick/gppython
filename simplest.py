import psycopg2

try:
    # You can also explicitly pass parameters like username, password,etc
    # this code assumes PGHOST, PGPASSWORD, PGUSER are set in environment
    connection = psycopg2.connect(database = "postgres")

    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        connection.close()
        print("PostgreSQL connection is closed")
