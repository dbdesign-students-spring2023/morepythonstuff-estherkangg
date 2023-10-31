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

-- display the five zip codes with the most wi-fi hotspots and the count in each DESC
SELECT postcode AS "Zip Code", COUNT(*) AS "Number of Hotspots" 
FROM hotspots 
GROUP BY postcode 
ORDER BY COUNT(*) DESC 
LIMIT 5;

-- display a list of the name, address, and zip code
SELECT name, location, postcode
FROM hotspots
WHERE provider = 'ALTICEUSA' AND city = 'Bronx' AND type LIKE '%Free%'
ORDER BY postcode DESC;

-- display the names of each boroughs of NYC and the # of free wifi hotspots in each
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

-- display the # of wifi hotspots in Bay Ridge, Brooklyn along with the population
SELECT COUNT(h.id) as hotspot_count, p.population
FROM hotspots h
JOIN populations p ON h.city = 'Brooklyn' AND p.nta = 'Bay Ridge'
GROUP BY p.population;

-- display the # of free wifi hotspots in each of the 5 nyc boroughs, along with population of each borough
SELECT p.borough, COUNT(h.id) as hotspot_count, p.population
FROM populations p
LEFT JOIN hotspots h ON (p.borough = h.city OR (p.borough = 'Manhattan' AND h.city = 'New York')) AND h.type = 'Free'
GROUP BY p.borough
ORDER BY p.borough;

-- display the names of each of the neighborhoods in which there exist wifi hotspots, but for which we do not have population data
SELECT DISTINCT h.nta
FROM hotspots h
LEFT JOIN populations p ON h.nta = p.nta_code
WHERE p.population IS NULL;

-- write query of choice
SELECT name, location, postcode, provider
FROM hotspots
WHERE postcode = 10012
ORDER BY provider ASC;

/*This query selects the name, location, postcode, 
and provider of all Wi-Fi hotspots with a postcode 
of 10012, which is in the SoHo neighborhood 
of Manhattan. The results are ordered alphabetically 
by provider, so you can easily see which providers
offer Wi-Fi in this area.*\
