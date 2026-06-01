"""
utils.py — Leitura e validação do CSV

SRP: este módulo só sabe ler e validar dados de entrada.
"""

import csv
import io
from typing import List, Tuple

COLUNAS_OBRIGATORIAS = {
    "transaction_id", "amount", "timestamp", "country_code", "frequency"
}


def ler_csv(conteudo: str) -> List[dict]:
    leitor = csv.DictReader(io.StringIO(conteudo))
    return [dict(linha) for linha in leitor]


def validar_schema(transacoes: List[dict]) -> Tuple[bool, str]:
    if not transacoes:
        return False, "Arquivo CSV está vazio."

    colunas_faltando = COLUNAS_OBRIGATORIAS - set(transacoes[0].keys())
    if colunas_faltando:
        return False, f"Colunas ausentes: {sorted(colunas_faltando)}"

    return True, ""
