import re

# -------------------- VALIDADOR DE CNPJ --------------------
def validar_cnpj(cnpj):
    """Valida CNPJ seguindo a regra dos dígitos verificadores."""

    # remover tudo que não for número
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False

    # rejeitar CNPJ com todos dígitos iguais (111..., 222..., etc)
    if cnpj == cnpj[0] * 14:
        return False

    # cálculo dos dígitos verificadores
    def calcular_dv(cnpj_sem_dv, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj_sem_dv, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    # primeiro dígito verificador
    dv1 = calcular_dv(cnpj[:12], [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    # segundo dígito verificador
    dv2 = calcular_dv(cnpj[:12] + dv1, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])

    return cnpj[-2:] == dv1 + dv2