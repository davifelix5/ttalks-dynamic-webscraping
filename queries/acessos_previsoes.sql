/* Retorna uma tabela com informações de todas as previsões feitas por dia e por cidade. Possui as seguintes colunas:

CIDADE -> cidade em questão
DT_ACESSO -> data de acesso à previsão
DT_PREVISAO -> data da previsão

*/

SELECT l.nome as CIDADE, a.dt_acesso as DT_ACESSO, a.dt_previsao as DT_PREVISAO
FROM acesso a
JOIN [local] l 
ON a.id_local=l.id;