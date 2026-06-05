CREATE TABLE IF NOT EXISTS employees (
    "Employee ID" SERIAL PRIMARY KEY,
    "First Name" VARCHAR(100),
    "Last Name" VARCHAR(100),
    "Date of Birth" DATE,
    City VARCHAR(100)
);

/* see if the three rows are added successfully */
SELECT * FROM employees;

/* check the update result: id=2, dob-> 2004-03-10 */
SELECT * FROM employees;

/* check the delete result: delete id=3 */
SELECT * FROM employees;
