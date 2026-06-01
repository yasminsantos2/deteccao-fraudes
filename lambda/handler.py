"""
handler.py — Ponto de entrada da Lambda (só roda na AWS)

Orquestra tudo mas não contém lógica de negócio.
"""

import json, os, boto3
from datetime import datetime, timezone
from utils  import ler_csv, validar_schema
from scorer import calcular_score

BUCKET_SAIDA = os.environ.get("OUTPUT_BUCKET", "fraude-output")


def lambda_handler(event: dict, context) -> dict:
    s3 = boto3.client("s3")

    registro       = event["Records"][0]["s3"]
    bucket_entrada = registro["bucket"]["name"]
    nome_arquivo   = registro["object"]["key"]

    print(f"[INFO] Processando: s3://{bucket_entrada}/{nome_arquivo}")

    conteudo   = s3.get_object(Bucket=bucket_entrada, Key=nome_arquivo)["Body"].read().decode("utf-8")
    transacoes = ler_csv(conteudo)

    valido, erro = validar_schema(transacoes)
    if not valido:
        raise ValueError(f"CSV inválido: {erro}")

    resultados = [calcular_score(t) for t in transacoes]

    relatorio = {
        "arquivo_origem":    nome_arquivo,
        "processado_em":     datetime.now(timezone.utc).isoformat(),
        "total_transacoes":  len(resultados),
        "resumo": {
            "OK":       sum(1 for r in resultados if r["status"] == "OK"),
            "SUSPEITO": sum(1 for r in resultados if r["status"] == "SUSPEITO"),
            "FRAUDE":   sum(1 for r in resultados if r["status"] == "FRAUDE"),
        },
        "alertas":  [r for r in resultados if r["status"] != "OK"],
        "detalhes": resultados,
    }

    nome_saida = nome_arquivo.replace(".csv", "_resultado.json")
    s3.put_object(
        Bucket=BUCKET_SAIDA, Key=nome_saida,
        Body=json.dumps(relatorio, indent=2, ensure_ascii=False),
        ContentType="application/json",
    )

    print(f"[INFO] Resumo: {relatorio['resumo']}")
    return {"statusCode": 200, "body": json.dumps(relatorio["resumo"])}
