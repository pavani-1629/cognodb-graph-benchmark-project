ONE_HOP_AQL = """
FOR edge IN friendships
    FILTER edge._from == CONCAT("users/", @id)
    FOR friend IN users
        FILTER friend._id == edge._to
        RETURN friend._key
"""

TWO_HOP_AQL = """
FOR v, e, p IN 2..2 OUTBOUND
    CONCAT("users/", @id)
    friendships
    RETURN v._key
"""

THREE_HOP_AQL = """
FOR v, e, p IN 3..3 OUTBOUND
    CONCAT("users/", @id)
    friendships
    RETURN v._key
"""

POINT_LOOKUP_AQL = """
FOR u IN users
    FILTER u._key == @id
    RETURN u._key
"""



AGGREGATION_AQL = """
FOR edge IN friendships
    COLLECT WITH COUNT INTO relationship_count
    RETURN relationship_count
"""


CONCURRENT_READ_AQL = """
FOR u IN users
    FILTER u._key == @id
    RETURN u._key
"""

CONCURRENT_WRITE_AQL = """
INSERT {
    _from: CONCAT("users/", @source),
    _to: CONCAT("users/", @target)
}
IN friendships
"""