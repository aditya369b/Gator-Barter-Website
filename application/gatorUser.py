from flask import json, jsonify
import time


class User():
    def __init__(
            self, 
            u_id, 
            u_email, 
            u_pwd,
            u_is_admin,
            u_create_ts,# = time.strftime('%Y-%m-%d %H:%M:%S'), 
            u_update_ts,# = time.strftime('%Y-%m-%d %H:%M:%S'),
            u_fname,
            u_lname,
            u_status = 1):
        
        self.u_id = u_id
        self.u_email = u_email
        self.u_fname = u_fname
        self.u_lname = u_lname
        self.u_is_admin = u_is_admin
        self.u_pwd = u_pwd
        self.u_create_ts = time.strftime('%Y-%m-%d %H:%M:%S')
        self.u_update_ts = time.strftime('%Y-%m-%d %H:%M:%S')
        self.u_status = u_status


def makeUser(userTuple):
    return User(*userTuple)
# -*- coding: utf-8 -*-

