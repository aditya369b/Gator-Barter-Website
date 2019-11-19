from flask import json, jsonify

"""
Product class to dynamically use data retrieved from the data base

toDict() method used for the session dictionary bacause Dictionary 
objects are hashable

"""

class Product():
    def __init__(
            self, i_id, i_title, i_desc, i_price, i_is_tradable,
            i_u_id, i_create_ts, i_update_ts, i_sold_ts, i_status,
            i_c_id, ii_url, ii_status, c_name, c_id, c_status
            ):
        self.i_id = i_id
        self.i_title = i_title
        self.i_desc = i_desc
        self.i_price = i_price
        self.i_is_tradable = i_is_tradable
        self.i_u_id = i_u_id
        self.i_create_ts = i_create_ts
        self.i_update_ts = i_update_ts
        self.i_sold_ts = i_sold_ts
        self.i_status = i_status
        self.i_c_id = i_c_id
        self.ii_url = ii_url
        self.ii_status = ii_status
        self.c_name = c_name
        self.c_id = c_id
        self.c_status = c_status

    def getStatus(self):
        return self.i_status

    def toDict(self):
        return {
        'i_id' : self.i_id,
        'i_title' : self.i_title,
        'i_desc' : self.i_desc,
        'i_price' : self.i_price,
        'i_is_tradable' : self.i_is_tradable,
        'i_u_id' : self.i_u_id,
        'i_create_ts' : self.i_create_ts,
        'i_update_ts' : self.i_update_ts,
        'i_sold_ts' : self.i_sold_ts,
        'i_status' : self.i_status,
        'i_c_id' : self.i_c_id,
        'ii_url' : self.ii_url,
        'ii_status' : self.ii_status,
        'c_name' : self.c_name,
        'c_id' : self.c_id,
        'c_status' : self.c_status
        }


def makeProduct(productTuple):
    return Product(*productTuple)
