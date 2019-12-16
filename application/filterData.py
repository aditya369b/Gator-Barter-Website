"""
Class for holding logic for sorting Item Posts


The posts are a list of dictionareis which makes for interesting sort logic

Created By Alex Kohanim with some help from stack overflow

Please contact if any questions arise

"""

from flask import abort


def filter_data(data, filter_type):
    if filter_type == "alpha_desc":
        data = sorted(data, key=lambda k: k['i_title'])
    elif filter_type == "alpha_asc":
        data = sorted(data, key=lambda k: k['i_title'], reverse=True) 
    elif filter_type == "price_asc":
        data = sorted(data, key=lambda k: k['i_price']) 
    elif filter_type == "price_desc":
        data = sorted(data, key=lambda k: k['i_price'], reverse=True)
    elif filter_type == "date_asc":
        data = sorted(data, key=lambda k: k['i_create_ts'])  
    elif filter_type == "date_desc":
        data = sorted(data, key=lambda k: k['i_create_ts'], reverse=True)
    else:
        abort(404)
    return data
