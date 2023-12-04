MATCH (c:cell WHERE c.value =~ '\d') -[]- (n:cell WHERE n.value =~ '\D' AND n.value <> '.') 
RETURN c, n


CALL {
    MATCH (c:cell WHERE c.value =~ '\d') <-[:RIGHT]- (l:cell WHERE l.value =~ '\D') 
    RETURN c AS start_nodes
    UNION 
    MATCH (d:cell WHERE d.value =~ '\d') WHERE NOT ((d)<-[:RIGHT]-())
    RETURN d AS start_nodes
}
WITH start_nodes AS d
OPTIONAL MATCH (d:cell) -[:RIGHT]-> (r:cell WHERE r.value =~ '\d')// -[:RIGHT]-> (rr:cell)// WHERE rr.value =~ '\d')
WITH d,r// rr
OPTIONAL MATCH (r:cell) -[:RIGHT]-> (rr:cell WHERE rr.value =~ '\d')
// RETURN d.value + r.value + rr.value 
// RETURN d.value, r.value, rr.value 
RETURN d,r,rr
