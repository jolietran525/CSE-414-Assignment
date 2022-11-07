-- PART 1
CREATE TABLE frumbleData (
name VARCHAR(20),
discount VARCHAR(4),
month VARCHAR(3),
price INT);




-- PART 2
-- name -> discount
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.name = f2.name AND
f1.discount != f2.discount;

-- name, discount -> month
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.name = f2.name AND
f1.discount = f2.discount AND
f1.month != f2.month;

-- dicount -> price
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.discount = f2.discount AND
f1.price != f2.price;

-- month -> price
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.month = f2.month AND
f1.price != f2.price;

-- [FD holds] name -> price
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.name = f2.name AND
f1.price != f2.price;

-- [FD holds] month -> discount
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.month = f2.month AND
f1.discount != f2.discount;

-- name -> price AND month -> discount
-- IMPLIES name, month -> price, discount

-- [FD holds] name, discount -> month, price
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.name = f2.name AND
f1.discount = f2.discount AND
f1.month != f2.month AND
f1.price != f2.price;

-- name, price -> month, discount
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.name = f2.name AND
f1.price = f2.price AND
f1.month != f2.month AND
f1.discount != f2.discount;

-- [FD holds] month, price -> discount
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.month = f2.month AND
f1.price = f2.price AND
f1.discount != f2.discount;

-- [FD holds] month, price -> name, discount
SELECT *
FROM frumbleData f1, frumbleData f2
WHERE f1.month = f2.month AND
f1.price = f2.price AND
f1.name != f2.name AND
f1.discount != f2.discount;

-- FDs:
-- name -> price 
-- month -> discount
-- name, month -> price, discount
-- name, discount -> month, price
-- month, price -> discount
-- month, price -> name, discount




-- PART 3
-- R(name, discount, month, price)
-- {name}+ = {name, price}, which is neither {name} nor {name, discount, month, price}

-- So using BCNF Decomposition on R(name, discount, month, price), we get:
-- R1(name, price) and
-- R2(name, discount, month)
-- R1 is now fine and name is the key.
-- However, we still problem with R2

-- {month}+ = {month, discount}, which is neither {month} nor {name, discount, month}
-- So using BCNF Decomposition on R2(name, discount, month), we get:
-- R2a(month, discount) and
-- R2b(month, name)

-- Therefore, we have R1(name, price), R2a(month, discount), R2b(month, name)




-- PART 4
CREATE TABLE Name_Price (
name VARCHAR(20) PRIMARY KEY,
price INT);

CREATE TABLE Month_Discount (
month VARCHAR(3) PRIMARY KEY,
discount VARCHAR(4));

CREATE TABLE Name_Month (
name VARCHAR(20) REFERENCES Name_Price(name),
month VARCHAR(3) REFERENCES Month_Discount(month));

INSERT INTO Name_Price
SELECT DISTINCT name, price FROM frumbleData;

-- 36 rows
SELECT COUNT(*)
FROM Name_Price;

INSERT INTO Month_Discount 
SELECT DISTINCT month, discount FROM frumbleData;

-- 12 rows
SELECT COUNT(*)
FROM Month_Discount;


INSERT INTO Name_Month 
SELECT DISTINCT name, month FROM frumbleData;

-- 426 rows
SELECT COUNT(*)
FROM Name_Month;