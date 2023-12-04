import os
import requests 
import json 

import utils as u
# import solutions.utils as u


DAY = 1

def build_statement(row: str, row_idx: int) -> str:
  statement = ""
  for idx, char in enumerate(row): 
    if str.isalpha(char):
      char = f'"{char}"'
    statement += f"CREATE (v{idx}_{row_idx}:calibration {{value: {char}, row:{row_idx}}}) "
  for idx in range(len(row) - 1):
    statement += f"CREATE (v{idx}_{row_idx})-[:NEXT]->(v{idx+1}_{row_idx})"
  return statement

def load_to_neo(config, test: int = 0):
  path = u.get_path(DAY, test=test)

  with open(path, 'r') as f:
    data = [d.strip() for d in f.readlines()]

  # cnt = 0
  # for row in data:
  #   row_value = ''
  #   for i in row:
  #     if i.isnumeric():
  #       row_value += i
  #       break
  #   for i in row[::-1]:
  #     if i.isnumeric():
  #       row_value += i
  #       break
  #   cnt += int(row_value)
  statements = []
  for row_idx, row in enumerate(data):
    statements.append({"statement": build_statement(row, row_idx)})

  all_data = {"statements": statements}

  results = u.post(config, all_data)

def clear_neo(config):
  statement = """
    MATCH (n: calibration)-[r:NEXT]-() 
    DELETE n, r
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query) 

def part_1():
  statement = """
    MATCH (c:calibration) 
    WHERE NOT ((c)<-[:NEXT]-())
    OPTIONAL MATCH (c) -[*]-> (tgt)
    WHERE tgt.value <> toString(tgt.value)
    WITH c.value AS init, c.row AS row, COLLECT(tgt.value) AS chain

    WITH
    CASE 
        WHEN init <> toString(init) THEN init + chain 
        ELSE chain 
    END AS chain 

    RETURN SUM(toInteger(toString(chain[0])+toString(chain[-1]))) AS result
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query)
  return results.json()['results'][0]['data'][0]['row'][0]

def part_2(config:dict):
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
  print(f"Day 1 Part 1 test: expected: {142}, actual: {part_1()}")
  clear_neo(config)

  load_to_neo(config, test=2)
  part_2(config)
  print(f"Day 1 Part 2 test: expected: {360}, actual: {part_1()}") 
  clear_neo(config)

  load_to_neo(config)
  print(f"Day 1 Part 1 actual: {part_1()}") # 52974
  part_2(config)
  print(f"Day 1 Part 2 actual: {part_1()}") # 53340
  clear_neo(config)