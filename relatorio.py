# Importando as classes para criar o pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pathlib import Path
import json
import os


ROOT = Path(__file__).parent  # Definição de pasta atual do arquivo
ARQUIVO_RESIDUOS = ROOT / "banco_de_dados" / "residuos.json"  # Caminho do arquivo não reciclados
ARQUIVO_RECICLADOS = ROOT / "banco_de_dados" / "residuos_reciclados.json"  # Caminho do arquivo reciclados

LOGO = ROOT / "images" / "logo.jpeg"  # <-- coloque sua logo aqui
PDF_SAIDA = ROOT / "relatorio_reciclagem.pdf"  # caminho onde o pdf final vai ser salvo


def carregar_ou_vazio(caminho, padrao):
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return padrao
    return padrao


def gerar_pdf():
    residuos = carregar_ou_vazio(ARQUIVO_RESIDUOS, [])
    reciclados = carregar_ou_vazio(ARQUIVO_RECICLADOS, [])

    styles = getSampleStyleSheet()
    pdf = SimpleDocTemplate(str(PDF_SAIDA), pagesize=A4)
    conteudo = []

    # ---------------------- LOGO DA EMPRESA ----------------------
    if LOGO.exists():
        try:
            img = Image(str(LOGO))
            img.drawHeight = 60  # altura da logo
            img.drawWidth = 60   # largura da logo
            conteudo.append(img)
            conteudo.append(Spacer(1, 20))
        except Exception as e:
            print("Erro ao carregar a logo:", e)

    # ---------------------- TÍTULO ----------------------
    conteudo.append(Paragraph("<b>Relatório de Reciclagem</b>", styles["Title"]))
    conteudo.append(Spacer(1, 20))

    # ====================== RESÍDUOS PENDENTES ======================
    conteudo.append(Paragraph("<b>Resíduos disponíveis (não reciclados):</b>", styles["Heading2"]))
    conteudo.append(Spacer(1, 10))

    if residuos:
        tabela_residuos = [["Nome", "Tipo", "Peso (kg)", "Origem", "Fornecedor"]]

        for r in residuos:
            tabela_residuos.append([
                r.get("nome", "-"),
                r.get("tipo", "-"),
                r.get("peso", "-"),
                r.get("origem", "-"),
                r.get("cnpj_fornecedor", "-"),
            ])

        tabela = Table(tabela_residuos, repeatRows=1)
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        conteudo.append(tabela)
    else:
        conteudo.append(Paragraph("Nenhum resíduo pendente.", styles["BodyText"]))

    conteudo.append(Spacer(1, 20))

    # ====================== RESÍDUOS RECICLADOS ======================
    conteudo.append(Paragraph("<b>Resíduos reciclados:</b>", styles["Heading2"]))
    conteudo.append(Spacer(1, 10))

    if reciclados:
        tabela_reciclados = [["Nome", "Tipo", "Peso (kg)", "Origem", "Fornecedor", "Recicladora"]]

        for r in reciclados:
            tabela_reciclados.append([
                r.get("nome", "-"),
                r.get("tipo", "-"),
                r.get("peso", "-"),
                r.get("origem", "-"),
                r.get("cnpj_fornecedor", "-"),
                r.get("cnpj_recicladora", "-"),
            ])

        tabela = Table(tabela_reciclados, repeatRows=1)
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        conteudo.append(tabela)
    else:
        conteudo.append(Paragraph("Nenhum resíduo reciclado ainda.", styles["BodyText"]))

    # ---------------------- SALVAR PDF ----------------------
    pdf.build(conteudo)
    print(f"📄 Relatório gerado com sucesso: {PDF_SAIDA}")


if __name__ == "__main__":
    gerar_pdf()
