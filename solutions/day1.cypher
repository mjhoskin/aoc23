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