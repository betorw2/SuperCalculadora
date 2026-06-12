# -*- coding: utf-8 -*-
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable

dolar=5.80
# preços/parametros
CART_KG=9.00; CART_G=312
TINTA_USD=79; TINTA_ML=6
CORR_KG=7.60; E_G=345
PVC_RS_M2=19.21/(1.20*0.62)     # 25,82 R$/m²
FITA_RS_M=75/50                 # 1,50 R$/m
ELAST=0.30
COLA_KG=30; COLA_G_M=5          # ESTIMADO g/m
MONTAGEM=3.50                   # ESTIMADO R$/display
CAIXA_BLANK_M2=2.44*0.70        # caixa 60x60x10 RSC, onda E (ESTIMADO blank)
qtd=1000
# Nozomi maquina
hm=22*8*3; chn=((18000000-4500000)/7/12 + 20000 + (3000+2000)*1.7)/hm
area_print=1.24*1.90            # 4/0
def nozomi_lote(q):
    th=area_print*q/(40*1.40*60); return max(th,1)*chn
# corte/vinco Yangchen 500 fls/h
cv_h=(3000+2000)*1.7/hm
cv_u=(1/500)*cv_h
cv_acerto=(100/500)*cv_h        # 100 folhas de acerto (lote)

def varun():
    cartao=1.34*1.96*CART_G/1000*CART_KG
    tinta=area_print*TINTA_ML/1000*TINTA_USD*dolar
    pvc=2*(0.58*0.06)*PVC_RS_M2
    elast=2*ELAST
    fita=2*0.04*FITA_RS_M
    suporteE=2*(0.10*0.20)*1.03*E_G/1000*CORR_KG
    cola=2.20*COLA_G_M/1000*COLA_KG
    caixa=CAIXA_BLANK_M2*E_G/1000*CORR_KG
    comp=[("Papel cartão 312g (folha 1,34×1,96 c/ perda)",cartao),
          ("Tinta UV Nozomi (1,24×1,90, 4/0)",tinta),
          ("PVC cristal 0,30 (2× 58×6 cm)",pvc),
          ("Elástico (2×)",elast),
          ("Fita Tesa (2× 4 cm)",fita),
          ("Suporte papelão E (2× 10×20 cm)",suporteE),
          ("Cola hot melt Fênix (2,20 m lin. · ~5 g/m EST.)",cola),
          ("Caixa individual onda E 60×60×10 (EST.)",caixa),
          ("Montagem — mão de obra (EST.)",MONTAGEM),
          ("Corte/vinco (MO, 500 fls/h)",cv_u)]
    return sum(c[1] for c in comp), comp

vu,comp=varun()
def ci_of(q):
    return vu*q + 2000 + nozomi_lote(q) + cv_acerto
ci=ci_of(qtd); ci_u=ci/qtd
fin=0.02*7/30
div=max(0.05,1-(0.25+0.15+0.09+fin))
frete_tot=130.0; frete_u=frete_tot/qtd
preco_u=ci_u/div+frete_u
faixas=[500,1000,2000,5000]
print("var/un",round(vu,3)); 
for nome,v in comp: print("  ",nome,round(v,3))
print("Nozomi lote(1000)",round(nozomi_lote(1000),1),"acerto cv",round(cv_acerto,2))
print("ci_u",round(ci_u,2),"fin",round(fin*100,3),"div",round(div,4),"preco_u",round(preco_u,2),"total",round(preco_u*qtd,2))
for q in faixas:
    cu=ci_of(q)/q; print("  faixa",q,"preco/un",round(cu/div+frete_tot/q,2))

# ---------- PDF ----------
CORAL=colors.HexColor("#D85A30"); CORALD=colors.HexColor("#993C1D"); LIGHT=colors.HexColor("#FAECE7"); GRAY=colors.HexColor("#888780"); LINE=colors.HexColor("#E0DCD3")
def brl(v): return "R$ "+f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
ss=getSampleStyleSheet()
body=ParagraphStyle('body',parent=ss['Normal'],fontName='Helvetica',fontSize=9.5,leading=14)
small=ParagraphStyle('small',parent=ss['Normal'],fontName='Helvetica',fontSize=8,textColor=GRAY,leading=11)
sech=ParagraphStyle('sech',parent=ss['Normal'],fontName='Helvetica-Bold',fontSize=11,textColor=CORALD,spaceBefore=8,spaceAfter=6)
cellL=ParagraphStyle('cellL',parent=ss['Normal'],fontName='Helvetica',fontSize=8.5,leading=11)
def header(st,W):
    h=Table([[Paragraph("<b>MAVIMIX ADESIVOS DECORATIVOS LTDA</b><br/><font size=8 color='#888780'>Avenida Brasil, 12025 — Braz de Pina — Rio de Janeiro/RJ<br/>CNPJ 06.340.575/0001-30 · Fone (21) 3866-9555 · www.m2flex.com.br</font>",body),
        Image("m2_logo.png",width=38*mm,height=38*mm*86/227)]],colWidths=[W*0.68,W*0.32])
    h.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT')])); st+=[h,Spacer(1,4),HRFlowable(width="100%",thickness=2,color=CORAL),Spacer(1,8)]
def comum(st,W):
    st.append(Paragraph("Atendendo à sua solicitação, apresentamos nossa proposta para confecção do display abaixo descrito:",body)); st.append(Spacer(1,8))
    info=Table([[Paragraph("<b>À</b>  CLIENTE EXEMPLO LTDA",body),Paragraph("<b>Orçamento</b> 79xxx",body)],
      [Paragraph("A/C: Roberto",small),Paragraph("Pagamento: À VISTA (faturado 7 dias)",small)],
      [Paragraph("Entrega: São Paulo/SP",small),Paragraph("Data: 09/06/2026 · Validade: 15 dias",small)]],colWidths=[W*0.6,W*0.4])
    info.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),1)])); st+=[info,Spacer(1,8)]
    st.append(Paragraph("<b><font color='#993C1D'>DISPLAY LAMÁ / ELÍPTICO DOBRÁVEL</font></b>",body))
    st.append(Paragraph("Formato fechado 60 × 190 cm · aberto 124 × 190 cm. Papel cartão <b>312 g</b>, impressão digital <b>UV Nozomi 4/0</b>, corte-vinco e dobra. Acessórios: 2 elásticos, 2 suportes de papelão E, 2 tiras de PVC cristal 0,30 (58×6), 2 fitas Tesa. Embalado em caixa individual de papelão (60×60×10 cm). Entrega em São Paulo.",body)); st.append(Spacer(1,10))
def tbl_qtd(st,W,mode):
    st.append(Paragraph("Preço por quantidade (com entrega SP)",sech))
    if mode=="cliente":
        qt=[['Quantidade','Preço unitário','Preço total']]
        for q in faixas: pu=ci_of(q)/q/div+frete_tot/q; qt.append([f"{q:,}".replace(",","."),brl(pu),brl(pu*q)]); 
        cw=[W*0.34,W*0.33,W*0.33]
    else:
        qt=[['Quantidade','Preço unitário','Preço total','vs. 500 un']]; base=ci_of(500)/500/div+frete_tot/500
        for q in faixas:
            pu=ci_of(q)/q/div+frete_tot/q; eco='—' if q==500 else f"-{round((1-pu/base)*100)}%"; qt.append([f"{q:,}".replace(",","."),brl(pu),brl(pu*q),eco])
        cw=[W*0.25,W*0.25,W*0.3,W*0.2]
    t=Table(qt,colWidths=cw); s=[('BACKGROUND',(0,0),(-1,0),colors.HexColor("#F1EFE8")),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(1,0),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if mode!="cliente": s.append(('TEXTCOLOR',(3,1),(3,-1),colors.HexColor("#3B6D11")))
    t.setStyle(TableStyle(s)); st+=[t,Spacer(1,8)]
def build(mode,outfile):
    doc=SimpleDocTemplate(outfile,pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm); W=A4[0]-32*mm; st=[]
    header(st,W); comum(st,W)
    st.append(Paragraph("Proposta comercial — quantidade 1.000 unidades",sech))
    rows=[['Descrição','Preço unit.','Total'],[Paragraph("<b>DISPLAY LAMÁ ELÍPTICO</b> — cartão 312g, UV Nozomi, montado, caixa individual, entrega SP",cellL),brl(preco_u),brl(preco_u*qtd)]]
    it=Table(rows,colWidths=[W-32*mm-32*mm,32*mm,32*mm]); it.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(1,0),(-1,-1),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    st+=[it,Spacer(1,4),Paragraph("Imposto ISS incluso (nota de serviço). Entrega inclusa — São Paulo/SP.",small),Spacer(1,12)]
    tbl_qtd(st,W,mode)
    if mode=="interno":
        st.append(Paragraph("Memorial de cálculo — custo industrial (1.000 un) — USO INTERNO",sech))
        mem=[['Item de custo (por display, salvo lote)','Custo/un','Custo total']]
        for nome,v in comp: mem.append([nome,brl(v),brl(v*qtd)])
        mem.append(["Faca (ferramental, lote)","",brl(2000)])
        mem.append(["Hora-máquina Nozomi (mín. 1h, lote)","",brl(nozomi_lote(qtd))])
        mem.append(["Acerto corte/vinco (100 fls, lote)","",brl(cv_acerto)])
        mem.append(["CUSTO INDUSTRIAL TOTAL","",brl(ci)])
        mt=Table(mem,colWidths=[W*0.56,W*0.22,W*0.22]); mt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8.3),('ALIGN',(1,0),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,LINE),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor("#FAF7F2")]),('BACKGROUND',(0,-1),(-1,-1),LIGHT),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('TEXTCOLOR',(0,-1),(-1,-1),CORALD),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
        st+=[mt,Spacer(1,8),Paragraph("Formação de preço",sech),
          Paragraph(f"Custo industrial unitário: <b>{brl(ci_u)}</b><br/>Financeiro = 2% × 7/30 = <b>{fin*100:.2f}%</b><br/>Divisor = 1 − (lucro 25% + comissão 15% + imposto 9% + financeiro {fin*100:.2f}%) = <b>{div:.4f}</b><br/>Preço base = {brl(ci_u)} ÷ {div:.4f} = <b>{brl(ci_u/div)}/un</b><br/>Frete SP (R$ 130 ÷ 1.000) = <b>{brl(frete_u)}/un</b> → Preço final <b>{brl(preco_u)}/un</b>",body),
          Spacer(1,6),Paragraph("Itens marcados (EST.) são estimativas a confirmar: cola hot melt (~5 g/m linear), caixa individual onda E 60×60×10 e mão de obra de montagem.",small),Spacer(1,10)]
    st.append(Paragraph("Condições gerais",sech))
    st.append(Paragraph("1. Valores sujeitos a alteração mediante análise dos arquivos finais.  2. Reservamo-nos o direito de entregar 5% a mais ou a menos da quantidade, pelo mesmo valor unitário.  3. Tinta Nozomi cotada em dólar (US$ ref. R$ 5,80).  4. Prazo de produção a combinar após aprovação de arte e ferramental.",small))
    st.append(Spacer(1,10)); st.append(HRFlowable(width="100%",thickness=1,color=LINE)); st.append(Spacer(1,4))
    st.append(Paragraph("USO INTERNO — não enviar ao cliente (contém composição de custo)." if mode=="interno" else "Documento comercial — M2 Flex.",small))
    doc.build(st); print("gerado",outfile)
build("cliente","M2_Orcamento_Cliente_Lamar_1000un.pdf")
build("interno","M2_Folha_Calculo_Lamar_1000un.pdf")
