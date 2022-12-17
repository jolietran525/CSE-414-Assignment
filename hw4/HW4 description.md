**CSE 414 Homework 4: Database Design**

**Objectives:** To translate from entity-relationship diagrams to a relational database, and to understand functional dependencies and normal forms.

**Assignment tools:**

- Pen and paper or any drawing tools you prefer (e.g., PowerPoint, [draw.io](https://www.draw.io/)).
- SQLite, Azure SQL Server, or any other relational database.

**What to turn in:** See submission instructions at the bottom.

**Assignment Details**

**Part 1: Geography E/R Diagram (10 points)**

Design an E/R diagram for geography that contains the following kinds of objects or entities together with the listed attributes.

Model the relationships between the objects with edges. Note that edges between entities can be labeled with constraints. Make sure to choose the correct primary key(s) based on the information below.

**Entities**

- countries (with attributes): name, area, population, GDP ("gross domestic product")
  - a country's name uniquely identifies the country within all countries
- cities: name, population, longitude, latitude
  - a city is uniquely identified by its (longitude, latitude) (not by name, ex: there are 41 different cities and towns named Springfield in the US!)
- rivers: name, length
- seas: name, max depth
- rivers and seas are uniquely identified within all water entities by their name (e.g., "Ganges" would be a unique water entity)

**Relationships:**

- each city belongs to exactly one country
- each river crosses one or several countries
- each country can be crossed by zero or several rivers
- each river ends in either a river or a sea

You can draw your diagrams on paper and scan them, take *quality* pictures of your drawn diagram then use [https://imagetopdf.com](https://imagetopdf.com/) to convert your image to a pdf or use your favorite drawing tools such as Powerpoint, Keynote, or [draw.io](https://www.draw.io/). (FYI: Google Slides lacks a few shapes that you might need such as rounded arrows... You can use a crescent and a line, or simply type a constraint label such as "=1".)

Name your file **geography.pdf**.

**Part 2: E/R to Schema (20 points)**

Consider the following E/R diagram:

![](Aspose.Words.45b17e6d-fa0c-4d77-846d-846776ac3214.001.jpeg)

*License plate* can have letters and numbers; *driverID* and *Social Security* contain only numbers; *maxLiability* is a real number; *year*, *phone*, *capacity* are integers; everything else are strings.

1. (10 points) Translate the diagram above by writing the SQL CREATE TABLE statements to represent this E/R diagram. Include all key constraints; you should specify both primary and foreign keys. Make sure that your statements are syntactically correct (you might want to check them using SQLite, Azure SQL Server, or another relational database).
2. (5 points) Which relation in your relational schema represents the relationship "insures" in the E/R diagram? Why is that your representation?
2. (5 points) Compare the representation of the relationships "drives" and "operates" in your schema, and explain why they are different.

Write your answers in a SQL file named driving.sql. Write your answers to questions b and c as *SQL comments* in the same file.

**Part 3: Functional Dependency Theory (35 points)**

Consider the following two relational schemas and sets of functional dependencies:

1. (10 points) R(A,B,C,D,E) with functional dependencies D → B, CE → A.
1. (10 points) S(A,B,C,D,E) with functional dependencies A → E, BC → A, DE → B.

For each of the above schemas, decompose it into BCNF. Show all of your work and explain, at each step, which dependency violations you are correcting. Make sure you describe each step in your decomposition steps. (5 points each)

A set of attributes X is called closed (with respect to a given set of functional dependencies) if X⁺ = X. Consider a relation with schema R(A,B,C,D) and an unknown set of functional dependencies. For each closed attribute set below, give a *set of functional dependencies* that is consistent with it.

3. (5 points) All subsets of {A,B,C,D} are closed.
3. (5 points) The only closed subsets of {A,B,C,D} are {} and {A,B,C,D}.
3. (5 points) The only closed subsets of {A,B,C,D} are {}, {B,C}, and {A,B,C,D}. Write your answers in a text file named theory.txt.

**Part 4: Mr. Frumble Relationship Discovery & Normalization (35**

**points)**

[Mr. Frumble](http://everythingbusytown.wikia.com/wiki/Mr._Frumble) (a great character for small kids who always gets into trouble) designed a simple database to record projected monthly sales in his small store. He never took a database class, so he came up with the following schema:

Sales(name, discount, month, price)

He inserted his data into a database, then realized that there was something wrong with it: it was difficult to update. He hires you as a consultant to fix his data management problems. He gives you this file [mrFrumbleData.txt](https://courses.cs.washington.edu/courses/cse344/mrFrumbleData.txt) and says: "Fix it for me!". Help him by normalizing his

database. Unfortunately, you cannot sit down and talk to Mr. Frumble to find out what functional dependencies make sense in his business. Instead, you will reverse engineer the functional dependencies from his data instance.

1. Create a table in the database and load the data from the provided file into that table; use SQLite or any other relational DBMS of your choosing.

Turn in your create-table statement. The data import statements are optional (you don't need to include these).

2. Find all non-trivial functional dependencies in the database. This is a reverse engineering task, so expect to proceed in a trial and error fashion. Search first for the simple dependencies, say name → discount then try the more complex ones, like name, discount → month, as needed. To check each functional dependency you have to write a SQL query.

Your challenge is to write this SQL query for every candidate functional dependency that you check, such that:

1. the query's answer is always short (say: no more than ten lines - remember that 0 results can be instructive as well)
1. you can determine whether the FD holds or not by looking at the query's answer. Try to be clever in order not to check too many dependencies, but don't miss potential relevant dependencies. For example, if you have A → B and C → D, you do not need to derive AC → BD as well.

Please write a SQL query for each functional dependency you find along with a comment describing the functional dependency. Please also include a SQL query for at least one functional dependency that does not exist in the dataset along with a comment mentioning that the functional dependency does not exist. Remember, short queries are preferred.

3. Decompose the table into Boyce-Codd Normal Form (BCNF), and create SQL tables for the decomposed schema. Create keys and foreign keys where appropriate.

For this question turn in the SQL commands for creating the tables.

4. Here, turn in the SQL queries that load the new tables, and count the size of the tables after loading them (obtained by running SELECT COUNT(\*) FROM Table).

Write your answers in a SQL file named **frumble.sql**. Don't forget to use SQL comments for all non-SQL-code answers.

**Submission Instructions**

The files you will need to submit to Gradescope

- geography.pdf
- driving.sql
- theory.txt
- frumble.sql

*Points may be deducted for incorrect file names, or for .sql files that are not executable.* Submit your answers to Gradescope.
