CREATE TABLE IF NOT EXISTS employees (
    "Employee ID" INT PRIMARY KEY,
    "First Name" VARCHAR(100),
    "Last Name" VARCHAR(100),
    "Date of Birth" DATE,
    City VARCHAR(100)
);

create TABLE if not EXISTS emp_cdc (
  cdc_id SERIAL PRIMARY KEY,
  "Employee ID" INT, 
  "First Name" VARCHAR(100), 
  "Last Name" VARCHAR(100),
  "Date of Birth" DATE, 
  City VARCHAR(100),
  "Action" VARCHAR(100)
);

/* Set up the trigger */
CREATE OR REPLACE FUNCTION log_employee_changes()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    INSERT INTO emp_cdc("Employee ID", "First Name", "Last Name", "Date of Birth", City, "Action")
    VALUES (OLD."Employee ID", OLD."First Name", OLD."Last Name", OLD."Date of Birth", OLD.City, 'DELETE');
  ELSIF TG_OP = 'UPDATE' THEN
    INSERT INTO emp_cdc("Employee ID", "First Name", "Last Name", "Date of Birth", City, "Action")
    VALUES (NEW."Employee ID", NEW."First Name", NEW."Last Name", NEW."Date of Birth", NEW.City, 'UPDATE');
  ELSIF TG_OP = 'INSERT' THEN
    INSERT INTO emp_cdc("Employee ID", "First Name", "Last Name", "Date of Birth", City, "Action")
    VALUES (NEW."Employee ID", NEW."First Name", NEW."Last Name", NEW."Date of Birth", NEW.City, 'INSERT');
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER employee_cdc_trigger
AFTER INSERT OR UPDATE OR DELETE ON employees
FOR EACH ROW EXECUTE FUNCTION log_employee_changes();

select * from emp_cdc;

/* test if trigger works */
INSERT INTO employees
("Employee ID", "First Name", "Last Name", "Date of Birth", City)
VALUES
(1, 'Max', 'Smith',	'2002-02-03', 'Sydney');

select * from emp_cdc;

/* add the remaining two rows to test update and delete */
INSERT INTO employees
("Employee ID", "First Name", "Last Name", "Date of Birth", City)
VALUES
(2, 'Karl',	'Summers', '2004-04-10', 'Brisbane');

INSERT INTO employees
("Employee ID", "First Name", "Last Name", "Date of Birth", City)
VALUES
(3, 'Sam', 'Wilde', '2005-02-06', 'Perth');

/* UPDATE: id=2, dob-> 2004-03-10 */
update employees
set "Date of Birth"='2004-03-10'
where "Employee ID"=2;

/* DELETE: id=3 */
delete from employees
where "Employee ID" = 3;


