# Docker Security Auditor

Ferramenta em Python que analisa um `Dockerfile` e verifica se ele segue boas práticas de segurança baseadas no CIS Docker Benchmark. Gera um relatório com score final e detalhes de cada verificação.

Não requer Docker instalado — a análise é feita lendo o arquivo `Dockerfile` como texto puro.

## O que ele verifica

1. **Usuário não-root** — o container não deve rodar como root por padrão
2. **Versão fixa da imagem base** — evita uso da tag `latest`, que gera builds não reprodutíveis
3. **Uso seguro de ADD/COPY** — evita uso desnecessário de `ADD`, que tem riscos extras (download remoto, descompactação automática)
4. **Sem portas sensíveis expostas** — verifica exposição de portas como SSH (22), Telnet (23), FTP (21), RDP (3389)
5. **Sem segredos hardcoded** — identifica senhas, tokens ou API keys escritas diretamente no Dockerfile
6. **HEALTHCHECK configurado** — verifica se há instrução de monitoramento de saúde do container
7. **Builds reprodutíveis** — identifica uso de `apt-get upgrade` genérico, que quebra a reprodutibilidade
8. **Limpeza de cache de pacotes** — verifica se o cache do gerenciador de pacotes é limpo após instalação, reduzindo o tamanho da imagem final

## Como usar

```bash
python main.py caminho/para/seu/Dockerfile
```

Se nenhum caminho for informado, ele analisa o arquivo de exemplo em `example_files/Dockerfile`:

```bash
python main.py
```

## Saída

O programa imprime o relatório no terminal e salva uma cópia em `relatorio.txt`, com o resultado de cada regra (PASS/FAIL) e o score final.

## Estrutura do projeto

```
docker-security-auditor/
├── main.py               # ponto de entrada do programa
├── rules.py               # as 8 regras de segurança
├── scanner.py             # lê o Dockerfile e aplica as regras
├── report_generator.py    # gera o relatório em texto
└── example_files/
    └── Dockerfile          # arquivo de exemplo para testes
```

## Requisitos

Apenas Python 3.8+ (sem dependências externas).
