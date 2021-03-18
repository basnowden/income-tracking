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
- [ ] Create GUI


Database Schema:
TABLE users(  
	username VARCHAR(30) NOT NULL,  
	admin BOOLEAN,  
	PRIMARY KEY(username)  
);  

TABLE jobs(  
	emp_id INT GENERATED ALWAYS AS IDENTITY,  
	username VARCHAR(30) NOT NULL,  
	employer VARCHAR(30) NOT NULL,  
	hourly_rate FLOAT(2),  
	tax_rate FLOAT,  
	PRIMARY KEY(emp_id),  
	FOREIGN KEY(username)  
		REFERENCES users(username)  
);  

TABLE income(  
	shift_id INT GENERATED ALWAYS AS IDENTITY,  
	shift_date DATE NOT NULL DEFAULT CURRENT_DATE,  
	emp_id INT NOT NULL,  
	shift_length INTERVAL HOUR TO MINUTE,  
	shift_income MONEY,  
	PRIMARY KEY(shift_id),  
	FOREIGN KEY(emp_id)  
		REFERENCES jobs(emp_id)  
);  
