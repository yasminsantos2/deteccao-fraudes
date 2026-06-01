"""
scorer.py — Calcula o score e define o status final

Para adicionar uma nova regra: inclua na lista REGRAS. Nada mais muda.
"""

from rules import (
    regra_valor_alto, regra_madrugada, regra_pais_estrangeiro,
    regra_velocity, regra_valor_invalido,
)

REGRAS = [
    ("valor_alto",       regra_valor_alto,       25),
    ("madrugada",        regra_madrugada,         25),
    ("pais_estrangeiro", regra_pais_estrangeiro,  25),
    ("velocity",         regra_velocity,          25),
    ("valor_invalido",   regra_valor_invalido,    25),
]

THRESHOLD_FRAUDE   = 50
THRESHOLD_SUSPEITO = 25


def classificar(score: int) -> str:
    if score >= THRESHOLD_FRAUDE:
        return "FRAUDE"
    elif score >= THRESHOLD_SUSPEITO:
        return "SUSPEITO"
    return "OK"


def calcular_score(transacao: dict) -> dict:
    score = 0
    regras_violadas = []

    for nome, funcao, pontos in REGRAS:
        if funcao(transacao):
            score += pontos
            regras_violadas.append(nome)

    return {
        "transaction_id":  transacao.get("transaction_id", "DESCONHECIDO"),
        "score":           score,
        "status":          classificar(score),
        "regras_violadas": regras_violadas,
    }
