import psycopg2
from psycopg2 import Error
import textwrap

def database(temp, humi, date):
    try:
        cred2 = open('cred','r')
        cred = cred2.readline()
        cred = cred.split(';')

        connection = psycopg2.connect(user=cred[0],
                                      password=cred[1],
                                      host=cred[2],
                                      port=cred[3],
                                      database=cred[4])


        cursor = connection.cursor()
        postgres_insert_query = """INSERT INTO data(temp,hum,timedate) VALUES (%s,%s,%s)"""
        record_to_insert = (temp,humi,date)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, Error) as error:
        print(error)
    finally:
        if (connection):
            cred2.close()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
