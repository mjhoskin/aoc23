// PART 1 
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

// PART 2 PROCESSING, RUN THEN RUN PART 1
 
MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
WHERE c1.value+c2.value+c3.value+c4.value = 'nine'
SET c3.value = 9

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'eight'
SET c3.value = 8

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'seven'
SET c3.value = 7

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
WHERE c1.value+c2.value+c3.value = 'six'
SET c2.value = 6

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
WHERE c1.value+c2.value+c3.value+c4.value = 'five'
SET c3.value = 5

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)
WHERE c1.value+c2.value+c3.value+c4.value = 'four'
SET c3.value = 4

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)-[:NEXT]->(c4)-[:NEXT]->(c5)
WHERE c1.value+c2.value+c3.value+c4.value+c5.value = 'three'
SET c3.value = 3

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
WHERE c1.value+c2.value+c3.value = 'two'
SET c2.value = 2

MATCH (c1:calibration)-[:NEXT]->(c2)-[:NEXT]->(c3)
WHERE c1.value+c2.value+c3.value = 'one'
SET c2.value = 1
