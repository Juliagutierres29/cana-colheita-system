# Makefile para Sistema de Cálculo de Perdas - Cana-de-Açúcar

.PHONY: help install start stop test clean logs status

# Configurações
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

help: ## Mostra esta mensagem de ajuda
	@echo "🌾 Sistema de Cálculo de Perdas - Cana-de-Açúcar"
	@echo "================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instala dependências e configura ambiente
	@echo "📦 Configurando ambiente..."
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; echo "⚙️ Arquivo .env criado"; fi
	@echo "✅ Instalação concluída!"

start: ## Inicia o banco Oracle via Docker
	@echo "🐳 Iniciando banco Oracle..."
	docker-compose up -d
	@echo "⏳ Aguardando inicialização do banco..."
	@sleep 10
	@echo "✅ Banco iniciado! (pode levar alguns minutos para estar pronto)"

stop: ## Para o banco Oracle
	@echo "🛑 Parando serviços..."
	docker-compose down
	@echo "✅ Serviços parados!"

test: ## Testa conexão com o banco
	@echo "🧪 Testando conexão..."
	$(PYTHON) main.py --test-connection

run: ## Executa o sistema principal
	@echo "🚀 Iniciando sistema..."
	$(PYTHON) main.py

logs: ## Mostra logs do banco Oracle
	@echo "📋 Logs do Oracle:"
	docker-compose logs -f oracle-db

status: ## Mostra status dos serviços
	@echo "📊 Status dos serviços:"
	docker-compose ps

clean: ## Remove containers e volumes (CUIDADO: apaga dados)
	@echo "⚠️ Removendo containers e volumes..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Limpeza concluída!"

setup: install start ## Setup completo (instalar + iniciar banco)
	@echo "🎉 Setup completo realizado!"
	@echo "💡 Execute 'make test' para testar a conexão"
	@echo "💡 Execute 'make run' para usar o sistema"

dev: ## Modo desenvolvimento (logs em tempo real)
	@echo "🔧 Modo desenvolvimento..."
	docker-compose up

backup: ## Faz backup dos dados JSON
	@echo "💾 Fazendo backup..."
	@mkdir -p backup/$(shell date +%Y%m%d_%H%M%S)
	@cp -r data/* backup/$(shell date +%Y%m%d_%H%M%S)/ 2>/dev/null || true
	@echo "✅ Backup realizado!"

# Aliases para comandos comuns
build: install ## Alias para install
init: setup ## Alias para setup
deploy: start ## Alias para start