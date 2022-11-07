-- Part a
CREATE TABLE InsuranceCo (
	name VARCHAR(100) PRIMARY KEY,
	phone INT);

CREATE TABLE Person (
	ssn INT PRIMARY KEY,
	name VARCHAR(100));

CREATE TABLE Driver (
	driverID INT,
	ssn INT PRIMARY KEY REFERENCES Person(ssn));

CREATE TABLE NonProfessionalDriver (
	ssn INT PRIMARY KEY REFERENCES Driver(ssn));

CREATE TABLE ProfessionalDriver (
	ssn INT PRIMARY KEY REFERENCES Driver(ssn),
	medicalHistory VARCHAR(200));
	
CREATE TABLE Vehicle (
	licensePlate VARCHAR(50) PRIMARY KEY,
	year INT,
	name VARCHAR(100) REFERENCES InsuranceCo(name),
	ssn INT REFERENCES Person(ssn),
	maxLiability REAL);

CREATE TABLE Car (
	licensePlate VARCHAR(50) PRIMARY KEY REFERENCES Vehicle(licensePlate),
	make VARCHAR(50));

CREATE TABLE Truck (
	licensePlate VARCHAR(50) PRIMARY KEY REFERENCES Vehicle(licensePlate),
	ssn INT REFERENCES ProfessionalDriver(ssn),
capacity INT);

CREATE TABLE Drives (
	licensePlate VARCHAR(50) REFERENCES Car(licensePlate),
	ssn INT REFERENCES NonProfessionalDriver(ssn),
	PRIMARY KEY (licensePlate, ssn));

-- Part b. 
-- The table Vehicle represents the relationship ‘insures’ in the E/R diagram.
-- ‘Insures’ is a many-to-one relationship, so I use a foreign key in Vehicle to represent this relationship.

-- Part c.
-- ‘Drives’ is a many-to-many relationship while ‘operates’ is a many-to-one relationship.
-- Therefore, I could represent the ‘operates’ relationship with a foreign key in the Truck table.
-- While I need to create a ‘Drives’ table to represent the ‘drives’ relationship.