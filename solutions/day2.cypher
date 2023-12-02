// DAY 1 

MATCH (p:pull) 
WITH p.game AS row 
WITH SUM(DISTINCT(row)) AS total
MATCH (p:pull) 
WHERE p.red > 12 OR p.green > 13 OR p.blue > 14 
WITH total, SUM(DISTINCT(p.game)) AS faulty_sum
RETURN total - faulty_sum AS valid

// DAY 2 

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