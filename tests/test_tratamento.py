"""Dez verificações automatizadas do trabalho DGT2823."""
import io
import subprocess
import sys
from pathlib import Path
import pandas as pd
import pytest
from src.tratamento import criar_relatorio, executar_tratamento, ler_dados, tratar_dados

RAIZ = Path(__file__).resolve().parents[1]
ORIGEM = RAIZ / "data" / "dados_originais.csv"

@pytest.fixture()
def etapas():
    return tratar_dados(ler_dados(ORIGEM))

def test_csv_tem_32_registros_e_seis_colunas(etapas):
    assert etapas.original.shape == (32, 6)
    assert etapas.original["ID"].tolist() == list(range(32))
    assert etapas.original["Calories"].isna().sum() == 2
    assert etapas.original["Date"].isna().sum() == 1

def test_original_nao_e_modificado(etapas):
    assert pd.isna(etapas.original.loc[18, "Calories"])
    assert pd.isna(etapas.original.loc[22, "Date"])
    assert etapas.original.loc[26, "Date"] == "20201226"
    assert etapas.original.loc[0, "Date"] == "'2020/12/01'"

def test_substituicao_das_calorias_nulas(etapas):
    assert etapas.apos_calorias.loc[18, "Calories"] == 0
    assert etapas.apos_calorias.loc[28, "Calories"] == 0
    assert etapas.apos_calorias["Calories"].isna().sum() == 0

def test_data_temporaria_e_removida(etapas):
    assert etapas.apos_datas_preenchidas.loc[22, "Date"] == "1900/01/01"
    assert pd.isna(etapas.apos_datas_normalizadas.loc[22, "Date"])
    assert 22 not in etapas.final["ID"].tolist()

def test_data_20201226_corrigida(etapas):
    valor = etapas.final.loc[etapas.final["ID"] == 26, "Date"].iloc[0]
    assert valor == pd.Timestamp("2020-12-26")
    assert pd.api.types.is_datetime64_any_dtype(etapas.final["Date"])

def test_saida_tem_31_linhas_e_zero_nulos(etapas):
    assert etapas.final.shape == (31, 6)
    assert int(etapas.final.isna().sum().sum()) == 0
    assert etapas.final["ID"].tolist() == [i for i in range(32) if i != 22]
    assert etapas.final["Calories"].dtype.kind in {"i", "u"}

def test_demais_valores_originais_preservados(etapas):
    assert etapas.final.loc[etapas.final["ID"] == 7, "Duration"].iloc[0] == 450
    id23 = etapas.final[etapas.final["ID"] == 23].iloc[0]
    assert (int(id23["Pulse"]), int(id23["Maxpulse"])) == (130, 101)
    assert etapas.final["Date"].eq(pd.Timestamp("2020-12-12")).sum() == 2
    assert etapas.original.loc[20, "Calories"] == 2430
    assert etapas.original.loc[21, "ID"] == 21

def test_relatorio_contem_contagens_reais(etapas):
    relatorio = criar_relatorio(etapas)
    assert "Registros: 32" in relatorio
    assert "Registros: 31" in relatorio
    assert "IDs excluídos: [22]" in relatorio
    assert "Nulos totais: 0" in relatorio

def test_execucao_salva_csv_e_relatorio(tmp_path):
    saida = tmp_path / "dados_tratados.csv"
    texto = tmp_path / "relatorio_execucao.txt"
    buffer = io.StringIO()
    etapas = executar_tratamento(ORIGEM, saida, texto, mostrar_etapas=False, fluxo=buffer)
    assert saida.is_file() and texto.is_file()
    nova_leitura = pd.read_csv(saida, sep=";")
    assert nova_leitura.shape == (31, 6)
    assert nova_leitura.loc[nova_leitura["ID"] == 26, "Date"].iloc[0] == "2020/12/26"
    assert "BASE TRATADA" in texto.read_text(encoding="utf-8")
    assert etapas.final.shape == (31, 6)

def test_main_rodando_de_outro_diretorio(tmp_path):
    concluido = subprocess.run(
        [sys.executable, str(RAIZ / "main.py"), "--resumido",
         "--saida", str(tmp_path / "limpos.csv"),
         "--relatorio", str(tmp_path / "resumo.txt")],
        cwd=tmp_path, capture_output=True, text=True, check=False)
    assert concluido.returncode == 0, concluido.stderr
    assert (tmp_path / "limpos.csv").is_file()
    assert (tmp_path / "resumo.txt").is_file()
