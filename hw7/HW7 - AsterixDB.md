﻿**CSE 414 Homework 7: JSON, NoSQL, and AsterixDB**

**Objectives:** To write queries over the semi-structured data model. To manipulate semi-structured data in JSON and use a NoSQL database system (AsterixDB).

**Assigned date:** December 1st, 2022 **Due date:** December 9th, 2022 **What to turn in:**

A single file for each question, i.e., q1.sqlp, q2.sqlp, etc. It should contain commands executable by SQL++, and any text answers should be comments in the file (start comment lines with -- as in SQL).

**Resources**

- [data](https://drive.google.com/file/d/1rNSUFs1wM1ppdGnRDvTDEuyA9gUwVGwV/view?usp=sharing): which contains mondial.adm (the entire dataset), country, mountain, and sea (three subsets)
- [documentation for AsterixDB](https://asterixdb.apache.org/docs/0.9.4/index.html)
- [guide written by former TAs](https://gitlab.cs.washington.edu/cse414-20wi/source/hw7/-/blob/master/asterix_guide.md)

**Assignment Details**

In this homework, you will write SQL++ queries over the semi-structured data model implemented in [AsterixDB](http://asterixdb.apache.org/). Asterix is an Apache project on building a DBMS over data stored in JSON or ADM files.

**Mondial Dataset**

You will run queries over the [Mondial database](https://www.dbis.informatik.uni-goettingen.de/Mondial/), a geographical dataset aggregated from multiple sources. As is common in real-world aggregated data, the Mondial dataset is *messy*; the schema is occasionally inconsistent, and some facts may conflict. We have provided the dataset in ADM format, converted from the XML format available online, for use in AsterixDB.

**Setting up AsterixDB**

1. Download and install AsterixDB. Download the file [asterixdb-0.9.6](https://dlcdn.apache.org/asterixdb/asterixdb-0.9.6/asterix-server-0.9.6-binary-assembly.zip) and unzip it anywhere you'd like.
2. (extra step for some users:) You need to install the **Java 8 SE Development Kit** if you don’t already have it. Follow [this link](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html) to the download for your system. Many people will have this already if you’ve installed the tools for writing Java programs. On Windows, just installing the JDK should be enough. For Mac you may need to do some additional steps as described [here](https://medium.com/@devkosal/switching-java-jdk-versions-on-macos-80bc868e686a).
2. Start an instance of AsterixDB using the **start-sample-cluster.sh** (or **.bat** if you are on Windows) located in the **opt/local/bin** folder.
2. When your AsterixDB instance is running you can enter the query interface by visiting [127.0.0.1:19001](http://127.0.0.1:19001) in your favorite web browser. It may take a few minutes before you can access the page, while the instance starts up.
2. Download the geographical data from the link in the resources above. The data are JSON data files; you can inspect them using your favorite text editor.
2. Create a dataverse of Mondial data. Copy and paste the text below in the Query box of the web interface. Edit the <path to mondial.adm>. Then press Run:

DROP DATAVERSE geo IF EXISTS; ![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.001.png)CREATE DATAVERSE geo;

CREATE TYPE geo.worldType AS {auto\_id:uuid };

CREATE DATASET geo.world(worldType)  PRIMARY KEY auto\_id AUTOGENERATED; LOAD DATASET geo.world USING localfs

(("path"="127.0.0.1:///<path to mondial.adm>, e.g., localhost://C:/Users/XXX/Desktop/hw7/data/mondial.adm"),("format"="adm")); /\* Edit the absolute path above to point to your copy of mondial.adm. \*/ /\* Use '\' instead of '/' in a path for Windows. e.g.,

C:\414\hw\geo\mondial.adm. \*/

7. Alternatively, you can use the terminal to run queries rather than the web interface. After you have started Asterix, put your query in a file (say **q1.sqlp**), then execute the query by typing the following command in terminal:

curl -v --data-urlencode "statement=`cat q1.sqlp`" --data pretty=true ![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.002.png)http://localhost:19002/query/service

This will print the output on the screen. If there is too much output, you can save it to a file

curl -v --data-urlencode "statement=`cat q1.sqlp`" --data pretty=true ![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.003.png)http://localhost:19002/query/service  > output.txt

You can now view **output.txt** using your favorite text editor.

8. To reference the geodatabase, use the statement USE geo; before each of your queries to declare the geo namespace. Alternatively, prefix every dataset with geo. Try this query to see if things are running correctly:

SELECT y.`-car\_code` as code, y.name as name ![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.004.png)FROM geo.world x, x.mondial.country y

ORDER BY y.name;

9. For practice, run, examine, modify these queries. They contain useful templates for the questions on the homework: make sure you understand them.

-- return the set of countries![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.005.png)

SELECT x.mondial.country FROM geo.world x;

-- return each country, one by one (see the difference?) SELECT y as country FROM geo.world x, x.mondial.country y;

-- return just their codes, and their names, alphabetically

-- notice that -car\_code is not a legal field name, so we enclose in ` ... `

SELECT y.`-car\_code` as code, y.name as name

FROM geo.world x, x.mondial.country y order by y.name;

-- this query will NOT run...

SELECT z.name as province\_name, u.name as city\_name

FROM geo.world x, x.mondial.country y, y.province z, z.city u

WHERE y.name='Hungary';

-- ...because some provinces have a single city, others have a list of cities; fix it:

SELECT z.name as province\_name, u.name as city\_name FROM geo.world x, x.mondial.country y, y.province z, CASE WHEN is\_array(z.city) THEN z.city

ELSE [z.city] END u

WHERE y.name='Hungary';

-- same, but return the city names as a nested collection;

-- note correct treatment of missing cities

-- also note the convenient LET construct (see SQL++ documentation) SELECT z.name as province\_name, (select u.name from cities u) as cities FROM geo.world x, x.mondial.country y, y.province z

LET cities = CASE WHEN z.city is missing THEN []

WHEN is\_array(z.city) THEN z.city

ELSE [z.city] END

WHERE y.name='Hungary';

10. To shutdown Asterix, simply run **stop-sample-cluster.sh** in the terminal. The script is located in **opt/local/bin** (or **opt\local\bin\stop-sample-cluster.bat** on windows).

**Problems (100 points)**

**For all questions asking to report free response-type questions, please leave your responses in comments**

Use only the mondial.adm dataset for problems 1-9.

1. Retrieve the names of all cities located in Peru, sorted alphabetically. Name your output attribute **city**. [Result Size: 30 rows of **{"city":...}**]
1. For each country return its name, its population, and the number of religions sorted alphabetically by country. Report 0 religions for countries without religions. Name your output attributes **country**, **population**, **num\_religions**. [Result Size: 238 rows of **{"num\_religions":..., "country":..., "population":...}** (order of keys can differ)]
1. For each religion return the number of countries where it occurs; order them in decreasing number of countries. Name your output attributes **religion**, **num\_countries**. [Result size: 37 of **{"religion':..., "num\_countries":...}** (order of keys can differ)]
1. For each ethnic group, return the number of countries where it occurs, as well as the total population world-wide of that group. Hint: you need to multiply the ethnicity’s percentage with the country’s population. Use the functions **float(x)** and/or **int(x)** to convert a **string** to a **float** or to an **int**. Name your output attributes **ethnic\_group**, **num\_countries**, **total\_population**. You can leave your final **total\_population** as a **float** if you like. [Result Size: 262 of **{"ethnic\_group":..., "num\_countries":..., "total\_population":...}** (order of keys can differ)]
1. Compute the list of all mountains, their heights, and the countries where they are located. Here you will join the "mountain" collection with the "country" collection, on the country code. You should return a list consisting of the mountain name, its height, the country code, and country name, in descending order of the height. Name your output attributes **mountain**, **height**, **country\_code**, **country\_name**. [Result Size: 272 rows of **{"mountain":..., "height":..., "country\_code":..., "country\_name":...}** (order of keys can differ)]

Hint: Some mountains can be located in more than one country. You need to output them for each country they are located in.

6. Compute a list of countries with all their mountains. This is similar to the previous problem, but now you will group the mountains for each country; return both the mountain name and its height. Your query should return a list where each element

consists of the country code, country name, and a list of mountain names and heights; order the countries by the number of mountains they contain, in descending order. Name your output attributes **country\_code**, **country\_name**, **mountains**. The attribute **mountains** should be a list of objects, each with the attributes **mountain** and **height**. [Result Size: 238 rows of **{"country\_code":..., "country\_name":..., "mountains": [{"mountain":..., "height":...}, {"mountain":..., "height":...}, ...]}** (order of keys can differ)]

7. Find all countries bordering two or more seas. Here you need to join the "sea" collection with the "country" collection. For each country in your list, return its code, its name, and the list of bordering seas, in decreasing order of the number of seas. Name your output attributes **country\_code**, **country\_name**, **seas**. The attribute **seas** should be a list of objects, each with the attribute sea. [Result Size: 74 rows of **{"country\_code":..., "country\_name":..., "seas": [{"sea":...}, {"sea":...}, ...]}** (order of keys can differ)]
7. Return all landlocked countries. A country is landlocked if it borders no sea. For each country in your list, return its code, its name, in decreasing order of the country's area. Note: this should be an easy query to derive from the previous one. Name your output attributes **country\_code**, **country\_name**, **area**. [Result Size: 45 rows of **{"country\_code":..., "country\_name":..., "area":...}** (order of keys can differ)]
7. For this query you should also measure and report the runtime; it may be approximate (warning: it might run for a while). Find all distinct pairs of countries that share both a mountain and a sea. Your query should return a list of pairs of country names. Avoid including a country with itself, like in (France,France), and avoid listing both (France,Korea) and (Korea,France) (not a real answer). Name your output attributes **first\_country**, **second\_country**. [Result Size: 7 rows of **{"first\_country":..., "second\_country":...}]**

For problems 10-12 we will ask you to load in the extra datasets provided in the data folder.

10. Create a new dataverse called geoindex, then run the following commands:

USE geoindex;![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.006.png)

CREATE TYPE countryType AS OPEN {

`-car\_code`: string,

`-area`: string,

population: string

};

CREATE DATASET country(countryType)

PRIMARY KEY `-car\_code`;

CREATE INDEX countryID ON country(`-car\_code`) TYPE BTREE; LOAD DATASET country USING localfs

(("path"="127.0.0.1://<path to country.adm>, e.g., /hw7/data/country.adm"![](Aspose.Words.b02d6df5-f2c1-481d-882e-766e4099001c.003.png)),("format"="adm"));

This created the type **countryType**, the dataset **country**, and a **BTREE** index on the attribute **-car\_code**, which is also the primary key. Both types are OPEN, which means that they may have other fields besides the three required fields **-car\_code**, **-area**, and population.

Create two new types: **mountainType** and **seaType**, and two new datasets, **mountain**, and **sea**. Both should have two required fields: **-id** and **-country**. Their key should be auto generated, and of type **uuid** (see how we did it for the mondial dataset). Create an index of type **KEYWORD** (instead of **BTREE**) on the **-country** field (for both **mountain** and **sea**). Turn in the complete sequence of commands for creating the dataverse and all three types, datasets, and indices (for **country**, **mountain**, **sea**).

Recall from the lecture that Asterix only allows creating index at the top-level collection, hence we provide the country, sea, etc collections individually even though their data is already included in mondial.

11. Re-run the query from 9. (“pairs of countries that share both a mountain and a sea”) on the new dataverse geoindex. Turn in your altered query and report on the new runtime. [Result Size: 7 rows of **{"first\_country":..., "second\_country":...}]**
11. Modify the query from 11. to return, for each pair of countries, the list of common mountains, and the list of common seas. Name your output attributes **first\_country**, **second\_country**, **mountains**, **seas**. [Result Size: 7 rows of **{"mountains":[{"mountain":...}, ...], "seas":[{"sea":...}, ...], "first\_country":..., "second\_country":...}]**

**Submission Instructions**

Write your answers in a file for each question: **q1.sqlp, … , q12.sqlp** to Gradescope. Leave your runtime and other responses in comments.