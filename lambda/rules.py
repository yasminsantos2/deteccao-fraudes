"""
rules.py — As 5 regras de detecção de fraude

Cada função recebe UMA transação (dicionário) e retorna True se a regra foi violada.
Princípio aplicado: SRP — cada função faz UMA coisa só.
"""

from datetime import datetime

# --------------------------------------------------------------------------
# CONSTANTES — altere aqui, não no meio do código
# --------------------------------------------------------------------------
VALOR_ALTO_LIMITE     = 10_000.00
HORA_MADRUGADA_INICIO = 0
HORA_MADRUGADA_FIM    = 5
PAIS_BASE             = "BR"
VELOCITY_LIMITE       = 5
VALOR_MINIMO_VALIDO   = 0.01


def regra_valor_alto(transacao: dict) -> bool:
    try:
        return float(transacao["amount"]) > VALOR_ALTO_LIMITE
    except (KeyError, ValueError, TypeError):
        return False


def regra_madrugada(transacao: dict) -> bool:
    try:
        hora = datetime.fromisoformat(transacao["timestamp"]).hour
        return HORA_MADRUGADA_INICIO <= hora <= HORA_MADRUGADA_FIM
    except (KeyError, ValueError, TypeError):
        return False


def regra_pais_estrangeiro(transacao: dict) -> bool:
    try:
        return str(transacao["country_code"]).upper().strip() != PAIS_BASE
    except (KeyError, AttributeError):
        return False


def regra_velocity(transacao: dict) -> bool:
    try:
        return int(transacao["frequency"]) > VELOCITY_LIMITE
    except (KeyError, ValueError, TypeError):
        return False


def regra_valor_invalido(transacao: dict) -> bool:
    try:
        return float(transacao["amount"]) < VALOR_MINIMO_VALIDO
    except (KeyError, ValueError, TypeError):
        return True
