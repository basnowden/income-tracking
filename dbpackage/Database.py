import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print("The error '{}' has occurred".format(e))
    except Exception as e:
        print("Error: {}".format(e))
    return connection

def create_database(connection, query, dbname):
    connection.autocommit = True
    cursor = connection.cursor()
    check_database_query = "SELECT datname FROM pg_catalog.pg_database WHERE datname = '{}';".format(dbname)
    try:
        cursor.execute(check_database_query)
        result = cursor.fetchall()
        db_exists = False
        for r in result:
            if r[0] == dbname:
                db_exists = True
        if not db_exists:
            cursor.execute(query)
            print("Database created successfully")
        else:
            print("Database already established")
        cursor.close()
    except OperationalError as e:
        print("The error '{}' has occurred".format(e))
        raise
    except Exception as e:
        print("Unexpected Error {}".format(e))
        raise

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        if query.split()[0] != 'UPDATE':
            result = cursor.fetchall()
        else:
            result = []
        cursor.close()
        connection.commit()
        return result
    except Exception as e:
        print("Error: {}".format(e))
        raise
