# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""
SELECT firstName, lastName
FROM employees
JOIN offices USING (officeCode)
WHERE city = 'Boston'
""", conn)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""
SELECT officeCode, city
FROM offices
WHERE officeCode NOT IN (SELECT officeCode FROM employees)
""", conn)

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""
SELECT firstName, lastName, city, state
FROM employees
LEFT JOIN offices USING (officeCode)
ORDER BY firstName, lastName
""", conn)

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""
SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY contactLastName
""", conn)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""
SELECT contactFirstName, contactLastName, amount, paymentDate
FROM customers
JOIN payments USING (customerNumber)
ORDER BY CAST(amount AS REAL) DESC
""", conn)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""
SELECT employeeNumber, firstName, lastName, COUNT(customerNumber) AS num_customers
FROM employees
LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employeeNumber
HAVING AVG(creditLimit) > 90000
ORDER BY num_customers DESC
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""
SELECT productName, COUNT(orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits
FROM products
JOIN orderdetails USING (productCode)
GROUP BY productCode
ORDER BY totalunits DESC
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""
SELECT productName, productCode, COUNT(DISTINCT customerNumber) AS numpurchasers
FROM products
JOIN orderdetails USING (productCode)
JOIN orders USING (orderNumber)
GROUP BY productCode
ORDER BY numpurchasers DESC
""", conn)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""
SELECT COUNT(customerNumber) AS n_customers, officeCode, offices.city
FROM customers
JOIN employees ON customers.salesRepEmployeeNumber = employees.employeeNumber
JOIN offices USING (officeCode)
GROUP BY officeCode
""", conn)

# STEP 10
# Replace None with your code 
df_under_20 = pd.read_sql("""
WITH few_buyers AS (
    SELECT productCode
    FROM orderdetails
    JOIN orders USING (orderNumber)
    GROUP BY productCode
    HAVING COUNT(DISTINCT customerNumber) < 20
)
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, f.city, f.officeCode
FROM employees e
JOIN offices f ON e.officeCode = f.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
WHERE od.productCode IN (SELECT productCode FROM few_buyers)
ORDER BY e.lastName, e.firstName DESC
""", conn)

conn.close