# income-tracking
Brady Snowden

This project will be for tracking income by shift, company, and employee. It is intended for personal use on a Windows computer at this time.

Successful execution of this program assumes that PostgreSQL is installed and running on the local machine.

TODO:
- [x] Setup Git repository
- [x] Setup basic command line shell
- [x] Setup database
- [x] Store initial data
- [ ] Implement search functions
- [ ] Automated testing
- [ ] Create GUI


Database Schema:
TABLE users(  
&nbsp;&nbsp;&nbsp;&nbsp;username VARCHAR(30) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;admin BOOLEAN,  
&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY(username)  
);  

TABLE jobs(  
&nbsp;&nbsp;&nbsp;&nbsp;emp_id INT GENERATED ALWAYS AS IDENTITY,  
&nbsp;&nbsp;&nbsp;&nbsp;username VARCHAR(30) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;employer VARCHAR(30) NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;hourly_rate FLOAT(2),  
&nbsp;&nbsp;&nbsp;&nbsp;tax_rate FLOAT,  
&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY(emp_id),  
&nbsp;&nbsp;&nbsp;&nbsp;FOREIGN KEY(username)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;REFERENCES users(username)  
);  

TABLE income(  
&nbsp;&nbsp;&nbsp;&nbsp;shift_id INT GENERATED ALWAYS AS IDENTITY,  
&nbsp;&nbsp;&nbsp;&nbsp;shift_date DATE NOT NULL DEFAULT CURRENT_DATE,  
&nbsp;&nbsp;&nbsp;&nbsp;emp_id INT NOT NULL,  
&nbsp;&nbsp;&nbsp;&nbsp;shift_length INTERVAL HOUR TO MINUTE,  
&nbsp;&nbsp;&nbsp;&nbsp;shift_income MONEY,  
&nbsp;&nbsp;&nbsp;&nbsp;PRIMARY KEY(shift_id),  
&nbsp;&nbsp;&nbsp;&nbsp;FOREIGN KEY(emp_id)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;REFERENCES jobs(emp_id)  
);  
