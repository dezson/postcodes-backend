import json
import requests

from http import HTTPStatus as http
from flask import current_app as app
from flask import make_response, jsonify
from flask import request

from .models import Store, db
from .utils import check_distance


@app.route('/health_check', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    app.logger.info("api.routes.health_check")

    msg = {"message": "ok"}
    header = {"Content-Type": "application/json"}
    return make_response(json.dumps(msg), http.OK, header)


@app.route('/add_store', methods=['POST'])
def add_stores():
    """This endpoints handles to create a new store resources"""
    fname = "api.add_store"
    app.logger.info(f"{fname}")

    if request.is_json and "name" in request.json and "postcode" in request.json:
        app.logger.info(f"{fname}: Payload {request.json}")
        new_store = Store(name=request.json["name"],
                          postcode=request.json["postcode"])

        db.session.add(new_store)
        db.session.commit()
        app.logger.info(f"{fname}: Store id : {new_store.id}")

        header = {"Location": f"/store/{new_store.id}"}
        return make_response("ok", http.CREATED, header)
    else:
        return make_response(json.dumps({"message": "Invalid payload"}), http.BAD_REQUEST)


@app.route("/store/<store_id>", methods=["GET"])
def get_store(store_id):
    """Delivers back a specific store's name, postcode, latitude, longitude
    Just for testing purposes, because the IDs will be hidden.
    """

    fname = "api.get_store"
    app.logger.info(f"{fname}")

    store = db.session.query(Store).filter(Store.id == store_id).first()
    app.logger.info(f"{fname}: Filtered store \n\t {store}")
    if store is None:
        return make_response("Item not found", http.NOT_FOUND)
    else:
        return make_response(jsonify(store.to_dict()), http.OK)


@app.route("/get_coords", methods=["GET"])
def list_get_coords():
    """Extends the loaded store records with latitude ang longitude fields.
    New fields are coming from postcodes api using HTTP GET request.
    """

    fname = "api.list_get_coords"
    app.logger.info(f"{fname}")
    stores = db.session.query(Store).all()
    if not stores:
        error = {"message": "There are no stores"}
        return make_response(json.dumps(error), http.NOT_FOUND)

    for store in stores:
        req = requests.get(f"http://api.postcodes.io/postcodes/{store.postcode}",
                           headers={"Accept": "application/json"})

        res = req.json()
        if res["status"] == 200:
            latitude = res["result"]["latitude"]
            longitude = res["result"]["longitude"]
            app.logger.info(f"{store.postcode}: {latitude} {longitude}")
            store.longitude = longitude
            store.latitude = latitude
        else:
            app.logger.info(f"{store.postcode} Not found!")

    db.session.commit()
    ret = []
    for r in stores:
        ret.append(r.to_verbose_dict())
    return make_response(jsonify(ret), http.OK)


@app.route("/stores_in_order",  methods=['GET'])
def list_stores_in_order():
    """Listing all stores in alphabetical order"""
    
    fname = "api.list_stores_in_order"
    app.logger.info(f"{fname}")

    stores = db.session.query(Store).all()
    app.logger.info(f"{fname}: Origin = {stores}")

    stores_in_order = sorted(stores, key=lambda x: str(x.name).upper(), reverse=False)
    app.logger.info(f"{fname}: Ordered = {stores_in_order}")

    if not stores_in_order:
        error = {"message": "There are no stores"}
        return make_response(json.dumps(error), http.NOT_FOUND)

    return make_response(jsonify([store.to_dict() for store in stores_in_order]), 200)



@app.route("/whats_in_radius/<postcode>/<radius>", methods=["GET"])
def get_stores_in_radius(postcode, radius):
    """Listing all loaded stores in a given radius compared to specific postcodes coordinates"""

    fname = "api.get_stores_in_radius"
    if not postcode or not radius:
        return make_response(json.dumps({"message": "Invalid parameters"}), http.BAD_REQUEST)

    req = requests.get(f"http://api.postcodes.io/postcodes/{postcode}",
                       headers={"Accept": "application/json"})

    res = req.json()
    if res["status"] != 200:
        return make_response("Given postcode not found", http.INTERNAL_SERVER_ERROR)

    x_coord = res["result"]["latitude"]
    y_coord = res["result"]["longitude"]
    app.logger.info(f"{fname} {postcode}: {x_coord} {y_coord}")

    stores = db.session.query(Store).all()

    res = []
    for store in stores:
        app.logger.info(f"{fname} Comparing : {store.latitude} {store.longitude} {x_coord} {y_coord}")
        if check_distance(store.latitude, store.longitude, x_coord, y_coord, float(radius)):
            app.logger.info(f"{fname} Added: {store.postcode}: {store.latitude} {store.longitude}")
            res.append(store.to_verbose_dict())

    app.logger.info(f"{fname} stores in radius: {res}")
    if not res:
        error = {"message": "Nothing in radius"}
        return make_response(json.dumps(error), http.NOT_FOUND)

    stores_in_order = sorted(res, key=lambda x: float(x["longitude"]), reverse=True)
    return make_response(jsonify(stores_in_order), http.OK)
