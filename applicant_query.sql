-- Desafío 3 — Reporte de fallas del sistema de publicidad (HackerAd)
-- Motor: MySQL 8.x
--
-- Objetivo: listar los clientes con MÁS DE 3 eventos con status = 'failure'
-- en sus campañas, mostrando el nombre completo del cliente y la cantidad de
-- fallas, ordenado por cantidad de fallas en forma descendente.
--
-- Relación entre tablas:
--   customers (1) --< campaigns (N) --< events (N)
--   events.status = 'failure' marca un evento fallido.

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    COUNT(*)                               AS failures
FROM customers AS c
JOIN campaigns AS cm ON cm.customer_id = c.id
JOIN events    AS e  ON e.campaign_id  = cm.id
WHERE e.status = 'failure'
GROUP BY c.id, c.first_name, c.last_name
HAVING COUNT(*) > 3
ORDER BY failures DESC;
