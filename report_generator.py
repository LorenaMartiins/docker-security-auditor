"""
report_generator.py
Gera um relatório legível a partir dos resultados do scanner.
Versão inicial: texto no terminal. Depois dá pra evoluir pra PDF com fpdf2.
"""


def print_report(results, passed, total):
    print("=" * 60)
    print("  RELATÓRIO DE AUDITORIA DE SEGURANÇA - DOCKERFILE")
    print("=" * 60)
    print()

    for r in results:
        icon = "✅" if r["status"] == "PASS" else "❌"
        print(f"{icon} [{r['id']}] {r['title']} — {r['status']}")
        print(f"   {r['detail']}")
        print()

    print("-" * 60)
    percentage = round((passed / total) * 100, 1)
    print(f"SCORE FINAL: {passed}/{total} regras aprovadas ({percentage}%)")
    print("=" * 60)


def save_report_txt(results, passed, total, output_path="relatorio.txt"):
    """Salva o relatório em um arquivo .txt (útil pra entregar ao cliente)."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("RELATÓRIO DE AUDITORIA DE SEGURANÇA - DOCKERFILE\n")
        f.write("=" * 60 + "\n\n")

        for r in results:
            f.write(f"[{r['id']}] {r['title']} — {r['status']}\n")
            f.write(f"   {r['detail']}\n\n")

        percentage = round((passed / total) * 100, 1)
        f.write("-" * 60 + "\n")
        f.write(f"SCORE FINAL: {passed}/{total} regras aprovadas ({percentage}%)\n")

    print(f"\nRelatório salvo em: {output_path}")
