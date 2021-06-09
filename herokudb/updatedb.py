import psycopg2
from psycopg2 import Error
import textwrap

try:
    cred2 = open('cred','r')
    cred = cred2.readline()
    cred = cred.split(';')
    print(cred[0])
    print(cred[1])
    #print(cred[1])

    # Connect to an existing database
    print(cred[4])
    connection = psycopg2.connect(user=cred[0],
                                  password=cred[1],
                                  host=cred[2],
                                  port=cred[3],
                                  database=cred[4])

   
    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    #cursor.execute("SELECT version();")
    # Fetch result
    #record = cursor.fetchone()
    #print("You are connected to - ", record, "\n")
    postgres_insert_query = """INSERT INTO data(temp,hum,timedate) VALUES (%s,%s,%s)"""
    record_to_insert = ('21','10','2021/06/09 13:37:00')
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into table")
    #cred2.close()

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cred2.close()
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")