"""Ponto de entrada: python main.py"""
from __future__ import annotations
import argparse
from pathlib import Path
from src.tratamento import executar_tratamento
RAIZ = Path(__file__).resolve().parent

def main() -> None:
    parser = argparse.ArgumentParser(description="Trabalho DGT2823 - Pandas")
    parser.add_argument("--entrada", type=Path, default=RAIZ / "data" / "dados_originais.csv")
    parser.add_argument("--saida", type=Path, default=RAIZ / "resultados" / "dados_tratados.csv")
    parser.add_argument("--relatorio", type=Path, default=RAIZ / "resultados" / "relatorio_execucao.txt")
    parser.add_argument("--resumido", action="store_true")
    args = parser.parse_args()
    executar_tratamento(args.entrada, args.saida, args.relatorio,
                        mostrar_etapas=not args.resumido)
if __name__ == "__main__":
    main()
