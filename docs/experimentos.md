# Experimentos de busca

**PDF usado:** `bd-aula.pdf` (aula de Bancos de Dados NoSQL).
**Conjunto de teste:** 15 perguntas escritas à mão, cada uma com a página onde está a resposta.
**Comando:** `python -m avaliacao.avaliar 4`

## Métricas

- **Acerto@4:** fração das perguntas em que a página certa apareceu entre os 4 primeiros trechos retornados.
- **MRR (Mean Reciprocal Rank):** média de 1/posição da página certa (1º lugar vale 1, 2º vale 1/2, 3º vale 1/3; não encontrada vale 0). Premia quando a resposta certa aparece mais cedo.

## Resultados

| Experimento | Tamanho | Sobreposição | Acerto@4 | MRR |
| --- | --- | --- | --- | --- |
| **baseline** | **800** | **100** | **0.733** | **0.70** |
| trechos pequenos | 400 | 50 | 0.733 | 0.50 |
| trechos grandes | 1200 | 150 | 0.733 | 0.50 |
| sem sobreposição | 800 | 0 | 0.733 | 0.40 |

## Conclusão

- **O Acerto@4 não mudou (11 de 15 perguntas):** em todas as configurações, a página certa entrou entre os 4 primeiros resultados em 11 das 15 perguntas. O que mudou foi a **posição** em que ela aparece, e é isso que o MRR mede.
- **O baseline (800/100) teve o melhor MRR (0.70)** e foi mantido como configuração final.
- **Trechos de 400 caracteres** ficaram curtos demais: cada pedaço perde contexto e compete com vários outros parecidos.
- **Trechos de 1.200 caracteres** misturam mais de um assunto no mesmo pedaço, o que dilui o significado do embedding.
- **Sem sobreposição, o MRR caiu para 0.40:** ideias cortadas no meio entre dois trechos ficam mais difíceis de encontrar.

## Limitações e próximos passos

- O conjunto é pequeno (15 perguntas e 1 PDF). As diferenças servem de indicação, não de prova estatística.
- Em cada configuração, 4 perguntas ficaram sem a página certa no top 4: o próximo passo é listar quais são e analisar essas falhas.
- Ideias a testar: prefixos `search_document:` / `search_query:` do `nomic-embed-text`, mais PDFs e mais perguntas.
