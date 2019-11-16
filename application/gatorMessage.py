from flask import json, jsonify

import time


class Message():
    def __init__(
            self, m_id, m_text, m_sender_id, m_receiver_id, m_item_id, m_sent_ts, u_fname, u_lname, u_email):

        self.m_id = m_id
        self.m_text = m_text
        self.m_sender_id = m_sender_id
        self.m_receiver_id = m_receiver_id
        self.m_item_id = m_item_id
        self.m_sent_ts = m_sent_ts
        self.u_fname = u_fname 
        self.u_lname = u_lname
        self.u_email = u_email
        

    def toDict(self):
        return {
        'm_id' : self.m_id,
        'm_text' : self.m_text,
        'm_sender_id' : self.m_sender_id,
        'm_receiver_id' : self.m_receiver_id,
        'm_item_id' : self.m_item_id,
        'm_sent_ts' : self.m_sent_ts,
        'u_fname' : self.u_fname, 
        'u_lname' : self.u_lname,
        'u_email' : self.u_email
        }


def makeMessage(messageTuple):
    return Message(*messageTuple)

# -*- coding: utf-8 -*-
