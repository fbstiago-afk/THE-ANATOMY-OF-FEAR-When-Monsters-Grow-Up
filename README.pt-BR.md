# The Anatomy of Fear — When Monsters Grow Up

<!-- portfolio-link:start -->
[![Ver o pôster no Power BI](https://img.shields.io/badge/Ver%20o%20p%C3%B4ster-Power%20BI-6C3BAA?style=for-the-badge)](https://app.powerbi.com/view?r=eyJrIjoiMGViN2ZkYmMtOGUwNy00NGFmLTg2YTItNjBiYmY3MTI0MWEyIiwidCI6IjMxYzJjZDk3LWE3MGItNDgwYy1iZTM1LTBhMGRiMzgwZTNlNCJ9)
[![Mais projetos](https://img.shields.io/badge/Mais%20projetos-bocardidata.com.br-24172F?style=for-the-badge)](https://bocardidata.com.br)

> 🔗 **Relatório publicado (Publish to web):** [https://app.powerbi.com/view?r=eyJrIjoiMGViN2…](https://app.powerbi.com/view?r=eyJrIjoiMGViN2ZkYmMtOGUwNy00NGFmLTg2YTItNjBiYmY3MTI0MWEyIiwidCI6IjMxYzJjZDk3LWE3MGItNDgwYy1iZTM1LTBhMGRiMzgwZTNlNCJ9)
> 📂 **Mais projetos de Power BI:** **[bocardidata.com.br](https://bocardidata.com.br)**
<!-- portfolio-link:end -->

Meu pôster para o **Halloween Data Visualization Contest 2026** (Microsoft Fabric / Power BI Community). Uma página A4 em pé, feita em Power BI, contando como os medos mudam entre a infância e a vida adulta — usando só as 105 respostas da pesquisa oficial.

> *We outgrew the monsters. Not the fear.*

## O que tem na pasta

- `TheAnatomyOfFear_Submission.pbix` → arquivo que vai para a submissão (o `TheAnatomyOfFear.pbix` é a mesma coisa).
- `TheAnatomyOfFear.pbip` + pastas `.Report` e `.SemanticModel` → projeto aberto (PBIR + TMDL), que é onde eu trabalho.
- `Assets/` → fundo (SVG original e JPG exportado), tema, specs do Deneb, HTML/CSS das animações, prévia em PNG.
- `Documentacao/` → medidas DAX, consulta da tabela Respondent, layout, checklist do concurso e meus scripts de apoio.
- `STATUS.md` → onde estou e o que falta.

Os arquivos do concurso (starter, CSV, regras, imagens de referência) estão intactos.

## A história

Li o pôster de cima para baixo em quatro partes:

1. **The monsters changed shape (I–II).** Um gráfico em forma de "coluna vertebral": infância de um lado, hoje do outro. Na infância lideram *Being trapped / small spaces* (14), *Heights* (13), *Snakes* e *The dark* (11). Hoje: *War* (19), *Uncertainty about the future* (14), *Death* (12), *Financial insecurity* (11). Embaixo, três destaques: War 5 → 19, The dark 11 → 2 e Financial insecurity 0 → 11 (ninguém citou quando criança).
2. **The fears that never left (III).** 45 de 105 pessoas (42,9%) repetiram exatamente o mesmo medo nas duas listas. Cada pessoa vira um fantasminha; os acesos são os que ainda carregam um medo antigo. O mais "fiel" é *Snakes*: 6 dos 11 que tinham esse medo quando crianças continuam com ele.
3. **Even data has monsters (IV).** O pior pesadelo de quem trabalha com dados: *It arrives a mess*, 23 de 105 (21,9%).
4. Fecho com *The monsters didn't disappear. They learned to use spreadsheets.*

Alguns cuidados que deixei escritos no próprio pôster: os números são de pessoas, não de seleções; dava para marcar vários medos; é uma amostra voluntária da comunidade, não da população; e as setas ▲▼ comparam totais, não mostram a "trajetória" de cada pessoa.

## Modelo

Aproveitei o modelo do starter inteiro (mesma fonte, mesmo parser de JSON, mesmas tabelas `FactFearSelection`, `DimFear`, `DimAgeGroup`, `DimGender`, `DimCountry`) e acrescentei:

- tabela **`Respondent`**, uma linha por resposta, com o `dataNightmare` original, rótulos curtos (`Nightmare`, `NightmareDetail`), `AgeGroup`, quantos medos se repetiram (`FearsKept`) e quais (`KeptFears`);
- relacionamento `Respondent[ResponseKey]` 1 → * `FactFearSelection[ResponseKey]`, direção única;
- as medidas na pasta **Anatomy of Fear** (detalhes em `Documentacao/DAX_Measures.md`). Nenhum número do pôster está digitado à mão — tudo sai das medidas. Nos rankings deixei de fora *None of these*, *Prefer not to answer* e *Something else*.

## Visuais

- **Deneb (Vega-Lite):** a coluna vertebral dos medos, os 105 fantasmas e o ranking dos pesadelos de dados.
- **HTML Content:** o fantasma com a vela no topo (decorativo) e o card do pesadelo de dados. O ícone do card é só ilustração: célula vazia = valor faltando, barras repetidas = duplicatas, barras desalinhadas = formatos diferentes.
- **Nativos:** títulos, textos e números principais ficam em caixas de texto e cartões, que se comportam melhor com leitor de tela.
- O fundo (moldura gótica, lua, morcegos, teia, skyline) é uma imagem só, sem informação.

### Tooltips

A regra permite páginas de tooltip para detalhe extra, desde que a história funcione sem elas — então tudo que é essencial está na página principal. Fiz quatro, todas ocultas:

| Tooltip | Onde aparece | O que mostra |
|---|---|---|
| Fear dossier | qualquer medo da coluna vertebral | categoria, pessoas e % na infância e hoje, quantas repetiram, gráfico por faixa etária |
| Persistence | 42.9%, "45 of 105" e *Most loyal monster* | os medos que mais ficaram e o % que manteve algum medo por faixa etária |
| Data nightmare | barras dos pesadelos | detalhe da resposta, n e %, % por faixa etária |
| Ghost case file | cada fantasma | a "ficha" da resposta: medos de infância e de hoje, os repetidos destacados, faixa etária e pesadelo de dados |

Cada tooltip tem uma animaçãozinha em CSS: olhos no escuro e uma aranha descendo; um fantasma espiando atrás da lápide *STILL HERE* e uma vela; uma planilha assombrada e um morcego; e o fantasma flutuando na ficha. São só enfeite e param quando o sistema pede menos movimento.

Não usei bookmarks: não acrescentavam nada à história e complicavam a navegação por teclado.

## Acessibilidade

- Contraste conferido sobre o fundo `#151020`: textos entre 8:1 e 15,8:1; barras acima de 4:1; a faixa menta acima de 3:1 sobre as barras.
- Nada depende só de cor: valores escritos, ▲▼, ranks #1–#3, fantasmas cheios × vazados com números.
- Alt text vem de medidas e descreve o achado, sempre com o total (ex.: "45 of 105 respondents, 42.9%…").
- Ordem de tabulação segue a leitura; o fantasma decorativo está fora dela.

## Para abrir

Abra o `.pbix` direto. Se for atualizar, a fonte é o blob oficial do concurso (acesso anônimo). Visuais do AppSource usados: **Deneb** e **HTML Content** — já vão dentro do PBIX.

Os scripts em `Documentacao/scripts` são os que uso para remontar o projeto e o fundo quando mexo no layout (`python Documentacao/scripts/build.py pbip Assets/Background/AnatomyOfFear_Background.jpg`).
