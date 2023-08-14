
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=10609301&assignment_repo_type=AssignmentRepo)


Update the solution contents of this file according to [the instructions](instructions/instructions.md).

## Solutions

The following sections contain a report on the solutions to each of the required components of this exam.

### Data munging

The code in the Python program, [solution.py](solution.py), contains the solutions to the **data munging** part of this exam.

### Spreadsheet analysis

The spreadsheet file, [wifi.xslx](data/wifi.xslx), contains the solutions to the **spreadsheet analysis** part of this exam. In addition, the formulas used in that spreadsheet are indicated below:

1. Total number of free Wi-Fi hotspots in NYC

```
=COUNTIF(C3:C3321, "Free")
```

2. Number of free Wi-Fi hotspots in each of the 5 boroughs of NYC.

```
=COUNTIFS(R:R, AE7, C:C, "Free")
=COUNTIFS(R:R, AE8, C:C, "Free")
=COUNTIFS(R:R, AE9, C:C, "Free")
=COUNTIFS(R:R, AE10, C:C, "Free")
=COUNTIFS(R:R, AE11, C:C, "Free")
```

3. Number of free Wi-Fi hotspots provided by the LinkNYC - Citybridge in each of the zip codes of Manhattan.

```
=COUNTIFS(V:V, AE25, D:D, "LinkNYC - Citybridge", C:C, "Free")
```

4. The percent of all hotspots in Manhattan that are provided by LinkNYC - Citybridge.

```
=(COUNTIFS(R:R,"Manhattan",D:D,"LinkNYC - Citybridge")/COUNTIF(R:R,"Manhattan"))*100
```

### SQL queries

This section shows the SQL queries that you determined solved each of the given problems.

1. Write two SQL commands to create two tables named `hotspots` and `populations`.

```sql
create table hotspots (
id INTEGER PRIMARY KEY,
borough_id INTEGER,
type TEXT,
provider TEXT,
name TEXT,
location TEXT,
latitude FLOAT,
longitude FLOAT,
x FLOAT,
y FLOAT,
location_t TEXT,
remarks TEXT,
city TEXT,
ssid TEXT,
source_id TEXT,
activated DATETIME,
boroughcode INTEGER,
borough_name TEXT,
nta_code TEXT,
nta TEXT,
council_district INTEGER,
postcode INTEGER,
boro_cd INTEGER,
census_tract INTEGER,
bctcb2010 INTEGER,
bin INTEGER,
bbl INTEGER,
doitt_id INTEGER,
lat_lng TEXT
);
```

```sql
create table populations (
id INTEGER PRIMARY KEY AUTOINCREMENT,
borough TEXT,
year INTEGER,
fips_county_code INTEGER,
nta_code TEXT,
nta TEXT,
population INTEGER
);

-- needed to create a temp table 
create table temp (
borough TEXT,
year INTEGER,
fips_county_code INTEGER,
nta_code TEXT,
nta TEXT,
population INTEGER
);

-- copying to original populations table 
INSERT INTO populations
(borough, year, fips_county_code, nta_code, nta, population)
SELECT * FROM temp;

-- then drop the temp one
DROP TABLE temp;
```

2. Import the data in the `wifi.csv` and `neighborhood_populations.csv` CSV files into these two tables.

```sql
.import data/wifi.csv hotspots --skip 1
```

```sql
.import data/neighborhood_populations.csv populations --skip 1
```

3. Display the five zip codes with the most Wi-Fi hotspots and the number of Wi-Fi-hotspots in each in descending order of the number of Wi-Fi-hotspots.

```sql
SELECT postcode AS "Zip Code", COUNT(*) AS "Number of Hotspots" 
FROM hotspots 
GROUP BY postcode 
ORDER BY COUNT(*) DESC 
LIMIT 5;
```

4. Display a list of the name, location, and zip code for all of the free Wi-Fi locations provided by `ALTICEUSA` in Bronx, in descending order of zip code.

```sql
SELECT name, location, postcode
FROM hotspots
WHERE provider = 'ALTICEUSA' AND city = 'Bronx' AND type LIKE '%Free%'
ORDER BY postcode DESC;
```

5. Display the names of each of the boroughs of NYC, and the number of free Wi-Fi hotspots in each.

```sql
SELECT
    CASE
        WHEN borough_id = 1 THEN 'New York'
        WHEN borough_id = 2 THEN 'Bronx'
        WHEN borough_id = 3 THEN 'Brooklyn'
        WHEN borough_id = 4 THEN 'Queens'
        WHEN borough_id = 5 THEN 'Staten Island'
        ELSE 'Unknown'
    END AS borough,
    COUNT(*) AS num_free_wifi_hotspots
FROM hotspots
WHERE type = 'Free'
GROUP BY borough_id;
```

6. Display the number of wifi hotspots in Bay Ridge, Brooklyn along with the population of Bay Ridge, Brooklyn.

```sql
SELECT COUNT(h.id) as hotspot_count, p.population
FROM hotspots h
JOIN populations p ON h.city = 'Brooklyn' AND p.nta = 'Bay Ridge'
GROUP BY p.population;
```

7. Display the number of **Free** wifi hotspots in each of the 5 NYC boroughs, along with the population of each borough.

```sql
SELECT p.borough, COUNT(h.id) as hotspot_count, p.population
FROM populations p
LEFT JOIN hotspots h ON (p.borough = h.city OR (p.borough = 'Manhattan' AND h.city = 'New York')) AND h.type = 'Free'
GROUP BY p.borough
ORDER BY p.borough;
```

8. Display the names of each of the neighborhoods in which there exist Wi-Fi hotspots, but for which we do not have population data.

```sql
SELECT DISTINCT h.nta
FROM hotspots h
LEFT JOIN populations p ON h.nta = p.nta_code
WHERE p.population IS NULL;
```

9. Write an additional SQL query of your choice using Sqlite with this table; then describe the results

This query selects the name, location, postcode, 
and provider of all Wi-Fi hotspots with a postcode 
of 10012, which is where I currrently live. The results are ordered alphabetically by provider, so I can easily see which providers offer Wi-Fi in this area.

```sql
SELECT name, location, postcode, provider
FROM hotspots
WHERE postcode = 10012
ORDER BY provider ASC;
```

### Normalization and Entity-relationship diagramming

This section contains responses to the questions on normalization and entity-relationship diagramming.

1. Is the data in `wifi.csv` in fourth normal form?

```
No, 'wifi.csv' is not in 4NF.
```

2. Explain why or why not the `wifi.csv` data meets 4NF.

```
It does not meet 4NF because in this file, there are multi-valued dependencies between the attributes location, borough_name, nta_code, nta, and postcode, as they all describe information about the location of the Wi-Fi hotspot, thus violating 4NF. 
```

3. Is the data in `neighborhood_populations.csv` in fourth normal form?

```
No, the data in 'neighborhood_populations.csv' is not in 4NF. 
```

4. Explain why or why not the `neighborhood_populations.csv` data meets 4NF.

```
This dataset doesn't seem to be in fourth normal form because it contains a transitive dependency. The borough field is dependent on the nta_code field, and the population field is dependent on both year and nta_code. However, nta is also dependent on nta_code, so there is a transitive dependency nta_code -> nta -> borough, thus violating 4NF.
```

5. Use [draw.io](https://draw.io) to draw an Entity-Relationship Diagram showing a 4NF-compliant form of this data, including primary key field(s), relationship(s), and cardinality.

Please refer to my images directory for my ER Diagram. 

