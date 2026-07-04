"""
main.py
Ponto de entrada do programa. Roda o scanner e mostra o relatório.

Uso:
    python main.py caminho/para/Dockerfile
    (se não passar caminho, usa example_files/Dockerfile por padrão)
"""

import sys
from scanner import run_scan, calculate_score
from report_generator import print_report, save_report_txt


def main():
    if len(sys.argv) > 1:
        dockerfile_path = sys.argv[1]
    else:
        dockerfile_path = "example_files/Dockerfile"

    print(f"Analisando: {dockerfile_path}\n")

    results = run_scan(dockerfile_path)
    passed, total = calculate_score(results)

    print_report(results, passed, total)
    save_report_txt(results, passed, total)


if __name__ == "__main__":
    main()
