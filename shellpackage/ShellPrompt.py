from cmd import Cmd
from dbpackage import Database

dbname = "it_app"

class ShellPrompt(Cmd):
    prompt = 'it> '
    intro = "Welcome! Type ? to list commands"
    connection = None
    
    def preloop(self):
        print("Establishing database")
        try:
            internal_connection = Database.create_connection("postgres", "postgres", "abc123", "127.0.0.1", "5432")
            create_database_query = "CREATE DATABASE {}".format(dbname)
            Database.create_database(internal_connection, create_database_query, dbname)
        except Exception as e:
            print("Error '{}' has occurred".format(e))

    def do_exit(self, inp):
        '''exit the application. Shorthand z'''
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            print("Connection closed")
        print("Bye")
        return True
    
    def help_exit(self):
        print("Safely exit the prompt. Shorthand: z")
    
    def do_say(self, inp):
        '''print the input text in single quotes.'''
        print("'{}'".format(inp))

    def help_say(self):
        print("Print the provided text")
    
    def do_connect(self, inp):
        '''attempt to connect to database. Shorthand c'''
        print("Opening connection")
        if self.connection is None:
            try:
                self.connection = Database.create_connection("it_app", "postgres", "abc123", "127.0.0.1", "5432")
            except Exception as e:
                print("Error: {}".format(e))
        else:
            print("Connection already established")

    #TODO: remove after inital testing is complete
    def do_query(self, inp):
        '''execute query. Shorthand q'''
        try:
            print("Executing query")
            if self.connection is not None:
                result = Database.execute_query(self.connection, inp)
                for r in result:
                    print(r)
            else:
                print("Connection to database not yet established. Execute 'connect' first.")
        except Exception as e:
            print("Error: {}".format(e))
    
    def default(self, inp):
        if inp == 'z':
            return self.do_exit(inp)
        elif inp == 'c':
            return self.do_connect(inp)
        elif inp == 'q':
            return self.do_query(inp)
        else:
            print("Default: {}".format(inp))