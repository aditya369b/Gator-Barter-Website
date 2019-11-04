from flask import json, jsonify


class User():
    def __init__(
            self, u_id, u_email, u_pass, u_is_admin, u_created_ts,
            u_updated_ts, u_fname, u_lname, u_status
            ):
        self.u_id = u_id
        self.u_email = u_email
        self.u_pass = u_pass
        self.u_is_admin = u_is_admin
        self.u_created_ts = u_created_ts
        self.u_updated_ts = u_updated_ts
        self.u_fname = u_fname
        self.u_lname = u_lname
        self.u_status = u_status


def makeUser(userTuple):
    return User(*userTuple)
