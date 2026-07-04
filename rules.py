"""
rules.py
Cada função recebe a lista de linhas do Dockerfile e retorna um dicionário
com o resultado da checagem: PASS ou FAIL.
"""

import re


def check_root_user(lines):
    """Regra 1: Não deve rodar como usuário root."""
    text = "\n".join(lines)
    has_user_instruction = re.search(r"^\s*USER\s+(\S+)", text, re.MULTILINE | re.IGNORECASE)

    if not has_user_instruction:
        return {
            "id": "R1",
            "title": "Usuário não-root definido",
            "status": "FAIL",
            "detail": "Nenhuma instrução USER encontrada. O container roda como root por padrão."
        }

    user = has_user_instruction.group(1)
    if user.lower() == "root":
        return {
            "id": "R1",
            "title": "Usuário não-root definido",
            "status": "FAIL",
            "detail": f"Instrução 'USER root' encontrada explicitamente."
        }

    return {
        "id": "R1",
        "title": "Usuário não-root definido",
        "status": "PASS",
        "detail": f"Container configurado para rodar como usuário '{user}'."
    }


def check_latest_tag(lines):
    """Regra 2: Não deve usar tag 'latest' na imagem base."""
    text = "\n".join(lines)
    from_lines = re.findall(r"^\s*FROM\s+(\S+)", text, re.MULTILINE | re.IGNORECASE)

    for image in from_lines:
        if image.endswith(":latest") or ":" not in image:
            return {
                "id": "R2",
                "title": "Imagem base com versão fixa",
                "status": "FAIL",
                "detail": f"Imagem '{image}' usa tag 'latest' (implícita ou explícita). Prefira uma versão fixa, ex: python:3.12-slim."
            }

    return {
        "id": "R2",
        "title": "Imagem base com versão fixa",
        "status": "PASS",
        "detail": "Todas as imagens base usam tags de versão específicas."
    }


def check_add_vs_copy(lines):
    """Regra 3: Evitar ADD quando COPY é suficiente."""
    text = "\n".join(lines)
    add_lines = re.findall(r"^\s*ADD\s+(.+)$", text, re.MULTILINE | re.IGNORECASE)

    risky_adds = [line for line in add_lines if not (line.strip().startswith("http") or ".tar" in line)]

    if risky_adds:
        return {
            "id": "R3",
            "title": "Uso seguro de ADD/COPY",
            "status": "FAIL",
            "detail": f"Encontrado(s) {len(risky_adds)} uso(s) de ADD para cópia simples de arquivo. Use COPY, que é mais previsível e seguro."
        }

    return {
        "id": "R3",
        "title": "Uso seguro de ADD/COPY",
        "status": "PASS",
        "detail": "Nenhum uso arriscado de ADD encontrado."
    }


def check_exposed_ports(lines):
    """Regra 4: Não expor portas sensíveis desnecessárias."""
    text = "\n".join(lines)
    exposed = re.findall(r"^\s*EXPOSE\s+(.+)$", text, re.MULTILINE | re.IGNORECASE)

    sensitive_ports = {"22", "3389", "23", "21"}
    found_sensitive = []

    for line in exposed:
        ports = re.findall(r"\d+", line)
        for p in ports:
            if p in sensitive_ports:
                found_sensitive.append(p)

    if found_sensitive:
        return {
            "id": "R4",
            "title": "Sem exposição de portas sensíveis",
            "status": "FAIL",
            "detail": f"Porta(s) sensível(is) exposta(s): {', '.join(found_sensitive)} (SSH, Telnet, FTP, RDP)."
        }

    return {
        "id": "R4",
        "title": "Sem exposição de portas sensíveis",
        "status": "PASS",
        "detail": "Nenhuma porta sensível exposta explicitamente."
    }


def check_hardcoded_secrets(lines):
    """Regra 5: Não deve ter senha/API key hardcoded."""
    text = "\n".join(lines)
    secret_patterns = re.findall(
        r"^\s*(ENV|ARG)\s+.*(PASSWORD|SECRET|API_KEY|TOKEN|PASSWD)\s*=",
        text,
        re.MULTILINE | re.IGNORECASE
    )

    if secret_patterns:
        return {
            "id": "R5",
            "title": "Sem segredos hardcoded",
            "status": "FAIL",
            "detail": f"Encontrada(s) {len(secret_patterns)} variável(is) com nome sugestivo de segredo (senha/API key/token) diretamente no Dockerfile."
        }

    return {
        "id": "R5",
        "title": "Sem segredos hardcoded",
        "status": "PASS",
        "detail": "Nenhum segredo hardcoded encontrado nas instruções ENV/ARG."
    }


def check_healthcheck(lines):
    """Regra 6: Deve ter HEALTHCHECK definido."""
    text = "\n".join(lines)
    has_healthcheck = re.search(r"^\s*HEALTHCHECK\s+", text, re.MULTILINE | re.IGNORECASE)

    if not has_healthcheck:
        return {
            "id": "R6",
            "title": "HEALTHCHECK configurado",
            "status": "FAIL",
            "detail": "Nenhuma instrução HEALTHCHECK encontrada. Recomendado para monitoramento de saúde do container."
        }

    return {
        "id": "R6",
        "title": "HEALTHCHECK configurado",
        "status": "PASS",
        "detail": "Instrução HEALTHCHECK presente."
    }


def check_pinned_upgrade(lines):
    """Regra 7: Evitar apt-get upgrade sem versões fixas (builds não reprodutíveis)."""
    text = "\n".join(lines)
    has_upgrade = re.search(r"apt-get\s+upgrade", text, re.IGNORECASE)

    if has_upgrade:
        return {
            "id": "R7",
            "title": "Builds reprodutíveis (sem upgrade genérico)",
            "status": "FAIL",
            "detail": "Uso de 'apt-get upgrade' encontrado. Isso gera builds não reprodutíveis, pois pega sempre as últimas versões disponíveis."
        }

    return {
        "id": "R7",
        "title": "Builds reprodutíveis (sem upgrade genérico)",
        "status": "PASS",
        "detail": "Nenhum 'apt-get upgrade' genérico encontrado."
    }


def check_cache_cleanup(lines):
    """Regra 8: Limpar cache do gerenciador de pacotes após instalar."""
    text = "\n".join(lines)
    has_apt_install = re.search(r"apt-get\s+install", text, re.IGNORECASE)
    has_cleanup = re.search(r"rm\s+-rf\s+/var/lib/apt/lists", text, re.IGNORECASE)

    if has_apt_install and not has_cleanup:
        return {
            "id": "R8",
            "title": "Limpeza de cache de pacotes",
            "status": "FAIL",
            "detail": "Uso de 'apt-get install' sem limpeza posterior do cache (/var/lib/apt/lists/*). Isso aumenta o tamanho final da imagem desnecessariamente."
        }

    return {
        "id": "R8",
        "title": "Limpeza de cache de pacotes",
        "status": "PASS",
        "detail": "Cache de pacotes limpo corretamente ou não aplicável."
    }


# Lista com todas as regras -- adicione novas funções aqui conforme evoluir o projeto
ALL_RULES = [
    check_root_user,
    check_latest_tag,
    check_add_vs_copy,
    check_exposed_ports,
    check_hardcoded_secrets,
    check_healthcheck,
    check_pinned_upgrade,
    check_cache_cleanup,
]
