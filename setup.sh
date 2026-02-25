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
    pip install pylint pre-commit black isort
fi

if [ ! -f ".pylintrc" ]; then
    echo "Gerando arquivo .pylintrc..."
    pylint --generate-rcfile > .pylintrc
fi


if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "Criando .pre-commit-config.yaml padrão..."

cat <<EOF > .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/pylint
    rev: v3.1.0
    hooks:
      - id: pylint
EOF

fi

echo "Instalando hooks do pre-commit..."
pre-commit install

echo "=============================="
echo " Setup concluído com sucesso "
echo "=============================="