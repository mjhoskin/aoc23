import os
import requests 
import json 
import string

import utils as u
# import solutions.utils as u


DAY = 3

def build_statement(rows: list) -> str:
  statement = ""
  for row_idx, row in enumerate(rows):
    for col_idx, value in enumerate(row):
      statement += f"CREATE (v{row_idx}_{col_idx}:cell {{value: '{value}', row: {row_idx}, col: {col_idx}}}) "

  for row_idx, row in enumerate(rows):
    for col_idx in range(len(row)-1): # RIGHT
      statement += f"CREATE (v{row_idx}_{col_idx})-[:RIGHT]->(v{row_idx}_{col_idx+1}) "
      if col_idx != len(row) - 1 and row_idx != len(rows) - 1:
        statement += f"CREATE (v{row_idx}_{col_idx})-[:DIAG]->(v{row_idx+1}_{col_idx+1}) "
        statement += f"CREATE (v{row_idx+1}_{col_idx})-[:DIAG]->(v{row_idx}_{col_idx+1}) "
    for col_idx in range(len(row)):
      if row_idx < len(rows) - 1: # DOWN 
        statement += f"CREATE (v{row_idx}_{col_idx})-[:DOWN]->(v{row_idx+1}_{col_idx}) "
  # for idx, count in enumerate(row[2::2]): 
  #   colour = row[2*idx+3]
  #   statement += f"CREATE (v{idx}_{game_id}:pull {{{colour}: {count}, game:{game_id}}}) "
  # for idx in range(len(row) - 1):
  #   statement += f"CREATE (v{idx}_{game_id})-[:NEXT]->(v{idx+1}_{game_id})"
  return statement

def load_to_neo(config, test: bool = False):
  path = u.get_path(DAY, test=test)

  with open(path, 'r') as f:
    board = [list(d.strip()) for d in f.readlines()]

  statements = []
  statements.append({"statement": build_statement(board)})

  all_data = {"statements": statements}

  results = u.post(config, all_data)

def clear_neo(config):
  statement = """
    MATCH (n: cell)-[r]-() 
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
  statement = """
    MATCH (p:pull) 
    WHERE NOT ((p)<-[:NEXT]-())
    MATCH (p) -[*]-> (tgt) 
    WITH p AS p,  p.game AS game, MAX(tgt.blue) AS b, MAX(tgt.green) AS g, MAX(tgt.red) AS r
    WITH [p.red, r] AS rr,[p.green, g] as gg, [p.blue, b] as bb,  game as game
    UNWIND rr AS r
    WITH game, max(r) as r, gg, bb
    UNWIND gg as g
    WITH game, max(g) as g, r, bb
    UNWIND bb as b 
    WITH game, max(b) as b, r, g
    WITH game, r * g * b AS power
    RETURN SUM(power)
  """

  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query)
  return results.json()['results'][0]['data'][0]['row'][0]

if __name__ == "__main__":
  config = u.neo4j_config_local(os.environ['NEO4J_PASSWORD_LOCAL'])

  clear_neo(config)
  load_to_neo(config, test=1)
  print(f"Day 1 Part 1 test: expected: {4361}, actual: {part_1(config)}")
  # print(f"Day 1 Part 2 test: expected: {2286}, actual: {part_2(config)}") 
  clear_neo(config)

  # load_to_neo(config)
  # print(f"Day 1 Part 1 actual: {part_1(config)}") # 3099
  # print(f"Day 1 Part 2 actual: {part_2(config)}") # 72970
  # clear_neo(config)