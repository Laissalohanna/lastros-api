#!/bin/bash

set -e 

echo "=============================="
echo " Iniciando setup do ambiente "
echo "=============================="

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
else
    echo "Ambiente virtual já existe."
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Atualizando pip..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "Instalando dependências principais..."
    pip install -r requirements.txt
fi

if [ -f "requirements-dev.txt" ]; then
    echo "Instalando dependências de desenvolvimento..."
    pip install -r requirements-dev.txt
else
    echo "Instalando ferramentas dev manualmente..."
    pip install pylint pre-commit black isort mypy bandit types-requests
fi

if [ ! -f ".pylintrc" ]; then
    echo "Gerando arquivo .pylintrc..."
    pylint --generate-rcfile > .pylintrc
fi

if [ ! -f "mypy.ini" ]; then
    echo "Criando mypy.ini..."
cat <<EOF > mypy.ini
[mypy]
python_version = 3.11
strict = True
ignore_missing_imports = True
EOF
fi

if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "Criando .pre-commit-config.yaml padrão..."

cat <<EOF > .pre-commit-config.yaml
repos:
  - repo: https://github.com/pycqa/isort
    rev: 8.0.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/psf/black
    rev: 26.1.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.8
    hooks:
      - id: bandit
        args: ["-ll"]

  - repo: local
    hooks:
      - id: pylint
        name: pylint
        entry: pylint
        language: system
        types: [python]
        args:
          [
            "-rn",
            "-sn",
            "--rcfile=.pylintrc",
            "--load-plugins=pylint.extensions.docparams"
          ]
EOF

fi

echo "Instalando hooks do pre-commit..."
pre-commit install

echo "Rodando pre-commit pela primeira vez..."
pre-commit run --all-files || true

echo "=============================="
echo " Setup concluído com sucesso "
echo "=============================="