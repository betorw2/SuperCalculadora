# Super Calculadora de Displays — M2 Flex

Ferramenta de **orçamento de displays de papelão** (PDV) por modelo real de produção. Calcula custo industrial, frete e preço de venda por quantidade, e gera proposta comercial, folha de cálculo e planilha de custos.

## O que ela faz

- **Calculadora web** (`calculadora_displays_m2_web.html`): aplicativo autônomo, roda em qualquer navegador (PC ou celular), sem instalação nem servidor. Tudo roda localmente — nada é enviado para fora.
- Calcula, por modelo, o custo de **cartão/papelão**, **impressão** (comparando Nozomi digital × offset × direta), **insumos** (PVC, elástico, fita, suporte, cola, caixa, montagem) e **mão de obra**.
- **Frete por rota** (origem/destino, km, R$/km, capacidade do caminhão) com link para o Google Maps.
- Aplica **margens** (lucro, comissão, imposto, financeiro pró-rata) e devolve custo unitário, frete unitário e preço de venda.

## Modelos cadastrados

Automático Médio, Evolution, Premium, Slim (3 e 4 prateleiras), Farma, Flash Display, Flash Farm e Display Lamá (elíptico).

## Estrutura do projeto

| Arquivo / pasta | Descrição |
|---|---|
| `calculadora_displays_m2_web.html` | Calculadora web (versão para compartilhar) |
| `motor_orcamento_pdv_m2.html` | Mesma calculadora (versão "motor" interna) |
| `M2_Biblioteca_Modelos_BOM.json` | Base de dados dos modelos (peças, ondas, medidas) |
| `gerar_proposta.py`, `gerar_proposta2.py`, `lamar.py`, `gerar_henrique.py` | Scripts que geram os PDFs e planilhas de orçamento |
| `auditoria_custos_calculadora.xlsx` | Planilha de auditoria dos parâmetros/custos |
| `Manuais de engenharia de producao/` | Manuais de fabricação dos modelos |
| `*.pdf`, `*.xlsx`, `*.xlsm`, `*.docx` | Propostas, folhas de cálculo e documentos de apoio |

## Como usar a calculadora

Abra o arquivo `calculadora_displays_m2_web.html` com dois cliques no navegador. Escolha o modelo, a quantidade e ajuste os parâmetros conforme o pedido.

## Como publicar online

Veja `COMO_PUBLICAR_a_calculadora.md` (Netlify Drop, GitHub Pages ou Vercel).

## Observação

O arquivo `BACKUP_M2_Calculadora_*.zip` (~128 MB) **não é versionado** (está no `.gitignore`) porque ultrapassa o limite de 100 MB do GitHub.
