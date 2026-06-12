# Como publicar a Super Calculadora de Displays online

O arquivo **`calculadora_displays_m2_web.html`** é autônomo (um único arquivo, sem instalação, sem servidor). Funciona em qualquer navegador e em celular. Abra com dois cliques pra testar localmente. Para o time acessar por um link, escolha uma das opções abaixo.

## Opção 1 — Netlify Drop (mais rápido, grátis, ~2 min)
1. Acesse https://app.netlify.com/drop
2. Arraste o arquivo `calculadora_displays_m2_web.html` para a página.
3. O Netlify gera um link na hora (ex.: `https://nome-aleatorio.netlify.app`). Renomeie em Site settings se quiser algo como `calculadora-m2.netlify.app`.
4. Compartilhe o link. Para atualizar, arraste o arquivo novo por cima.

Dica: faça login (grátis) antes pra o site não expirar.

## Opção 2 — GitHub Pages (bom pra versionar)
1. Crie um repositório no GitHub (pode ser privado).
2. Suba o arquivo renomeado para `index.html`.
3. Settings → Pages → Branch `main` / pasta raiz → Save.
4. Em ~1 min o link fica `https://seuusuario.github.io/repo/`.

## Opção 3 — Vercel
1. https://vercel.com → New Project → suba o arquivo (renomeado `index.html`).
2. Deploy → link `https://projeto.vercel.app`.

## Opção 4 — Sem internet pública (interno)
- Coloque o arquivo numa pasta compartilhada (Google Drive / OneDrive / SharePoint) e gere um link "qualquer pessoa com o link pode ver".  
- Ou hospede na intranet da M2.

## Colocar no grupo do Teams
1. Crie o grupo/equipe (ex.: "M2 — Teste Calculadora") e adicione **compras** e **orçamento**.
2. Em um canal, aba **+ → Site/Website** e cole o link publicado (Netlify/GitHub) — fica embutido dentro do Teams.
3. Ou só fixe o link na descrição do canal e peça o feedback por lá.

## O que pedir pro time testar
- Rodar orçamentos reais que já fizeram "na mão" e comparar com a calculadora (achar divergências).
- Conferir, por modelo, se o **preço bate com a realidade** (especialmente compras, que conhece os custos de insumo).
- Validar os parâmetros que estão editáveis: dólar, % lucro/comissão/imposto/financeiro, custos de offset, capacidade dos caminhões.
- Apontar modelos faltando ou medidas de peça erradas.

## Pontos em aberto pra validar com o time (importante)
- **Premium**: a estrutura foi lida do manual, mas prateleiras e acessórios foram dimensionados por analogia (o manual agrupa essas peças numa chapa só, sem cota individual). Confirmar a cota real.
- **Flash / Flash Farm**: usam onda mais leve (B/E) e construção sem laterais/base separadas, por isso saem mais baratos que os modelos EB — confirmar se está correto.
- **Custos de offset** (chapa R$300, acerto R$600, milheiro R$1.200, arte R$500, perda 150 folhas/entrada): estão editáveis; confirmar.
- **Capacidade dos caminhões** (branco ~340, amarelo ~575 displays): ajustar conforme o flat-pack real.

## Observação
A calculadora roda 100% no navegador (nada é enviado pra fora). O botão "Buscar km da rota" abre o Google Maps. A geração de proposta em PDF continua no app M2 (Cowork) — a versão web é para **cotar rápido**; quando quiser o PDF, peça aqui.
