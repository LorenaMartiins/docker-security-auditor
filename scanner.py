"""
scanner.py
Lê um Dockerfile e roda todas as regras de segurança contra ele.
"""

from rules import ALL_RULES


def load_dockerfile(path):
    """Abre o Dockerfile e retorna a lista de linhas."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


def run_scan(path):
    """Roda todas as regras contra o Dockerfile e retorna a lista de resultados."""
    lines = load_dockerfile(path)

    results = []
    for rule_function in ALL_RULES:
        result = rule_function(lines)
        results.append(result)

    return results


def calculate_score(results):
    """Calcula quantas regras passaram, do total."""
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    return passed, total
