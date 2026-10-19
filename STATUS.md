# Status

Última atualização: 19/10/2026 · prazo de envio: 21/10/2026

## Feito
- Modelo do starter + tabela `Respondent` e medidas da pasta *Anatomy of Fear*.
- Página principal A4 em pé (1357 × 1920), uma só visível. As páginas *Read Me*, *Data Preview* e *Landscape* do starter não entraram no projeto.
- Três gráficos em Deneb, dois HTML Content, textos e cartões nativos, tema próprio e fundo gótico.
- Quatro tooltips ocultos (Fear dossier, Persistence, Data nightmare, Ghost case file), cada um com uma animação.
- Alt text, ordem de tabulação e contraste revisados.
- PBIX salvo: `TheAnatomyOfFear_Submission.pbix`.

## Conferências
- Números batem com o CSV: 105 respostas, 285 seleções de infância e 264 atuais, 45 pessoas com medo repetido (42,9%), Being trapped 14, War 19, It arrives a mess 23 (21,9%). Também recalculei a persistência por outro caminho (`IsRetained`) e deu 45.
- Nenhuma linha da fato sem resposta correspondente.
- Tooltips testados passando o mouse: War, Heights, *It doesn't add up*, o 42.9% e fantasmas (#55 e #46 conferidos linha a linha no CSV).
- Persistência por faixa etária: 18–24 3/4, 25–34 18/35, 35–44 15/40, 45–54 8/18, 55–64 1/8.
- Specs do Deneb funcionando tanto na versão 1 quanto na 2 do visual.

## Ajustes ao longo do caminho
- O Georgia usa números "antigos" e o 0 parecia um "o" nos destaques → troquei por Segoe UI.
- O card de pesadelo cortava a última linha → reduzi a tipografia.
- Tirei do ícone da planilha os "#N/A", "NULL" e números, para não parecer dado real.
- Um gráfico de tooltip por idade sumia com as barras → simplifiquei a spec.

## Falta
1. Última olhada em tela cheia e exportar em PDF para conferir a impressão A4.
2. Passar pelo pôster com o Narrador do Windows.
3. Enviar o PBIX na Contests Gallery até 21/10.
