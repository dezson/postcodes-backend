# This utility loads the content of the stores.json one by one into the database
# Because that's the RESTful way to add multiple resources

import json

import requests


def main():
    with open('stores.json') as json_file:
        stores = json.load(json_file)
        try:
            requests.get("http://localhost:8080/health_check")
            for s in stores:
                requests.post(
                    "http://localhost:8080/add_store",
                    headers={'Content-type': 'application/json'},
                    data=json.dumps(s))
        except:
            print("Is your server running?")
            exit(1)


if __name__ == '__main__':
    main()
