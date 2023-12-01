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

def load_to_neo(config, test: bool = False):
  path = u.get_path(DAY, test=test)

  with open(path, 'r') as f:
    data = [d.strip() for d in f.readlines()]

  cnt = 0
  for row in data:
    row_value = ''
    for i in row:
      if i.isnumeric():
        row_value += i
        break
    for i in row[::-1]:
      if i.isnumeric():
        row_value += i
        break
    cnt += int(row_value)
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

    WITH
    CASE 
        WHEN size(chain) = 1 THEN chain + chain 
        ELSE chain 
    END AS chain

    RETURN SUM(toInteger(toString(chain[0])+toString(chain[-1]))) AS result
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query)
  return results.json()['results'][0]['data'][0]['row'][0]


def part_2():
  pass

if __name__ == "__main__":
  config = u.neo4j_config_local(os.environ['NEO4J_PASSWORD_LOCAL'])

  load_to_neo(config, test=True)
  print(f"Day 1 Part 1 test: expected: {142}, actual: {part_1()}")
  # # assert part_2() == xxx
  clear_neo(config)

  load_to_neo(config, test=False)
  print(f"Day 1 Part 1 actual: {part_1()}") # 52974
  # # part_2()
  # clear_neo(config)