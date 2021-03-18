from cmd import Cmd
import re
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

    def help_connect(self):
        print("Attempt to connect to the database. Shorthand: c")

    #TODO: remove after inital testing is complete
    def do_query(self, inp):
        '''execute query. Choose from INSERT, SELECT, and UPDATE. Shorthand q'''
        args = inp.split()
        valInp = False
        query = ''
        try:
            if len(args) > 1:
                print("Executing query as input")
                query = inp
                valInp = True
            elif len(args) == 1:
                if args[0].upper() == "INSERT":
                    tab = input("Insert into table jobs or income?\n")
                    if tab == 'jobs':
                        un = input("Username?\n")
                        emp = input("Employer?\n")
                        hr = input("Hourly rate? Format xx.xx (Optional)\n")
                        tr = input("Tax rate? Format xx.xx (Optional)\n")
                        if un.isalnum() and emp.isalnum():
                            hrchk = re.fullmatch("[0-9]+\.[0-9][0-9]",hr) is not None
                            trchk = re.fullmatch("[0-9]+\.[0-9][0-9]",tr) is not None
                            if hrchk and tr == '':
                                query = "INSERT INTO {table} (username, employer, hourly_rate) VALUES ({user},{employ},{hour}) RETURNING *;".format(table=tab,user=un,employ=emp,hour=hr)
                                valInp = True
                            elif trchk and hr == '':
                                query = "INSERT INTO {table} (username, employer, tax_rate) VALUES ({user},{employ},{tax}) RETURNING *;".format(table=tab,user=un,employ=emp,tax=tr)
                                valInp = True
                            elif hrchk and trchk:
                                query = "INSERT INTO {table} (username, employer, hourly_rate, tax_rate) VALUES ({user},{employ},{hour},{tax}) RETURNING *;".format(table=tab,user=un,employ=emp,hour=hr,tax=tr)
                                valInp = True
                            else:
                                print("Invalid input")
                        else:
                            print("Invalid input")
                    elif tab == 'income':
                        sd = input("Shift date? Format MMM-dd-yyyy\n")
                        emp = input("Employee ID?\n")
                        sl = input("Shift duration? Format PTxHyM where x is hours and y is minutes\n")
                        si = input("Shift income? Format $x[.y] (Optional)\n")
                        
                        sdchk = re.fullmatch("((SEP|APR|JUN|NOV)-([0][1-9]|[12]\\d|30)|(JAN|MAR|MAY|JUL|AUG|OCT|DEC)-([0][1-9]|[12]\\d|3[01])|(FEB)-([0][1-9]|1\\d|2[0-9]))-(\\d\\d\\d\\d)",sd) is not None
                        slchk = re.fullmatch("PT(0?\\d|1\\d|2[0-3])H[0-5]?\\dM",sl) is not None
                        sichk = re.fullmatch("\\$\\d+(.\\d\\d)?",si) is not None
                        
                        if sdchk and emp.isnumeric():
                            if slchk:
                                if si == '':
                                    query = "INSERT INTO {table} (shift_date,emp_id,shift_length) VALUES ('{date}',{empid},'{length}') RETURNING *;".format(table=tab,date=sd,empid=emp,length=sl)
                                    valInp = True
                                elif sichk:
                                    query = "INSERT INTO {table} (shift_date,emp_id,shift_length, shift_income) VALUES ('{date}',{empid},'{length}','{inc}') RETURNING *;".format(table=tab,date=sd,empid=emp,length=sl,inc=si)
                                    valInp = True
                                else:
                                    print("Invalid input")
                            else:
                                print("Invalid input")
                        else:
                            print("Invalid input")
                    else:
                        print("Invalid table")
                elif args[0].upper() == "SELECT":
                    '''needs sanitization'''
                    query = input("Selection query? Format as full query, e.g SELECT * FROM jobs;\n")
                    valInp = True
                elif args[0].upper() == "UPDATE":
                    '''needs some sanitization'''
                    tab = input("Update in table jobs or income?\n")
                    if tab == 'jobs':
                        more = True
                        query = "UPDATE {table}".format(table=tab)
                        while(more):
                            col = input("Set column? Choose one:  username, employer, hourly_rate, tax_rate\n")
                            if col.lower() == 'username' or col.lower() == 'employer' or col.lower() == 'hourly_rate' or col.lower() == 'tax_rate':
                                upd = input("New value?\n")
                                nmchk = re.fullmatch("\\d?\\d(.\\d*)?",upd) is not None
                                if (col.lower() == 'username' or col.lower() == 'employer') and upd.isalnum():
                                    query += " SET {column} = {update}".format(column=col,update=upd)
                                elif (col.lower() == 'hourly_rate' or col.lower() == 'tax_rate') and nmchk:
                                    query += " SET {column} = {update:.2f}".format(column=col,update=upd)
                                else:
                                    print("Invalid data, input rejected")
                            else:
                                print("Invalid column, input rejected")
                            moreInp = input("More changes for this row? y/n\n")
                            if moreInp == 'y':
                                more = True
                                query += ","
                            else:
                                more = False
                        where = input("Conditional update? y/n\n")
                        if where == 'y':
                            cond = input("Condition?\n") #sanitize this
                            query += " WHERE {condition} RETURNING *;".format(condition=cond)
                        else:
                            query += " RETURNING *;"
                        valInp = True
                    elif tab == 'income':
                        more = True
                        query = "UPDATE {table}".format(table=tab)
                        while(more):
                            col = input("Set column? Choose one:  shift_date, emp_id, shift_length, shift_income\n")
                            if col.lower() == 'shift_date' or col.lower() == 'emp_id' or col.lower() == 'shift_length' or col.lower() == 'shift_income':
                                upd = input("New value?\n")
                                sdchk = re.fullmatch("((SEP|APR|JUN|NOV)-([0][1-9]|[12]\\d|30)|(JAN|MAR|MAY|JUL|AUG|OCT|DEC)-([0][1-9]|[12]\\d|3[01])|(FEB)-([0][1-9]|1\\d|2[0-9]))-(\\d\\d\\d\\d)",upd) is not None
                                slchk = re.fullmatch("PT(0?\\d|1\\d|2[0-3])H[0-5]?\\dM",upd) is not None
                                sichk = re.fullmatch("\\$\\d+(.\\d\\d)?",upd) is not None
                                
                                if col.lower() == 'shift_date' and sdchk:
                                    query += " SET {column} = '{update}'".format(column=col,update=upd)
                                elif col.lower() == 'emp_id' and upd.isnumeric():
                                    query += " SET {column} = {update}".format(column=col,update=upd)
                                elif col.lower() == 'shift_length' and slchk:
                                    query += " SET {column} = '{update}'".format(column=col,update=upd)
                                elif col.lower() == 'shift_income' and sichk:
                                    query += " SET {column} = '{update}'".format(column=col,update=upd)
                                else:
                                    print("Invalid data, input rejected")
                            else:
                                print("Invalid column, input rejected")
                            moreInp = input("More changes for this row? y/n\n")
                            if moreInp == 'y':
                                more = True
                                query += ","
                            else:
                                more = False
                        where = input("Conditional update? y/n\n")
                        if where == 'y':
                            cond = input("Condition?\n") #sanitize this
                            query += " WHERE {condition} RETURNING *;".format(condition=cond)
                        else:
                            query += " RETURNING *;"
                        valInp = True
                    else:
                        print('invalid table')
                else:
                    print("Option {} not recognized".format(args[0]))
            else:
                print("Command 'query' requires further arguments")
            if self.connection is not None and valInp:
                if query[-1] != ';':
                    query += ';'
                print(query)
                result = Database.execute_query(self.connection, query)
                for r in result:
                    print(r)
            elif not valInp:
                print("Invalid input")
            else:
                print("Connection to database not yet established. Execute 'connect' first.")
        except Exception as e:
            print("Error: {}".format(e))
    
    def help_query(self):
        print("Execute query. Choose from INSERT, SELECT, and UPDATE. Shorthand: q <query>")
    
    def default(self, inp):
        inpList = inp.split()
        command = inpList[0]
        if command == 'z':
            return self.do_exit(inp)
        elif command == 'c':
            return self.do_connect(inp)
        elif command == 'q':
            return self.do_query(" ".join(inpList[1:]))
        else:
            print("Default: {}. Arguments: {}".format(command, inp))