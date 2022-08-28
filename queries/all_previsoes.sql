/* Retorna uma tabela com horário e temperatura por cidade, data de previsão e data de acesso. Possui as seguintes colunas:

CIDADE -> nome da cidade em questão
DT_ACESSO -> data de acesso da previsão
DT_PREVISAO -> data da previsão
HORARIO -> horario da previsão
TEMPERATURA -> temperatura prevista para o horario HORARIO da data DT_PREVISAO

*/

SELECT l.nome as CIDADE, a.dt_acesso as DT_ACESSO, a.dt_previsao as DT_PREVISAO,
p.horario as HORARIO, p.temperatura as TEMPERATURA
FROM acesso a 
JOIN previsao p 
ON a.id=p.id_acesso
JOIN [local] l 
ON a.id_local=l.id;