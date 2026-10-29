--1 

SELECT COUNT(*) AS total_trechos FROM trechos;

--2

SELECT id, pagina, LENGTH(conteudo) AS tamanho
FROM trechos
ORDER BY tamanho DESC
LIMIT 1;

--3

SELECT d.nome, ROUND(AVG(LENGTH(t.conteudo))) AS tamanho_medio
FROM documentos d
JOIN trechos t ON t.documento_id = d.id
GROUP BY d.nome;

--4 
SELECT pagina, LEFT(conteudo, 100) AS inicio 
FROM trechos
wHERE conteudo ILIKE '%nosql%';

--5 
SELECT p AS pagina_sem_texto
FROM generate_series(1, (SELECT MAX(pagina) FROM trechos WHERE documento_id = 1)) AS p
WHERE p NOT IN (SELECT pagina FROM trechos WHERE documento_id = 1);

    

