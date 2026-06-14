# -*- coding: utf-8 -*-
import sys, json, math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable

# ---------- MOTOR (espelho da calculadora) ----------
MODELOS=json.load(open("/sessions/beautiful-confident-johnson/mnt/claude orcamento/M2_Biblioteca_Modelos_BOM.json"))["modelos"]
GRAM={"E":345,"B":425,"EB":615}; CART_G={"E":190,"B":230,"EB":230}
C=dict(corr_kg=7.60,cart_kg=9.00,perda=1.03,tinta_usd_l=79,tinta_ml_m2=6,plast_m2=0.90,cola_g_m2=6,cola_kg=30,
 caixa=12.63,clip_par=0.55,mo=1.46,noz=dict(dep=(18000000-4500000)/7/12,manut=20000,op=3000,aj=2000,enc=0.70,m_min=50,boca=1.40,min_h=1))

def geo(mk):
    ac=pe=ap=cc=ent=0
    for p in MODELOS[mk]["pecas"]:
        nm,q,o,imp,L,A=p; a=L*A/10000*q*C["perda"]
        ac+=a; pe+=a*GRAM[o]/1000; ap+=a*(2 if imp=="4/4" else 1); cc+=a*CART_G[o]/1000*C["cart_kg"]; ent+=(2 if imp=="4/4" else 1)
    return dict(ac=ac,pe=pe,ap=ap,cc=cc,ent=ent,nprat=MODELOS[mk]["nprat"])

def custo(mk,qtd,o):
    g=geo(mk); acopla=o["impr"] in("nozomi","offset")
    c_corr=g["pe"]*C["corr_kg"]; c_cart=g["cc"] if acopla else 0
    c_tinta=g["ap"]*C["tinta_ml_m2"]/1000*C["tinta_usd_l"]*o["dolar"] if o["impr"] in("nozomi","direta") else 0
    c_plast=g["ap"]*C["plast_m2"] if (o["acab"]!="sem" and o["impr"]!="sem") else 0
    c_cola=g["ac"]*C["cola_g_m2"]/1000*C["cola_kg"]; c_clip=g["nprat"]*1.5*C["clip_par"]
    var_u=c_corr+c_cart+c_tinta+c_plast+c_cola+c_clip+C["mo"]+C["caixa"]
    hm=22*8*3; chn=(C["noz"]["dep"]+C["noz"]["manut"]+(C["noz"]["op"]+C["noz"]["aj"])*(1+C["noz"]["enc"]))/hm
    c_noz=0
    if o["impr"] in("nozomi","direta"):
        th=g["ap"]*qtd/(C["noz"]["m_min"]*C["noz"]["boca"]*60); c_noz=max(th,C["noz"]["min_h"])*chn
    c_faca=o["faca_valor"] if o["faca"]=="nova" else 0
    ci=var_u*qtd+c_noz+c_faca
    comp=[("Corrugado EB/E (Paraibuna)","Matéria-prima",c_corr*qtd),("Papel cartão 230g/190g","Matéria-prima",c_cart*qtd),
      ("Tinta UV Nozomi","Impressão",c_tinta*qtd),("Plastificação","Acabamento",c_plast*qtd),("Cola hotmelt","Colagem",c_cola*qtd),
      ("Clips de prateleira","Acessórios",c_clip*qtd),("Mão de obra (acopl.+corte)","Produção",C["mo"]*qtd),
      ("Caixa de transporte","Embalagem",C["caixa"]*qtd),("Hora-máquina Nozomi (lote)","Impressão",c_noz),("Faca (ferramental, lote)","Ferramental",c_faca)]
    comp=[c for c in comp if c[2]>0.005]
    return dict(ci=ci,ci_u=ci/qtd,comp=comp,g=g)

def frete(o,qtd):
    if o["frete"]=="direto": tot=o.get("frete_valor",0)
    elif o["frete"]=="rota":
        v=math.ceil(qtd/max(1,o.get("cap",1))); tot=v*(2*o.get("km",0)*o.get("rs_km",0))
    else: tot=0
    return tot, (tot/qtd if qtd else 0)

# ---------- CONFIG do pedido ----------
CFG=dict(mk="medio", qtd=500, dolar=5.80, impr="nozomi", acab="sem", faca="nova", faca_valor=1800,
  frete="retira", lucro=30, comissao=5, imposto=9, taxa_fin=2, prazo=28,
  cliente="CLIENTE EXEMPLO LTDA", orc="79xxx")
fin=CFG["taxa_fin"]/100*CFG["prazo"]/30
div=max(0.05,1-(CFG["lucro"]/100+CFG["comissao"]/100+CFG["imposto"]/100+fin))
r=custo(CFG["mk"],CFG["qtd"],CFG)
ft,fu=frete(CFG,CFG["qtd"])
preco_retira=r["ci_u"]/div
preco_frete=preco_retira+fu
faixas=[250,500,1000,2000,5000]
faixa_rows=[]
for q in faixas:
    rr=custo(CFG["mk"],q,CFG); _,fuq=frete(CFG,q); faixa_rows.append((q, rr["ci_u"]/div+fuq))

# ---------- PDF ----------
CORAL=colors.HexColor("#D85A30"); CORALD=colors.HexColor("#993C1D"); LIGHT=colors.HexColor("#FAECE7"); GRAY=colors.HexColor("#888780"); LINE=colors.HexColor("#E0DCD3")
def brl(v): return "R$ "+f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
ss=getSampleStyleSheet()
body=ParagraphStyle('body',parent=ss['Normal'],fontName='Helvetica',fontSize=9.5,leading=14)
small=ParagraphStyle('small',parent=ss['Normal'],fontName='Helvetica',fontSize=8,textColor=GRAY,leading=11)
sech=ParagraphStyle('sech',parent=ss['Normal'],fontName='Helvetica-Bold',fontSize=11,textColor=CORALD,spaceBefore=8,spaceAfter=6)
cellL=ParagraphStyle('cellL',parent=ss['Normal'],fontName='Helvetica',fontSize=8.5,leading=11)
NOME=MODELOS[CFG["mk"]]["nome"]; DIM=MODELOS[CFG["mk"]]["dim_cm"]

def header(st,W):
    h=Table([[Paragraph("<b>MAVIMIX ADESIVOS DECORATIVOS LTDA</b><br/><font size=8 color='#888780'>Avenida Brasil, 12025 — Braz de Pina — Rio de Janeiro/RJ<br/>CNPJ 06.340.575/0001-30 · IE 79247480 · IM 3542360<br/>Fone (21) 3866-9555 · www.m2flex.com.br · fin@m2flex.com.br</font>",body),
        Image("m2_logo.png",width=38*mm,height=38*mm*86/227)]],colWidths=[W*0.68,W*0.32])
    h.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT')]))
    st+=[h,Spacer(1,4),HRFlowable(width="100%",thickness=2,color=CORAL),Spacer(1,8)]

def comum(st,W):
    st.append(Paragraph("Atendendo à sua solicitação, apresentamos nossa proposta para confecção do display abaixo descrito:",body)); st.append(Spacer(1,8))
    info=Table([[Paragraph(f"<b>À</b>  {CFG['cliente']}",body),Paragraph(f"<b>Orçamento</b> {CFG['orc']}",body)],
      [Paragraph("A/C: Roberto",small),Paragraph("Data: 09/06/2026 · Validade: 15 dias",small)],
      [Paragraph("CNPJ/CPF: (a preencher) · Tel.: (a preencher)",small),Paragraph(f"Pagamento: FATURADO {CFG['prazo']} dias",small)]],colWidths=[W*0.6,W*0.4])
    info.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),2),('TOPPADDING',(0,0),(-1,-1),1)]))
    st+=[info,Spacer(1,8)]
    desc=Paragraph(f"<b><font color='#993C1D'>{NOME.upper()} — REDBOX</font></b><br/><br/>"
      f"Display de chão (FSDU) {DIM['larg']} × {DIM['prof']} × {DIM['alt']} cm, <b>{MODELOS[CFG['mk']]['nprat']} prateleiras</b>.<br/>"
      "Estrutura em corrugado onda <b>EB/E</b> (Paraibuna), cartão <b>230g/190g</b> contracolado, impressão digital <b>UV Nozomi</b> (corpo 4/4, demais 4/0), corte-vinco e montagem automática. Caixa de transporte inclusa. Suporta ~30 kg/prateleira.<br/>"
      "<font size=8 color='#888780'>patente BR 112020016883-1</font>",body)
    prod=Table([[Image("display_real.png",width=33*mm,height=33*mm*2828/1029),desc]],colWidths=[40*mm,W-40*mm])
    prod.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(1,0),(1,0),10)]))
    st+=[prod,Spacer(1,10)]

def build(mode,outfile):
    doc=SimpleDocTemplate(outfile,pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=14*mm,bottomMargin=14*mm)
    W=A4[0]-32*mm; st=[]; header(st,W); comum(st,W)
    st.append(Paragraph(f"Proposta comercial — quantidade {CFG['qtd']} unidades",sech))
    if CFG["frete"]=="retira":
        rows=[['Descrição','Preço unit.','Total'],
          [Paragraph("<b>CLIENTE RETIRA NA FÁBRICA</b> (sem frete)<br/><font size=7 color='#888780'>Retirada em São Paulo/SP</font>",cellL),brl(preco_retira),brl(preco_retira*CFG['qtd'])]]
        it=Table(rows,colWidths=[W-32*mm-32*mm,32*mm,32*mm])
    else:
        rows=[['Opção','Descrição','Preço unit.','Total'],
          ['A',Paragraph("<b>CLIENTE RETIRA NA FÁBRICA</b> (sem frete)",cellL),brl(preco_retira),brl(preco_retira*CFG['qtd'])],
          ['B',Paragraph("<b>ENTREGA INCLUSA</b> (com frete)",cellL),brl(preco_frete),brl(preco_frete*CFG['qtd'])]]
        it=Table(rows,colWidths=[14*mm,W-14*mm-32*mm-32*mm,32*mm,32*mm])
    sty=[('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
      ('FONTSIZE',(0,0),(-1,-1),9),('ALIGN',(-2,0),(-1,-1),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
      ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]
    it.setStyle(TableStyle(sty)); st+=[it,Spacer(1,4),Paragraph("Imposto ISS incluso (nota de serviço).",small),Spacer(1,12)]
    # tabela por quantidade
    st.append(Paragraph("Preço por quantidade",sech))
    if mode=="cliente":
        qt=[['Quantidade','Preço unitário','Preço total']]
        for q,pu in faixa_rows: qt.append([f"{q:,}".replace(",","."),brl(pu),brl(pu*q)])
        qcw=[W*0.34,W*0.33,W*0.33]
    else:
        qt=[['Quantidade','Preço unitário','Preço total','vs. 250 un']]; base=faixa_rows[0][1]
        for q,pu in faixa_rows:
            eco='—' if q==faixa_rows[0][0] else f"-{round((1-pu/base)*100)}%"; qt.append([f"{q:,}".replace(",","."),brl(pu),brl(pu*q),eco])
        qcw=[W*0.25,W*0.25,W*0.3,W*0.2]
    qtb=Table(qt,colWidths=qcw); s2=[('BACKGROUND',(0,0),(-1,0),colors.HexColor("#F1EFE8")),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
      ('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(1,0),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,LINE),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    if mode!="cliente": s2.append(('TEXTCOLOR',(3,1),(3,-1),colors.HexColor("#3B6D11")))
    qtb.setStyle(TableStyle(s2)); st+=[qtb,Spacer(1,8)]
    if mode=="interno":
        st.append(Paragraph(f"Memorial de cálculo — custo industrial ({CFG['qtd']} un) — USO INTERNO",sech))
        mem=[['Item de custo','Etapa','Custo total','% do custo']]; tot=sum(c[2] for c in r["comp"])
        for nome,et,v in r["comp"]: mem.append([nome,et,brl(v),f"{v/tot*100:.1f}%"])
        mem.append(['CUSTO INDUSTRIAL TOTAL','',brl(tot),'100%'])
        mt=Table(mem,colWidths=[W*0.40,W*0.22,W*0.23,W*0.15])
        mt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),CORAL),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
          ('FONTSIZE',(0,0),(-1,-1),8.5),('ALIGN',(2,0),(-1,-1),'RIGHT'),('GRID',(0,0),(-1,-1),0.5,LINE),
          ('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor("#FAF7F2")]),('BACKGROUND',(0,-1),(-1,-1),LIGHT),
          ('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('TEXTCOLOR',(0,-1),(-1,-1),CORALD),('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5)]))
        st+=[mt,Spacer(1,8),Paragraph("Formação de preço",sech),
          Paragraph(f"Custo industrial unitário: <b>{brl(r['ci_u'])}</b><br/>"
            f"Financeiro pró-rata = {CFG['taxa_fin']}% × {CFG['prazo']}/30 = <b>{fin*100:.2f}%</b><br/>"
            f"Divisor markup = 1 − (lucro {CFG['lucro']}% + comissão {CFG['comissao']}% + imposto {CFG['imposto']}% + financeiro {fin*100:.2f}%) = <b>{div:.4f}</b><br/>"
            f"Preço retira = {brl(r['ci_u'])} ÷ {div:.4f} = <b>{brl(preco_retira)}/un</b>" + ("" if CFG['frete']=='retira' else f"<br/>Com frete = <b>{brl(preco_frete)}/un</b>"),body),Spacer(1,12)]
    st.append(Paragraph("Condições gerais",sech))
    st.append(Paragraph("1. Valores sujeitos a alteração mediante análise dos arquivos finais.  2. Reservamo-nos o direito de entregar 5% a mais ou a menos da quantidade, pelo mesmo valor unitário.  3. Clientes interestaduais sem inscrição estadual: valor final pode variar pelo diferencial de alíquotas.  4. Matérias-primas sujeitas a disponibilidade após confirmação do pedido.  5. Tinta Nozomi cotada em dólar (US$ ref. R$ 5,80) — reajuste conforme câmbio.  6. Prazo de produção a combinar após aprovação de arte e ferramental.",small))
    st.append(Spacer(1,10)); st.append(HRFlowable(width="100%",thickness=1,color=LINE)); st.append(Spacer(1,4))
    st.append(Paragraph("USO INTERNO — não enviar ao cliente (contém composição de custo)." if mode=="interno" else "Documento comercial — M2 Flex.",small))
    doc.build(st); print("gerado",outfile)

build("cliente","M2_Orcamento_Cliente_Medio_500un.pdf")
build("interno","M2_Folha_Calculo_Medio_500un.pdf")
print(f"\nci_u={r['ci_u']:.2f} fin={fin*100:.3f}% div={div:.4f} preco_retira={preco_retira:.2f}")
