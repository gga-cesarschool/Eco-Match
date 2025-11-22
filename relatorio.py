#Importando as classes para criar o pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pathlib import Path
import json
import os


ROOT = Path(__file__).parent  #Definião de pasta atual do arquivo
ARQUIVO_RESIDUOS = ROOT / "banco_de_dados" / "residuos.json" #Caminho do arquivo não reciclados
ARQUIVO_RECICLADOS = ROOT / "banco_de_dados" / "residuos_reciclados.json" #Caminho do arquivo reciclados
PDF_SAIDA = ROOT / "relatorio_reciclagem.pdf" #caminho onde o pdf final vai ser salvo


def carregar_ou_vazio(caminho, padrao): #Define função genérica para carregar JSON ou retornar valor padrão
    if os.path.exists(caminho): #verificação de existencia do arquivo
        try: #tentativa de carregamento e abertura do json
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return padrao #Caso de erro, retorna padrão
    return padrao # se não existir arquivo, retorna padrão


def gerar_pdf(): # gera o pdf por meio dessa função
    residuos = carregar_ou_vazio(ARQUIVO_RESIDUOS, []) #carrega a lista dos resíduos pendentes ou retorna a lista sem nada
    reciclados = carregar_ou_vazio(ARQUIVO_RECICLADOS, []) # <-- mesma coisa que o de cima porém dos reciclados

    styles = getSampleStyleSheet() #estilos de textos pré-definidos. O que foi feito no design
    pdf = SimpleDocTemplate(str(PDF_SAIDA), pagesize=A4)
    conteudo = [] # o que irá pra o pdf fica nessa lista

    # Título
    conteudo.append(Paragraph("<b>Relatório de Reciclagem</b>", styles["Title"])) #parte do design do pdf
    conteudo.append(Spacer(1, 20)) #add espaço de 20 pixels

    # Resíduos pendentes 
    conteudo.append(Paragraph("<b>Resíduos disponíveis (não reciclados):</b>", styles["Heading2"])) #add título
    conteudo.append(Spacer(1, 10)) #add espaço de separação

    if residuos:
        tabela_residuos = [["Nome", "Tipo", "Peso (kg)", "Origem", "Fornecedor"]] #add linha de cabeçalho da tabela

        for r in residuos: # a cada resíduo criado, vai  uma linha na tabela usando "-" se faltar campo
            tabela_residuos.append([
                r.get("nome", "-"),
                r.get("tipo", "-"),
                r.get("peso", "-"),
                r.get("origem", "-"),
                r.get("cnpj_fornecedor", "-"),
            ])

        tabela = Table(tabela_residuos, repeatRows=1) # criação da tabela ; repeatRows é pra q o cabeçalho seja repetido em novas páginas
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])) #design do cabeçalho

        conteudo.append(tabela) #insere a tabela no pdf
    else:
        conteudo.append(Paragraph("Nenhum resíduo pendente.", styles["BodyText"]))

    conteudo.append(Spacer(1, 20)) #espacinho para a próxima seção

    # Resíduos reciclados
    conteudo.append(Paragraph("<b>Resíduos reciclados:</b>", styles["Heading2"])) #título dessa parte
    conteudo.append(Spacer(1, 10)) #add espaço

    if reciclados:
        tabela_reciclados = [["Nome", "Tipo", "Peso (kg)", "Origem", "Fornecedor", "Recicladora"]] #cabeçalho da tabela

        for r in reciclados: #preenchimento da tabela com os dados
            tabela_reciclados.append([
                r.get("nome", "-"),
                r.get("tipo", "-"),
                r.get("peso", "-"),
                r.get("origem", "-"),
                r.get("cnpj_fornecedor", "-"),
                r.get("cnpj_recicladora", "-"),
            ])

        tabela = Table(tabela_reciclados, repeatRows=1) #criação da tabela com cabeçalhos repetidos
        tabela.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])) #design da tabela

        conteudo.append(tabela) #add tabela ao pdf
    else:
        conteudo.append(Paragraph("Nenhum resíduo reciclado ainda.", styles["BodyText"]))

    # Salvar PDF
    pdf.build(conteudo) #o que constrói o pdf
    print(f" Relatório gerado com sucesso: {PDF_SAIDA}")


if __name__ == "__main__": #execução da função
    gerar_pdf()
