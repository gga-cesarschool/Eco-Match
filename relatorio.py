import os 
os.system('cls')

import aspose.pdf as ap
from datetime import datetime
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
        "{{QTD1}}": str(dados["qtd1"]),
        "{{CLASSE1}}": dados["classe1"],
        "{{TOTAL_RESIDUOS}}": str(dados["total_residuos"]),
        "{{PERCENTUAL_RECICLAGEM}}": f"{dados['percentual']}%",
        "{{CO2}}": str(dados["co2"]),
        "{{STATUS}}": dados["status"],
        "{{DATA}}": datetime.now().strftime("%d/%m/%Y"),
        "{{CODIGO}}": str(uuid.uuid4())[:8]
    }

    # Substituir os textos no PDF
    for marcador, valor in substituicoes.items():
        absorber = ap.text.TextFragmentAbsorber(marcador)
        doc.pages.accept(absorber)

        for fragment in absorber.text_fragments:
            fragment.text = valor

    # Salvar PDF final
    nome_saida = f"certificado_{dados['empresa'].replace(' ', '_')}.pdf"
    doc.save(nome_saida)

    print("Certificado gerado:", nome_saida)