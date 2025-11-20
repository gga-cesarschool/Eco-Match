import os 
os.system('cls')

import aspose.pdf as ap       #Aqui é a importação do aspose.pdf que vai interagir e editar o nosso código
from datetime import datetime #Importação a classe para trabalhar com datas 
import uuid


def gerar_certificados(dados):
    doc = ap.Document("Certificado de Descarte Correto.pdf")

 # Lista de substituições (marcador → valor)
    substituicoes = {
        "{{EMPRESA}}": dados["Empresa"],
        "{{CNPJ}}": dados["cnpj"],
        "{{UNIDADE}}": dados["unidade"],
        "{{RESPONSAVEL}}": dados["responsavel"],
        "{{ENDERECO}}": dados["endereco"],
        "{{TIPO1}}": dados["tipo1"], 
        "{{QTD1}}": str(dados["qtd1"]), # converte valores numéricos para texto
        "{{CLASSE1}}": dados["classe1"],
        "{{TOTAL_RESIDUOS}}": str(dados["total_residuos"]), 
        "{{PERCENTUAL_RECICLAGEM}}": f"{dados['percentual']}%", #Adiciona o símbolo de porcentagem depois do valor
        "{{CO2}}": str(dados["co2"]),
        "{{STATUS}}": dados["status"],
        "{{DATA}}": datetime.now().strftime("%d/%m/%Y"), #Para gerar data atual: dia , mes e ano
        "{{CODIGO}}": str(uuid.uuid4())[:8] # Essa parte vai criar um código de 8 caracteres para o certificado
    }

    # Substituir os textos no PDF do relatório
    for marcador, valor in substituicoes.items(): #Iteração de cada marcador no dicionário
        absorber = ap.text.TextFragmentAbsorber(marcador)
        doc.pages.accept(absorber) # vai buscando por todo doc

        for fragment in absorber.text_fragments: #Para cada ponto do PDF onde o marcador foi encontrado, substitui seu texto pelo valor correspondente --> Dar enfase
            fragment.text = valor

    # Salvar PDF final
    nome_saida = f"certificado_{dados['empresa']. replace(' ', '_')}.pdf" #Cria o nome do arqv final
    doc.save(nome_saida) #Salva o novo PDF com todos os dados preenchidos


    print("Certificado gerado:", nome_saida)