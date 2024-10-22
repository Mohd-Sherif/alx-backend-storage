#!/usr/bin/env python3
"""
a Python function that returns all students
sorted by average score.
"""


def top_students(mongo_collection):
    """
    Top students
    """
    return mongo_collection.aggregate(
            [
                {
                    '$project': {
                        'averageScore': {
                            '$avg': {
                                '$avg': '$topics.score',
                            },
                        },
                    },
                },
                {
                    '$sort': {'averageScore': -1},
                },
            ]
        )
