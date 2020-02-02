###### docker build -t tails-backend:latest .
###### docker run -d -p 8080:8080  tails-backend


###### make bulk (Content of stores.json will be loaded into the db, python-requests dependency)
###### make test (Testing, pytest dependency)




* GET /health_check - Basic health check, returns with 200 (OK)
* GET /stores_in_order - A list of store names and postcodes in JSON (in alphabetical order)
* POST /add_store - Create a new store from a JSON body.
* GET /get_coords - Add all coordinates to the stores and return with that.
* GET /whats_in_radius/<postcode>/<radius> - return a list of stores in any given radius of any given postcode in the UK ordered from north to south 

* GET /store/<store_id> - Return a single store. Just for test purposes. (Ids are hidden form users) 
