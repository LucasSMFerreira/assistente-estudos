# Experimentos de busca

PDF usado: bd-aula.pdf. Métricas medidas com `python -m avaliacao.avaliar 4`.

| Experimento | Tamanho | Sobreposição | Acerto@4 | MRR | Conclusão |
| --- | --- | --- | --- | --- | --- |
| baseline | 800 | 100 | 15 | 0.733 | 0.7 | PONTO DE PARTIDA
| trechos pequenos | 400 | 50 | 15 | 0.733 | 0.5 |
| trechos grandes | 1200 | 150 | 15 | 0.733 | 0.5 |
| sem sobreposição | 800 | 0 | 15 | 0.733 | 0.4 |

-- Trechos menores melhoraram o MRR, porque cada trecho fala de um só assunto. Sem sobreposição, a nota caiu, porque ideias foram cortadas no meio. Escolhi 400/50 como configuração final