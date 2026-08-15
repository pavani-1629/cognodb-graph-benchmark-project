ONE_HOP_CYPHER = """
MATCH (u:User {id: $id})
      -[:FRIENDS_WITH]->(friend)
RETURN friend.id
"""

TWO_HOP_CYPHER = """
MATCH (u:User {id: $id})
      -[:FRIENDS_WITH*2]->(friend)
RETURN DISTINCT friend.id
"""

THREE_HOP_CYPHER = """
MATCH (u:User {id: $id})
      -[:FRIENDS_WITH*3]->(friend)
RETURN DISTINCT friend.id
"""
POINT_LOOKUP_CYPHER = """
MATCH (u:User {id: $id})
RETURN u.id
"""

AGGREGATION_CYPHER = """
MATCH ()-[r:FRIENDS_WITH]->()
RETURN count(r) AS relationship_count
"""

CONCURRENT_READ_CYPHER = """
MATCH (u:User {id: $id})
RETURN u.id
"""

CONCURRENT_WRITE_CYPHER = """
MATCH (source:User {id: $source})
MATCH (target:User {id: $target})
CREATE (source)-[:FRIENDS_WITH]->(target)
"""