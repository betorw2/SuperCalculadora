# -*- coding: utf-8 -*-
# Gera proposta M2 em dois modos: 'cliente' (sem composição de custo, sem coluna -%) e 'interno' (folha de cálculo completa)
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable)
from reportlab.lib.enums import TA_RIGHT

CORAL=colors.HexColor("#D85A30"); CORALD=colors.HexColor("#993C1D")
LIGHT=colors.HexColor("#FAECE7"); GRAY=colors.HexColor("#888780"); LINE=colors.HexColor("#E0DCD3")
def brl(v):
    return "R$ "+f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

ss=getSampleStyleSheet()
body=ParagraphStyle('body',parent=ss['Normal'],fontName='Helvetica',fontSize=9.5,leading=14)
small=ParagraphStyle('small',parent=ss['Normal'],fontName='Helvetica',fontSize=8,textColor=GRAY,leading=11)
sech=ParagraphStyle('sech',parent=ss['Normal'],fontName='Helvetica-Bold',fontSize=11,textColor=CORALD,spaceBefore=8,spaceAfter=6)
cellL=ParagraphStyle('cellL',parent=ss['Normal'],fontName='Helvetica',fontSize=8.5,leading=11)

# ---- dados do exemplo (Médio 500un) ----
DADOS=dict(
 cliente="CLIENTE EXEMPLO LTDA", orc="79xxx", modelo="DISPLAY AUTOMÁTICO MÉDIO — REDBOX",
 desc=("Display de chão (FSDU) 30 × 30 × 144 cm, <b>4 prateleiras</b>.<br/>"
   "Estrutura em corrugado onda <b>EB/E</b> (Paraibuna), cartão <b>230g/190g</b> contracolado, "
   "impressão digital <b>UV Nozomi</b> (corpo 4/4, demais 4/0), corte-vinco e montagem automática. "
   "Caixa de transporte inclusa. Suporta ~30 kg/prateleira.<br/>"
   "<font size=8 color='#888780'>patente BR 112020016883-1</font>"),
 qtd=500, preco_retira=397.56, preco_frete=403.75,
 tot_retira=198778.54, tot_frete=201874.54,
 faixas=[(250,404.20),(500,397.56),(1000,394.24),(2000,392.58),(5000,391.58)],
 # memorial (só interno)
 ci_u=215.48, ci_tot=107737.97,
 memorial=[("Corrugado EB/E (Paraibuna)","Matéria-prima",40705.26),("Papel cartão 230g/190g","Matéria-prima",21018.46),
   ("Tinta UV Nozomi","Impressão",32511.89),("Hora-máquina Nozomi","Impressão",1009.04),("Cola hotmelt","Colagem",1998.32),
   ("Clips de prateleira","Acessórios",1650.00),("Mão de obra (acopl.+corte)","Produção",730.00),
   ("Caixa de transporte","Embalagem",6315.00),("Faca (ferramental)","Ferramental",1800.00)],
 divisor=0.542, frete_desc="SP→Rio (caminhão próprio, 2 viagens × 2 × 430 km × R$ 1,80) = R$ 3.096,00 ÷ 500")

def header(st,W):
    head=Table([[
      Paragraph("<b>MAVIMIX ADESIVOS DECORATIVOS LTDA</b><br/>"
        "<font size=8 color='#888780'>Avenida Brasil, 12025 — Braz de Pina — Rio de Janeiro/RJ<br/>"
        "CNPJ 06.340.575/0001-30 · IE 79247480 · IM 3542360<br/>"
        "Fone (21) 3866-9555 · www.m2flex.com.br · fin@m2flex.com.br</font>", body),
      Image("m2_logo.png",width=38*mm,height=38*mm*86/227)
    ]],colWidths=[W*0.68,W*0.32])
    head.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT')]))
    st+=[head, Spacer(1,4), HRFlowable(width="100%",thickness=2,color=CORAL), Spacer(1,8)]

def build(mode, outfile):
    d=DADOS
    doc=SimpleDocTemplate(outfile,pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm)
    W=A4[0]-32*mm; st=[]
    header(st,W)
    st.append(Paragraph("Atendendo à sua solicitação, apresentamos nossa proposta para confecção do display abaixo descrito:", body))
    st.append(Spacer(1,8))
    info=Table([
      [Paragraph(f"<b>À</b>  {d['cliente']}",body), Paragraph(f"<b>Orçamento</b> {d['orc']}",body)],
      [Paragraph("A/C: Roberto",small), Paragraph("Data: 09/06/2026 · Validade: 15 dias",small)],
      [Paragraph("CNPJ/CPF: (a preencher) · Tel.: (a preencher)",small), Paragraph("Pagamento: FATURADO 28 dias",small)],
    ],colWidths=[W*0.6,W*0.4])
    info.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),1)]))
    st+=[info, Spacer(1,8)]
    desc=Paragraph(f"<b><font color='#993C1D'>{d['modelo']}</font></b><br/><br/>"+d['desc'], body)
    prod=Table([[Image("display_real.png",width=33*mm,height=33*mm*2828/1029), desc]],colWidths=[40*mm,W-40*mm])
    prod.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(1,0),(1,0),10)]))
    st+=[prod, Spacer(1,10)]
    # opções A/B
    st.append(Paragraph(f"Proposta comercial — quantidade {d['qtd']} unidades", sech))
    rows=[['Opção','Descrição','Preço unit.','Total'],
      ['A', Paragraph("<b>CLIENTE RETIRA NA FÁBRICA</b> (sem frete)<br/><font size=7 color='#888780'>Retirada em São Paulo/SP</font>",cellL), brl(d['preco_retira']), brl(d['tot_retira'])],
      ['B', Paragraph("<b>ENTREGA INCLUSA</b> (com frete)<br/><font size=7 color='#888780'>SP → Rio de Janeiro</font>",cellL), brl(d['preco_frete']), brl(d['tot_frete'])]]
    it=Table(rows,colWidths=[14*mm,W-14*mm-32*mm-32*mm,32*mm,32*mm])
    it.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),
      ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(2,0),(3,-1),'RIGHT'),
      ('ALIGN',(0,0),(0,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
      ('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    st+=[it, Spacer(1,4), Paragraph("As opções A e B não se somam — o cliente escolhe uma delas. Imposto ISS incluso (nota de serviço).",small), Spacer(1,12)]
    # tabela por quantidade
    st.append(Paragraph("Preço por quantidade (opção retira)", sech))
    if mode=='cliente':
        qt=[['Quantidade','Preço unitário','Preço total']]
        for q,pu in d['faixas']: qt.append([f"{q:,}".replace(",","."), brl(pu), brl(pu*q)])
        qcw=[W*0.34,W*0.33,W*0.33]
    else:
        qt=[['Quantidade','Preço unitário','Preço total','vs. 250 un']]
        base=d['faixas'][0][1]
        for q,pu in d['faixas']:
            eco='—' if q==d['faixas'][0][0] else f"-{round((1-pu/base)*100)}%"
            qt.append([f"{q:,}".replace(",","."), brl(pu), brl(pu*q), eco])
        qcw=[W*0.25,W*0.25,W*0.3,W*0.2]
    qtb=Table(qt,colWidths=qcw)
    sty=[('BACKGROUND',(0,0),(-1,0),colors.HexColor("#F1EFE8")),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
      ('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(1,0),(-1,-1),'RIGHT'),('ALIGN',(0,0),(0,-1),'LEFT'),
      ('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if mode!='cliente': sty.append(('TEXTCOLOR',(3,1),(3,-1),colors.HexColor("#3B6D11")))
    qtb.setStyle(TableStyle(sty))
    st+=[qtb, Spacer(1,8)]

    if mode=='interno':
        st.append(Paragraph("Memorial de cálculo — custo industrial (500 un) — USO INTERNO", sech))
        mem=[['Item de custo','Etapa','Custo total','% do custo']]
        tot=sum(c[2] for c in d['memorial'])
        for nome,et,v in d['memorial']: mem.append([nome,et,brl(v),f"{v/tot*100:.1f}%"])
        mem.append(['CUSTO INDUSTRIAL TOTAL','',brl(tot),'100%'])
        mt=Table(mem,colWidths=[W*0.40,W*0.22,W*0.23,W*0.15])
        mt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
          ('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(2,0),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,LINE),
          ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor("#FAF7F2")]),('BACKGROUND',(0,-1),(-1,-1),LIGHT),
          ('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('TEXTCOLOR',(0,-1),(-1,-1),CORALD),('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5)]))
        st+=[mt, Spacer(1,8), Paragraph("Formação de preço", sech),
          Paragraph(f"Custo industrial unitário: <b>{brl(d['ci_u'])}</b><br/>"
            f"Divisor markup = 1 − (lucro 30% + comissão 5% + imposto 9% + financeiro 1,8%) = <b>{d['divisor']:.3f}</b><br/>"
            f"Preço retira = {brl(d['ci_u'])} ÷ {d['divisor']:.3f} = <b>{brl(d['preco_retira'])}/un</b><br/>"
            f"Frete {d['frete_desc']} = <b>R$ 6,19/un</b> (repasse) → com entrega <b>{brl(d['preco_frete'])}/un</b>", body), Spacer(1,12)]

    st.append(Paragraph("Condições gerais", sech))
    st.append(Paragraph("1. Valores sujeitos a alteração mediante análise dos arquivos finais.  2. Reservamo-nos o direito de entregar 5% a mais ou a menos da quantidade, pelo mesmo valor unitário.  3. Clientes interestaduais sem inscrição estadual: valor final pode variar pelo diferencial de alíquotas.  4. Matérias-primas sujeitas a disponibilidade após confirmação do pedido.  5. Tinta Nozomi cotada em dólar — reajuste conforme câmbio.  6. Prazo de produção a combinar após aprovação de arte e ferramental.",small))
    st.append(Spacer(1,10)); st.append(HRFlowable(width="100%",thickness=1,color=LINE)); st.append(Spacer(1,4))
    tag = "USO INTERNO — não enviar ao cliente (contém composição de custo)." if mode=='interno' else "Documento comercial — M2 Flex."
    st.append(Paragraph(tag,small))
    doc.build(st); print("gerado",outfile)

build('cliente',"M2_Orcamento_Cliente_EXEMPLO_Medio.pdf")
build('interno',"M2_Folha_Calculo_EXEMPLO_Medio.pdf")
