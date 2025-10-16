#!/bin/bash

# Script de setup para Sistema de Cálculo de Perdas - Cana-de-Açúcar
# Autor: Sistema Automatizado
# Data: $(date)

echo "🌾 =============================================="
echo "🌾 SETUP - SISTEMA CANA-DE-AÇÚCAR"
echo "🌾 =============================================="

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    echo "💡 Visite: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    echo "💡 Visite: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker e Docker Compose encontrados!"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não está instalado. Por favor, instale Python 3.8+ primeiro."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION encontrado!"

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências Python
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Dependências Python instaladas!"

# Copiar arquivo de configuração
if [ ! -f ".env" ]; then
    echo "⚙️  Criando arquivo de configuração..."
    cp .env.example .env
    echo "✅ Arquivo .env criado! Você pode editá-lo se necessário."
fi

# Configurar permissões para scripts
chmod +x docker/init-scripts/setup.sh

echo ""
echo "🚀 =============================================="
echo "🚀 PRÓXIMOS PASSOS:"
echo "🚀 =============================================="
echo ""
echo "1. 🐳 Iniciar banco Oracle com Docker:"
echo "   docker-compose up -d"
echo ""
echo "2. ⏳ Aguardar banco inicializar (pode levar alguns minutos)"
echo ""
echo "3. 🔍 Verificar se banco está rodando:"
echo "   docker-compose logs oracle-db"
echo ""
echo "4. ▶️  Executar o sistema:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "5. 🧪 Testar conexão com banco:"
echo "   python main.py --test-connection"
echo ""
echo "📚 Para mais detalhes, consulte o README.md"
echo ""
echo "✅ Setup concluído com sucesso!"