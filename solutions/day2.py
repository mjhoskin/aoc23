import os
import requests 
import json 
import string

import utils as u
# import solutions.utils as u


DAY = 2

def build_statement(row: str) -> str:
  statement = ""
  game_id = row[1]
  for idx, count in enumerate(row[2::2]): 
    colour = row[2*idx+3]
    statement += f"CREATE (v{idx}_{game_id}:pull {{{colour}: {count}, game:{game_id}}}) "
  for idx in range(len(row) - 1):
    statement += f"CREATE (v{idx}_{game_id})-[:NEXT]->(v{idx+1}_{game_id})"
  return statement

def load_to_neo(config, test: bool = False):
  path = u.get_path(DAY, test=test)

  with open(path, 'r') as f:
    games = [d for d in f.readlines()]


  statements = []
  for row in games:
    for char in string.punctuation:
      row = row.replace(char, '')
    row = row.split()
    statements.append({"statement": build_statement(row)})

  all_data = {"statements": statements}

  results = u.post(config, all_data)

def clear_neo(config):
  statement = """
    MATCH (n: pull)-[r:NEXT]-() 
    DELETE n, r
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query) 

def part_1(config:dict):
  statement = """
    MATCH (p:pull) 
    WITH p.game AS row 
    WITH SUM(DISTINCT(row)) AS total
    MATCH (p:pull) 
    WHERE p.red > 12 OR p.green > 13 OR p.blue > 14 
    WITH total, SUM(DISTINCT(p.game)) AS faulty_sum
    RETURN total - faulty_sum AS valid
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query)
  return results.json()['results'][0]['data'][0]['row'][0]

def part_2(config:dict):
  pass
  statements = [
    """
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
      WHERE c1.value+c2.value+c3.value+c4.value = 'nine'
      SET c3.value = 9
    """,
    """
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
      WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'eight'
      SET c3.value = 8
    """,
    """
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
      WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'seven'
      SET c3.value = 7
    """,
    """
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
      WHERE c1.value+c2.value+c3.value = 'six'
      SET c2.value = 6
    """,
    """
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
      WHERE c1.value+c2.value+c3.value+c4.value = 'five'
      SET c3.value = 5
    """,
    """    
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
      WHERE c1.value+c2.value+c3.value+c4.value = 'four'
      SET c3.value = 4
    """,
    """    
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
      WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'three'
      SET c3.value = 3
    """,
    """    
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
      WHERE c1.value+c2.value+c3.value = 'two'
      SET c2.value = 2
    """,
    """    
      MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
      WHERE c1.value+c2.value+c3.value = 'one'
      SET c2.value = 1
    """
  ]

  query = {"statements": [{"statement": statement} for statement in statements]}
  results = u.post(config, query)
  return results

if __name__ == "__main__":
  config = u.neo4j_config_local(os.environ['NEO4J_PASSWORD_LOCAL'])

  clear_neo(config)
  load_to_neo(config, test=1)
  print(f"Day 1 Part 1 test: expected: {8}, actual: {part_1(config)}")
  # print(f"Day 1 Part 2 test: expected: {8}, actual: {part_2(config)}") 
  clear_neo(config)

  load_to_neo(config)
  print(f"Day 1 Part 1 actual: {part_1(config)}") # 3099
  print(f"Day 1 Part 2 actual: {part_2(config)}") # 53340
  clear_neo(config)