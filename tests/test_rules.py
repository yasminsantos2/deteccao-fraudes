"""
test_rules.py — 32 testes das 5 regras

Rodar: pytest tests/ -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lambda"))

from rules import (
    regra_valor_alto, regra_madrugada, regra_pais_estrangeiro,
    regra_velocity, regra_valor_invalido,
)


class TestRegraValorAlto:
    def test_valor_acima_do_limite_dispara(self):
        assert regra_valor_alto({"amount": "15000.00"}) is True

    def test_valor_abaixo_nao_dispara(self):
        assert regra_valor_alto({"amount": "500.00"}) is False

    def test_valor_exato_no_limite_nao_dispara(self):
        assert regra_valor_alto({"amount": "10000.00"}) is False

    def test_campo_ausente_nao_quebra(self):
        assert regra_valor_alto({}) is False

    def test_valor_int_funciona(self):
        assert regra_valor_alto({"amount": 20000}) is True


class TestRegraMarugada:
    def test_as_3h_dispara(self):
        assert regra_madrugada({"timestamp": "2024-01-15T03:15:00"}) is True

    def test_meia_noite_dispara(self):
        assert regra_madrugada({"timestamp": "2024-01-15T00:00:00"}) is True

    def test_as_5h59_dispara(self):
        assert regra_madrugada({"timestamp": "2024-01-15T05:59:00"}) is True

    def test_as_6h_nao_dispara(self):
        assert regra_madrugada({"timestamp": "2024-01-15T06:00:00"}) is False

    def test_horario_comercial_nao_dispara(self):
        assert regra_madrugada({"timestamp": "2024-01-15T14:30:00"}) is False

    def test_timestamp_invalido_nao_quebra(self):
        assert regra_madrugada({"timestamp": "data-invalida"}) is False

    def test_campo_ausente_nao_quebra(self):
        assert regra_madrugada({}) is False


class TestRegraPaisEstrangeiro:
    def test_eua_dispara(self):
        assert regra_pais_estrangeiro({"country_code": "US"}) is True

    def test_argentina_dispara(self):
        assert regra_pais_estrangeiro({"country_code": "AR"}) is True

    def test_brasil_nao_dispara(self):
        assert regra_pais_estrangeiro({"country_code": "BR"}) is False

    def test_minuscula_normalizado(self):
        assert regra_pais_estrangeiro({"country_code": "br"}) is False

    def test_campo_ausente_nao_quebra(self):
        assert regra_pais_estrangeiro({}) is False


class TestRegraVelocity:
    def test_frequencia_alta_dispara(self):
        assert regra_velocity({"frequency": "8"}) is True

    def test_no_limite_nao_dispara(self):
        assert regra_velocity({"frequency": "5"}) is False

    def test_frequencia_normal_nao_dispara(self):
        assert regra_velocity({"frequency": "2"}) is False

    def test_frequencia_int_funciona(self):
        assert regra_velocity({"frequency": 10}) is True

    def test_campo_ausente_nao_quebra(self):
        assert regra_velocity({}) is False


class TestRegraValorInvalido:
    def test_negativo_dispara(self):
        assert regra_valor_invalido({"amount": "-50.00"}) is True

    def test_zero_dispara(self):
        assert regra_valor_invalido({"amount": "0"}) is True

    def test_texto_dispara(self):
        assert regra_valor_invalido({"amount": "abc"}) is True

    def test_campo_ausente_dispara(self):
        assert regra_valor_invalido({}) is True

    def test_valor_valido_nao_dispara(self):
        assert regra_valor_invalido({"amount": "200.00"}) is False

    def test_valor_minimo_nao_dispara(self):
        assert regra_valor_invalido({"amount": "0.01"}) is False


class TestScorer:
    def setup_method(self):
        from scorer import calcular_score
        self.calcular_score = calcular_score

    def test_transacao_ok(self):
        t = {"transaction_id": "TX001", "amount": "500.00",
             "timestamp": "2024-01-15T14:30:00", "country_code": "BR", "frequency": "2"}
        r = self.calcular_score(t)
        assert r["score"] == 0 and r["status"] == "OK"

    def test_uma_regra_suspeito(self):
        t = {"transaction_id": "TX002", "amount": "15000.00",
             "timestamp": "2024-01-15T14:30:00", "country_code": "BR", "frequency": "2"}
        r = self.calcular_score(t)
        assert r["score"] == 25 and r["status"] == "SUSPEITO"

    def test_duas_regras_fraude(self):
        t = {"transaction_id": "TX003", "amount": "20000.00",
             "timestamp": "2024-01-15T03:00:00", "country_code": "BR", "frequency": "2"}
        r = self.calcular_score(t)
        assert r["score"] == 50 and r["status"] == "FRAUDE"

    def test_score_maximo(self):
        t = {"transaction_id": "TX008", "amount": "-999.00",
             "timestamp": "2024-01-15T02:45:00", "country_code": "US", "frequency": "10"}
        r = self.calcular_score(t)
        assert r["score"] >= 75 and r["status"] == "FRAUDE"
