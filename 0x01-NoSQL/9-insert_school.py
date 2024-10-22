#!/usr/bin/env python3
"""
a Python function that inserts a new document
in a collection based on `kwargs`.
"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a document in Python.
    """
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
