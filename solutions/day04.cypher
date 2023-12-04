MATCH (c:card) -[*] -(n WHERE n.value <> toString(n.value))
WITH c.card_id as card, n.value as card_value, count(*) as card_count 
WHERE card_count > 1
WITH card, collect([card_value, card_count]) AS counts, card_count
RETURN SUM(0.5 * 2^size(counts))