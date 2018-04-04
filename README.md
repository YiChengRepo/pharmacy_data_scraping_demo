# pharmacy_data_scraping_demo
a quick feasibility data scraping on weather the data would fit into MongoDB GeoSpatial query.
This app generate GeoJSON format which are suitable for MongoDB GeoSpatial query.

For example, for a single pharmacy it should contain the following element:

{
    "address": "10519 King George Blvd Surrey, BC  V3T 2X1 CANADA",
    "fax": "(604) 585-3350",
    "location": {
        "coordinates": [
            -122.8456202,
            49.1938138
        ],
        "type": "Point"
    },
    "name": "BELL PHARMACY",
    "phone": "(604) 585-3355"
}

You can import the generate file into mongo db via mongoimport, for example:
mongoimport --db dbName --collection collectionName --file fileName.json 

Then you can perform Geo Spatial query, for example:

db.pharmacy.find({ location:    { $geoWithin:       { $centerSphere: [ [ -123.3527434, 48.4288383 ], 0.2 / 3963.2 ] } } });
{ "_id" : ObjectId("5ab6d3747c9c1550b23f9989"), "name" : "AARONSON'S PHARMACY (COOK ST.) LTD.", "address" : "1711 Cook St. Victoria, BC  V8T 3P2 CANADA", "phone" : "(250) 383-6511", "fax" : "(250) 383-1353", "location" : { "type" : "Point", "coordinates" : [ -123.3527434, 48.4288383 ] } }


This appl works in both sequence and paraller mode which is much faster depends on number of thread you specify.

N.B the code isn't clean at all and require many tidy up.
