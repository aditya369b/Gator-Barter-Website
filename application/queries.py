#!/usr/bin env python3


class Query():
    def __init__(self):
        self.TEST_USER = "SELECT * FROM user WHERE user.u_is_admin=1 LIMIT 1;"

    def SEARCH_QUERY(self, search):
        starting = "" + search + "%"
        ending = "%" + search + ""
        starting2 = " " + search + "%"
        ending2 = "%" + search + " "
        middle = "%" + search + "%"
        exact = search
        return"""
        SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
        FROM item AS i
        JOIN item_image AS ii
        ON i.i_id = ii.ii_i_id
        JOIN category as c
        ON c.c_id = i.i_c_id
        WHERE i.i_status = 1
        AND i.i_sold_ts IS NULL
        AND (i.i_desc LIKE '""" + starting + """'
        OR i.i_desc LIKE '""" + ending + """'
        OR i.i_desc LIKE '""" + starting2 + """'
        OR i.i_desc LIKE '""" + ending2 + """'
        OR i.i_desc LIKE '""" + middle + """'
        OR i.i_desc LIKE '""" + exact + """');
        """

    def ALL_APPROVED_LISTINGS(self):
        return """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    WHERE i.i_status = 1
    AND i.i_sold_ts IS NULL;
    """

    def ALL_PENDING_LISTINGS(self):
        return self.ALL_APPROVED_LISTINGS().replace(
            "WHERE i.i_status = 1", "WHERE i.i_status = 0")

    def APPROVED_ITEM(self, product_id):
        return """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    WHERE i.i_id = """ + product_id + """
    AND i.i_status >= 0;"""

    def USER_FOR_PRODUCT(self, product_id):
        return """
    SELECT u.u_id, u.u_email, u.u_fname, u.u_lname, i.i_u_id FROM user AS u
    JOIN item as i
    ON i.i_u_id = u.u_id
    AND i.i_id = """ + product_id + """;
    """

    def APPROVED_ITEMS_FOR_CATEGORY(self, categoryName):
        return """
    SELECT i.*, ii.ii_url, ii.ii_status, c.c_name, c.c_id, c.c_status
    FROM item AS i
    JOIN item_image AS ii
    ON i.i_id = ii.ii_i_id
    JOIN category as c
    ON c.c_id = i.i_c_id
    HAVING c.c_name = '""" + categoryName + """'
    AND i.i_status = 1;"""

    def GET_USER_BY_EMAIL(self, email):
        return """
        SELECT *
        FROM user u
        WHERE u_email ='""" + email + """'
        AND u_status = 1"""

    def INSERT_USER(self, email, password, fname, lname, created_ts, updated_ts):
        print(type(email))
        return """
        INSERT INTO `user` (u_email, u_pass, u_fname, u_lname, u_created_ts, u_updated_ts)
        VALUES('""" + email + "', '" + password + "', '" + fname + "', '" + lname + "', '" + created_ts + "', '" + updated_ts + "');"

    def ALL_NON_ADMIN_APPROVED_USERS(self):
        return """SELECT * FROM user
        WHERE user.u_is_admin = 0
        AND user.u_status > 0"""


def query():
    return Query()
