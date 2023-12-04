import os
import requests 
import json 
import string

import utils as u
# import solutions.utils as u


DAY = 4

def build_statement(card: list) -> str:
  # statement = ""
  # wins = card[0].split()
  # card_id = wins[1][:-1]
  # matches = card[1].split()
  # statement += f"CREATE (c: card {{card_id: {card_id}}}) "
  # for idx, count in enumerate(wins[2:]): 
  #   statement += f"CREATE (w{idx}_{card_id}:num {{value: {count}, card_id:{card_id}}}) "
  # statement += f"CREATE (c) -[:WINS]-> (w0_{card_id}) "

  # for idx, count in enumerate(matches):
  #   statement += f"CREATE (m{idx}_{card_id}:num {{value: {count}, card_id:{card_id}}}) "
  # statement += f"CREATE (c) -[:DRAWS]-> (m0_{card_id}) "
  # for idx in range(len(wins) - 1):
  #   statement += f"CREATE (w{idx}_{card_id})-[:NEXT]->(w{idx+1}_{card_id}) "
  # for idx in range(len(matches) - 1):
  #   statement += f"CREATE (m{idx}_{card_id})-[:NEXT]->(m{idx+1}_{card_id}) "
  # return statement
  
  card.remove('|')
  statement = ""
  statement += f"CREATE (c:card {{card_id: {card[1][:-1]}}}) "
  for idx, value in enumerate(card[2:]):
    statement += f"CREATE (n{idx}: num {{value: {value}}}) "
  statement += f"CREATE (c) -[:NEXT]-> (n0) "
  for idx in range(0, len(card)-1):
    statement += f"CREATE (n{idx})-[:NEXT]->(n{idx+1}) "

  return statement

  

def load_to_neo(config, test: int = 0):
  path = u.get_path(DAY, test=test)

  with open(path, 'r') as f:
    cards = [d.strip().split() for d in f.readlines()]


  statements = []
  for card in cards:
    # for char in string.punctuation:
    #   row = row.replace(char, '')
    statements.append({"statement": build_statement(card)})

  all_data = {"statements": statements}

  results = u.post(config, all_data)

def clear_neo(config):
  statement = """
    MATCH (c:card)-[r*]-(n) 
    UNWIND r AS rr 
    DELETE c,rr,n
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query) 

def part_1(config:dict):
  statement = """
    MATCH (c:card) -[*] -(n WHERE n.value <> toString(n.value))
    WITH c.card_id as card, n.value as card_value, count(*) as card_count 
    WHERE card_count > 1
    WITH card, collect([card_value, card_count]) AS counts, card_count
    RETURN SUM(0.5 * 2^size(counts))
  """
  query = {"statements": [{"statement": statement}]}
  results = u.post(config, query)
  return results.json()['results'][0]['data'][0]['row'][0]

# def part_2(config:dict):
#   statement = """
#     MATCH (p:pull) 
#     WHERE NOT ((p)<-[:NEXT]-())
#     MATCH (p) -[*]-> (tgt) 
#     WITH p AS p,  p.game AS game, MAX(tgt.blue) AS b, MAX(tgt.green) AS g, MAX(tgt.red) AS r
#     WITH [p.red, r] AS rr,[p.green, g] as gg, [p.blue, b] as bb,  game as game
#     UNWIND rr AS r
#     WITH game, max(r) as r, gg, bb
#     UNWIND gg as g
#     WITH game, max(g) as g, r, bb
#     UNWIND bb as b 
#     WITH game, max(b) as b, r, g
#     WITH game, r * g * b AS power
#     RETURN SUM(power)
#   """

#   query = {"statements": [{"statement": statement}]}
#   results = u.post(config, query)
#   return results.json()['results'][0]['data'][0]['row'][0]

if __name__ == "__main__":
  config = u.neo4j_config_local(os.environ['NEO4J_PASSWORD_LOCAL'])

  clear_neo(config)
  load_to_neo(config, test=1)
  print(f"Day 1 Part 1 test: expected: {13}, actual: {part_1(config)}")
  # print(f"Day 1 Part 2 test: expected: {2286}, actual: {part_2(config)}") 
  clear_neo(config)

  load_to_neo(config)
  print(f"Day 1 Part 1 actual: {part_1(config)}") # 22488 
  # print(f"Day 1 Part 2 actual: {part_2(config)}") # 72970
  clear_neo(config)