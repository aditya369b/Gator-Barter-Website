from flask import json, jsonify

import time

"""
User class to dynamically use data retrieved from the data base

toDict() method used for the session dictionary bacause Dictionary 
objects are hashable

Timestamps are used in ISO format

"""
class User():
    def __init__(
            self,
            u_id,
            u_email,
            u_pwd,
            u_is_admin,
            u_create_ts,  # = time.strftime('%Y-%m-%d %H:%M:%S'),
            u_update_ts,  # = time.strftime('%Y-%m-%d %H:%M:%S'),
            u_fname,
            u_lname,
            u_status=1):

        self.u_id = u_id
        self.u_email = u_email
        self.u_fname = u_fname
        self.u_lname = u_lname
        self.u_is_admin = u_is_admin
        self.u_pwd = u_pwd
        if u_create_ts is "NULL":
            self.u_create_ts = time.strftime('%Y-%m-%d %H:%M:%S')
            self.u_update_ts = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.u_create_ts = u_create_ts
            self.u_update_ts = u_update_ts
        self.u_status = u_status

    def isAdmin(self):
        return self.u_is_admin > 0

    def toDict(self):
        return {
            'u_id': self.u_id,
            'u_email': self.u_email,
            'u_fname': self.u_fname,
            'u_lname': self.u_lname,
            'u_is_admin': self.u_is_admin,
            'u_pwd': self.u_pwd,
            'u_create_ts': self.u_create_ts,
            'u_update_ts': self.u_update_ts
        }


def makeUser(userTuple):
    return User(*userTuple)

# -*- coding: utf-8 -*-
