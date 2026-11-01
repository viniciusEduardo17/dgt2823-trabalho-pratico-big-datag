"""Leitura, exploração e tratamento do dataset da atividade DGT2823."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO
import io
import pandas as pd

COLUNAS = ("ID", "Duration", "Date", "Pulse", "Maxpulse", "Calories")
FORMATO_DATA = "%Y/%m/%d"
DATA_SUBSTITUTA = "1900/01/01"
DATA_IRREGULAR = "20201226"
DATA_CORRIGIDA = "2020/12/26"

@dataclass
class EtapasTratamento:
    original: pd.DataFrame
    apos_calorias: pd.DataFrame
    apos_datas_preenchidas: pd.DataFrame
    apos_datas_normalizadas: pd.DataFrame
    final: pd.DataFrame

def ler_dados(caminho: str | Path) -> pd.DataFrame:
    dados = pd.read_csv(caminho, sep=";", engine="python",
                        encoding="utf-8", dtype={"Date": "string"})
    if tuple(dados.columns) != COLUNAS:
        raise ValueError(f"Colunas inválidas: {list(dados.columns)}")
    return dados

def tratar_dados(original: pd.DataFrame) -> EtapasTratamento:
    dados = original.copy(deep=True)
    dados["Calories"] = pd.to_numeric(dados["Calories"], errors="raise").fillna(0)
    apos_calorias = dados.copy(deep=True)
    dados["Date"] = dados["Date"].astype("string").fillna(DATA_SUBSTITUTA)
    apos_datas_preenchidas = dados.copy(deep=True)
    dados["Date"] = dados["Date"].str.strip().str.strip("'\"")
    dados["Date"] = dados["Date"].replace({DATA_SUBSTITUTA: pd.NA})
    dados["Date"] = dados["Date"].replace({DATA_IRREGULAR: DATA_CORRIGIDA})
    dados["Date"] = pd.to_datetime(dados["Date"], format=FORMATO_DATA, errors="raise")
    apos_datas_normalizadas = dados.copy(deep=True)
    dados = dados.dropna(subset=["Date"]).copy()
    dados["Calories"] = dados["Calories"].astype("int64")
    return EtapasTratamento(
        original.copy(deep=True), apos_calorias,
        apos_datas_preenchidas, apos_datas_normalizadas, dados)

def resumo_dataframe(dados: pd.DataFrame) -> str:
    buffer = io.StringIO()
    dados.info(buf=buffer, memory_usage="deep", show_counts=True)
    return (
        f"Dimensões: {len(dados)} linhas x {len(dados.columns)} colunas\n"
        f"Nulos por coluna:\n{dados.isna().sum().to_string()}\n"
        f"Memória estimada: {dados.memory_usage(index=True, deep=True).sum()} bytes\n"
        f"\nInformações gerais:\n{buffer.getvalue()}"
        f"\nPrimeiras 10 linhas:\n{dados.head(10).to_string(index=False)}\n"
        f"\nÚltimas 10 linhas:\n{dados.tail(10).to_string(index=False)}")

def criar_relatorio(etapas: EtapasTratamento) -> str:
    orig, final = etapas.original, etapas.final
    return (
        "DGT2823 - TRABALHO PRÁTICO - RELATÓRIO DE EXECUÇÃO\n"
        "========================================================\n\n"
        "BASE ORIGINAL\n"
        f"Registros: {len(orig)} | Colunas: {len(orig.columns)}\n"
        f"Calories ausentes: {int(orig['Calories'].isna().sum())}\n"
        f"Date ausentes: {int(orig['Date'].isna().sum())}\n\n"
        "TRANSFORMAÇÕES\n"
        "Calorias ausentes substituídas por 0: 2\n"
        "Datas temporariamente preenchidas com 1900/01/01: 1\n"
        "Datas irregulares 20201226 corrigidas: 1\n"
        f"Registros excluídos por data ausente: {len(orig)-len(final)}\n"
        f"IDs excluídos: {sorted(set(orig['ID'])-set(final['ID']))}\n\n"
        "BASE TRATADA\n"
        f"Registros: {len(final)} | Colunas: {len(final.columns)}\n"
        f"Nulos totais: {int(final.isna().sum().sum())}\n"
        f"Tipo de Date: {final['Date'].dtype}\n"
        f"Tipo de Calories: {final['Calories'].dtype}\n\n"
        "OBSERVAÇÕES DE FIDELIDADE AO ENUNCIADO\n"
        "- Aspas simples das datas são removidas antes do to_datetime.\n"
        "- 1900/01/01 é válido sintaticamente, mas removido por instrução da atividade.\n"
        "- ID 21 foi recomposto de uma quebra visual de linha no PDF.\n"
        "- Duração 450 (ID 7), duplicidade (ID 11/12) e Pulse>Maxpulse (ID 23) "
        "foram preservados, pois o roteiro não autoriza sua correção.\n")

def executar_tratamento(entrada: str | Path, saida: str | Path,
                        relatorio: str | Path, *, mostrar_etapas: bool = True,
                        fluxo: TextIO | None = None) -> EtapasTratamento:
    import sys
    destino = fluxo if fluxo is not None else sys.stdout
    etapas = tratar_dados(ler_dados(entrada))
    pd.set_option("display.max_rows", 9999)
    if mostrar_etapas:
        print("\n=== CONJUNTO ORIGINAL ===\n", resumo_dataframe(etapas.original), file=destino)
        for titulo, dados in (
            ("CALORIAS NULAS SUBSTITUÍDAS", etapas.apos_calorias),
            ("DATAS TEMPORARIAMENTE PREENCHIDAS", etapas.apos_datas_preenchidas),
            ("DATAS EM DATETIME", etapas.apos_datas_normalizadas),
            ("RESULTADO FINAL", etapas.final)
        ):
            print(f"\n=== {titulo} ===\n", dados.to_string(index=False), file=destino)
    caminho_saida, caminho_relatorio = Path(saida), Path(relatorio)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    caminho_relatorio.parent.mkdir(parents=True, exist_ok=True)
    etapas.final.to_csv(caminho_saida, sep=";", index=False,
                        date_format="%Y/%m/%d", encoding="utf-8")
    conteudo = criar_relatorio(etapas)
    caminho_relatorio.write_text(conteudo, encoding="utf-8")
    print("\n" + conteudo, file=destino)
    print(f"CSV tratado salvo em: {caminho_saida.resolve()}", file=destino)
    print(f"Relatório salvo em: {caminho_relatorio.resolve()}", file=destino)
    return etapas
