# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="https://www.fiap.com.br/wp-content/themes/fiap2016/images/sharing/fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# 🌾 Sistema de Cálculo de Perdas na Colheita de Cana-de-Açúcar

## Grupo de Desenvolvimento - Cana Colheita System

## 👨‍🎓 Integrantes: 
- <a>Julia Gutierres Fernandes Souza</a>
- <a>Everton Marinho Souza</a>
- <a>Matheus Ribeiro Marteletti</a> 
- <a>Raimunda Nayara Mendes dos Santos</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/sabrina-otoni/">Sabrina Otoni</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andre-godoy/">André Godoy</a>

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Oracle](https://img.shields.io/badge/Oracle-F80000?style=flat&logo=oracle&logoColor=white)](https://www.oracle.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

## 📜 Descrição

Sistema completo em Python para calcular perdas durante a colheita de cana-de-açúcar, com integração ao banco de dados Oracle e PostgreSQL via Docker. O projeto foi desenvolvido como parte do curso da FIAP e implementa todos os tipos de dados obrigatórios (Lista, Tupla, Dicionário e Tabela de Memória) para análise de dados agrícolas.

**🎯 Objetivo**: Fornecer uma ferramenta robusta e precisa para produtores rurais calcularem e minimizarem perdas na colheita de cana-de-açúcar, utilizando algoritmos avançados que consideram fatores ambientais e condições de cultivo.

O sistema oferece interface CLI interativa, cálculos básicos e avançados de perdas, relatórios estatísticos consolidados, backup em JSON e sistema de ajuda completo. Implementa validação robusta de dados, logging detalhado e valores padrão inteligentes baseados nas condições brasileiras de cultivo.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets/</b>: Nesta pasta ficarão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens e recursos visuais.

- <b>config/</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto (.env, configurações de banco, etc.).

- <b>document/</b>: Aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts/</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups, setup automático.

- <b>src/</b>: Todo o código fonte criado para o desenvolvimento do projeto, incluindo módulos de banco de dados (Oracle e PostgreSQL), funções de cálculo de perdas e utilitários.

- <b>data/</b>: Aqui estão armazenados os arquivos JSON de exemplo e backups automáticos das produções e relatórios gerados pelo sistema.

- <b>docker/</b>: Contém os scripts de inicialização dos bancos de dados, arquivos SQL de setup e configurações específicas do Docker.

- <b>requirements.txt</b>: Lista todas as dependências Python necessárias para executar o projeto, incluindo cx_Oracle, psycopg2, pandas e outras bibliotecas.

- <b>docker-compose.yml</b>: Configuração principal do Docker Compose para orquestração dos serviços Oracle Database.

- <b>docker-compose-postgres.yml</b>: Configuração alternativa do Docker Compose para uso do PostgreSQL como banco de dados.

- <b>main.py</b>: Arquivo principal de execução do sistema com interface CLI interativa e menu de opções.

- <b>Makefile</b>: Arquivo com comandos automatizados para facilitar tarefas comuns como instalação, execução e testes.

- <b>README.md</b>: Arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

---

## � Início Rápido

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cana-colheita-system.git
cd cana-colheita-system

# 2. Execute o setup automático
scriptscripts/setup.sh

# 3. Inicie o banco de dados
docker-compose up -d

# 4. Execute o sistema
source venv/bin/activate
python main.py
```

## �📋 Índice

- [Descrição](#-descrição)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Início Rápido](#-início-rápido)
- [Características](#-características)  
- [Pré-requisitos](#-pré-requisitos)
- [Instalação Detalhada](#-como-executar-o-código)
- [Como Usar](#-como-usar-o-sistema)
- [Algoritmos de Cálculo](#-tipos-de-cálculo)
- [Exemplos](#-exemplos)
- [Troubleshooting](#-troubleshooting)
- [Histórico de Lançamentos](#-histórico-de-lançamentos)
- [Licença](#-licença)

## 🚀 Características

- ✅ **Cálculo de Perdas**: Básico e avançado (considera fatores ambientais)
- ✅ **Modo Automático**: Busca dados do banco e usa valores padrão inteligentes
- ✅ **Banco Duplo**: Oracle (principal) + PostgreSQL (alternativo)
- ✅ **Interface CLI**: Menus interativos e coloridos
- ✅ **Backup JSON**: Persistência dual (banco + arquivos)
- ✅ **Relatórios**: Consolidados com estatísticas
- ✅ **Validação**: Dados de entrada robusta
- ✅ **Logging**: Sistema de logs detalhado
- ✅ **Valores Padrão**: Preenchimento automático baseado em condições brasileiras
- ✅ **Sistema de Ajuda**: Documentação interativa completa sobre cálculos e campos

## 📋 Tipos de Dados Implementados (Obrigatórios)

Este projeto implementa **todos os tipos de dados obrigatórios**:

- **📝 LISTA**: Histórico de cálculos, medições múltiplas, coordenadas
- **🌍 TUPLA**: Coordenadas GPS (lat, lon, alt), versão do sistema, faixas ideais
- **📊 DICIONÁRIO**: Configurações, parâmetros de cálculo, cache de resultados
- **🗃️ TABELA DE MEMÓRIA**: DataFrame pandas para análises estatísticas

### 🔍 Como testar os tipos de dados:
```bash
# Execute a demonstração completa
python demo_tipos_dados.py

# Ou use o menu do sistema:
python main.py
# Opções 7, 8, 9, 10 demonstram cada tipo
```

📖 **Documentação detalhada**: [TIPOS_DADOS_OBRIGATORIOS.md](document/TIPOS_DADOS_OBRIGATORIOS.md)

## ❓ Sistema de Ajuda Interativa

O sistema inclui uma **ajuda completa e detalhada** acessível diretamente pelo menu:

### 🚀 Como Acessar
```bash
# Execute o sistema
python main.py

# No menu principal, digite:
h    # ou H, ou ?
```

### 📚 O que a Ajuda Inclui
- 🎯 **Objetivo**: Explicação clara do sistema
- 🧮 **Cálculos**: Como funcionam os métodos básico e avançado  
- 📋 **Campos**: Descrição detalhada de todos os campos
- 📊 **Tipos de Dados**: Demonstração dos 4 tipos obrigatórios
- 🚀 **Recursos**: Lista completa de funcionalidades
- 💡 **Exemplos**: Casos de uso práticos
- 🔧 **Padrões**: Valores padrão inteligentes aplicados
- 📈 **Interpretação**: Como entender os resultados

### 🎬 Demo da Ajuda
```bash
# Demonstração independente da ajuda
python demo_ajuda.py
```

📖 **Documentação da ajuda**: [AJUDA_SISTEMA.md](document/AJUDA_SISTEMA.md)

## � Pré-requisitos

### Obrigatórios
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Docker** ([Download](https://docs.docker.com/get-docker/))
- **Docker Compose** (geralmente incluído no Docker)

### Verificar Instalação
```bash
python3 --version    # Deve mostrar 3.8 ou superior
docker --version     # Deve mostrar versão do Docker
docker-compose --version  # Deve mostrar versão do Compose
```

## 🔧 Como executar o código

**Pré-requisitos:** Python 3.8+, Docker e Docker Compose instalados

### 🔥 Método Rápido (Recomendado)

```bash
# 1. Navegue até o diretório do projeto
cd cana-colheita-system

# 2. Execute o script de setup automático
scriptscripts/setup.sh

# 3. Inicie o banco de dados Oracle
docker-compose up -d

# 4. Aguarde o banco inicializar (30 segundos)
sleep 30

# 5. Teste a conexão
source venv/bin/activate
python main.py --test-connection

# 6. Execute o sistema
python main.py
```

### 📋 Método Manual Detalhado

#### Passo 1: Verificar Pré-requisitos
```bash
# Verificar Python (deve ser 3.8+)
python3 --version

# Verificar Docker
docker --version
docker-compose --version

# Se algum não estiver instalado, consulte a seção de pré-requisitos
```

#### Passo 2: Preparar Ambiente Python
```bash
# Navegar para o diretório do projeto
cd cana-colheita-system

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

#### Passo 3: Configurar Ambiente
```bash
# Copiar arquivo de configuração
cp .env.example .env

# (Opcional) Editar configurações se necessário
# nano .env
```

#### Passo 4: Iniciar Banco de Dados

**Opção A - Oracle (Recomendado - Principal)**
```bash
# Iniciar Oracle
docker-compose up -d

# Verificar se está rodando
docker ps

# Ver logs (opcional)
docker-compose logs -f oracle-db
```

**Opção B - PostgreSQL (Alternativo)**
```bash
# Iniciar PostgreSQL (como alternativo)
docker-compose -f docker-compose-postgres.yml up -d

# Aguardar inicialização (30 segundos)
sleep 30

# Ver logs (opcional)
docker-compose -f docker-compose-postgres.yml logs -f postgres-db
```

#### Passo 5: Testar Conexão
```bash
# Certificar-se de que o ambiente virtual está ativo
source venv/bin/activate

# Testar conexão com banco
python main.py --test-connection

# Resultado esperado: "✅ Teste de conexão bem-sucedido!"
```

#### Passo 6: Executar Sistema
```bash
# Executar o sistema principal
python main.py

# O sistema mostrará o menu principal
```

### 🐳 Comandos Docker Úteis

```bash
# Ver containers rodando
docker ps

# Ver todos os containers (incluindo parados)
docker ps -a

# Ver logs do PostgreSQL
docker-compose -f docker-compose-postgres.yml logs postgres-db

# Ver logs do Oracle
docker-compose logs oracle-db

# Parar serviços PostgreSQL
docker-compose -f docker-compose-postgres.yml down

# Parar serviços Oracle
docker-compose down

# Remover volumes (CUIDADO: apaga dados)
docker-compose -f docker-compose-postgres.yml down -v

# Verificar uso de espaço Docker
docker system df
```

### 🔧 Usando Makefile (Alternativa)

```bash
# Instalação completa
make setup

# Iniciar banco
make start

# Testar conexão
make test

# Executar sistema
make run

# Ver logs
make logs

# Parar serviços
make stop

# Ver todos os comandos disponíveis
make help
```

## 🚨 Problemas Comuns e Soluções

### ❌ "Docker não encontrado"
```bash
# macOS (Homebrew)
brew install docker
brew install docker-compose

# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Verificar instalação
docker --version
docker-compose --version
```

### ❌ "Python não encontrado"
```bash
# macOS (Homebrew)
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# Verificar versão (deve ser 3.8+)
python3 --version
```

### ❌ "Erro de permissão Docker"
```bash
# Linux - Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Ou executar com sudo (não recomendado)
sudo docker-compose -f docker-compose-postgres.yml up -d
```

### ❌ "Porta 5432 já está em uso" (PostgreSQL)
```bash
# Verificar o que está usando a porta
lsof -i :5432

# Parar PostgreSQL local se existir
sudo systemctl stop postgresql
# ou
brew services stop postgresql

# Ou alterar porta no docker-compose-postgres.yml
ports:
  - "5433:5432"  # Usar porta 5433 externa
```

### ❌ "Erro cx_Oracle ou psycopg2"
```bash
# Reinstalar dependências
source venv/bin/activate
pip uninstall cx_Oracle psycopg2-binary
pip install -r requirements.txt
```

### ❌ "Container não inicia"
```bash
# Ver logs detalhados
docker-compose -f docker-compose-postgres.yml logs postgres-db

# Remover e recriar
docker-compose -f docker-compose-postgres.yml down -v
docker-compose -f docker-compose-postgres.yml up -d

# Verificar espaço em disco
docker system df
```

### ❌ "Teste de conexão falha"
```bash
# Verificar se container está rodando
docker ps

# Aguardar mais tempo para inicialização
sleep 60

# Verificar logs do banco
docker-compose -f docker-compose-postgres.yml logs postgres-db

# Testar conexão manualmente
docker exec -it cana-postgres-db psql -U cana_user -d cana_db -c "SELECT 1;"
```

## 🏃‍♂️ Guia de Início Rápido

### Para Iniciantes
```bash
# 1. Baixar projeto (se ainda não fez)
git clone <url-do-repositorio>
cd cana-colheita-system

# 2. Executar setup automático
scripts/setup.sh

# 3. Iniciar banco PostgreSQL
docker-compose -f docker-compose-postgres.yml up -d

# 4. Aguardar e testar
sleep 30
source venv/bin/activate
python main.py --test-connection

# 5. Se teste passou, executar sistema
python main.py
```

### Para Desenvolvedores
```bash
# Setup completo com logs
make setup
make start
make test
make run

# Desenvolvimento com logs em tempo real
make dev
```

### Para Administradores
```bash
# Verificar status completo
docker ps
docker stats
make status

# Backup de dados
make backup

# Limpeza completa (CUIDADO)
make clean
```

## 🎮 Como Usar o Sistema

### 1️⃣ Primeiro Uso - Menu Principal
Após executar `python main.py`, você verá:

```
🌾 SISTEMA DE CÁLCULO DE PERDAS - CANA-DE-AÇÚCAR 🌾
============================================================
💾 Banco de dados: Oracle
============================================================
1. 📝 Cadastrar nova produção
2. 🧮 Calcular perdas
3. 📊 Gerar relatórios
4. 💾 Gerenciar arquivos JSON
5. 🔍 Consultar banco de dados
6. ⚙️  Testar conexão banco
0. 🚪 Sair
============================================================
```

### 2️⃣ Fluxo Recomendado para Primeira Execução

#### A) Testar Conexão
```
Escolha: 6
✅ Conexão com banco Oracle estabelecida com sucesso!
```

#### B) Cadastrar Primeira Produção (Opcional)
```
Escolha: 1

📝 CADASTRAR NOVA PRODUÇÃO
----------------------------------------
Localização: Fazenda Teste - Talhão 1
Área plantada (hectares): 50
Quantidade colhida (toneladas): 4000
Tipo de colheita:
1. Manual
2. Mecanizada
Escolha (1 ou 2): 2

# Dados opcionais - o sistema usará valores padrão se não informados
✅ Produção cadastrada no banco com ID: 1
```

#### C) Calcular Perdas (Modo Automático)
```
Escolha: 2

🧮 CALCULAR PERDAS NA COLHEITA
----------------------------------------
Escolha a fonte dos dados:
1. 🚀 Modo automático (dados do banco + valores padrão)
2. 📝 Modo manual (informar todos os dados)
3. 📂 Carregar arquivo JSON
Escolha (1, 2 ou 3): 1

🚀 MODO AUTOMÁTICO
------------------------------
📋 Últimas 5 produções disponíveis:
┌────┬─────────────────────────┬───────────┬──────────────┬─────────────┬────────────┐
│ ID │ Localização             │ Área (ha) │ Colhida (t)  │ Tipo        │ Data       │
├────┼─────────────────────────┼───────────┼──────────────┼─────────────┼────────────┤
│  1 │ Fazenda Teste - Talhão 1│      50.0 │       4000.0 │ mecanizada  │ 15/10/2024 │
└────┴─────────────────────────┴───────────┴──────────────┴─────────────┴────────────┘

ID da produção (Enter para usar a mais recente - ID 1): [Enter]

✅ Carregando dados da produção ID 1
📍 Local: Fazenda Teste - Talhão 1
🌾 4000.0t em 50.0ha

🔧 Valores padrão aplicados:
   • idade_cana_meses: 14
   • umidade_solo: 65.0
   • temperatura_media: 26.5
   • precipitacao_mm: 100.0
💡 Estes valores são baseados em condições típicas brasileiras

🔬 Executando cálculo avançado (fatores ambientais incluídos)...

📊 RESULTADO DO CÁLCULO DE PERDAS
==================================================
 Perda estimada: 320.0 toneladas
📉 Percentual de perda: 8.0%
🎯 Produção potencial: 4320.0 toneladas
✅ Eficiência da colheita: 92.59%

💾 Salvando resultado automaticamente...
✅ Resultado salvo!
```

#### D) Gerar Relatórios
```
Escolha: 3

#### D) Gerar Relatórios
```
Escolha: 3

📊 GERAR RELATÓRIOS
----------------------------------------
Filtro por período:
1. Todos os dados
2. Últimos 30 dias
3. Período personalizado
Escolha (1, 2 ou 3): 1

📈 RELATÓRIO DE PERDAS (3 registros)
================================================================================
📊 Total colhido: 15.640,00 toneladas
💔 Total de perdas: 1.251,20 toneladas
📉 Perda média: 8,00%
```

### 📝 Exemplo Detalhado: "Cadastrar Nova Produção"

#### 🎯 Cenário Prático
Vamos cadastrar uma produção real de cana-de-açúcar com dados típicos de uma fazenda brasileira:

#### ▶️ Passo a Passo
```
python main.py
Escolha uma opção: 1

📝 CADASTRAR NOVA PRODUÇÃO
----------------------------------------
```

#### 📋 Dados para o Exemplo
**DADOS OBRIGATÓRIOS:**
```
Localização (ex: Fazenda São José - Talhão 1): Usina Santa Rita - Setor B - Quadra 15
Área plantada (hectares): 85.5
Quantidade colhida (toneladas): 7695
Tipo de colheita:
1. Manual
2. Mecanizada
Escolha (1 ou 2): 2
Data da colheita (DD/MM/AAAA): 15/10/2024
```

**DADOS OPCIONAIS (para cálculo avançado):**
```
📊 Dados para cálculo avançado (opcional):
Variedade da cana (ex: RB92579): RB966928
Idade da cana (meses): 16
Umidade do solo (%): 68
Temperatura média (°C): 28.5
Precipitação dos últimos 30 dias (mm): 75
```

**COORDENADAS GPS (opcional):**
```
🌍 Coordenadas GPS (opcional):
Latitude: -20.4521
Longitude: -49.3874
Altitude (m): 540
```

#### ✅ Resultado do Cadastro
```
💾 SALVANDO PRODUÇÃO...
✅ Produção cadastrada no banco com ID: 4

📋 RESUMO DOS DADOS CADASTRADOS:
📍 Localização: Usina Santa Rita - Setor B - Quadra 15
🌾 Área: 85.5 ha
⚖️  Quantidade colhida: 7.695 t
📏 Produtividade: 90.0 t/ha
🔧 Tipo: Mecanizada
📅 Data: 15/10/2024
🧬 Variedade: RB966928
⏰ Idade: 16 meses
💧 Umidade solo: 68%
🌡️  Temperatura: 28.5°C
🌧️  Precipitação: 75mm
🌍 GPS: (-20.4521, -49.3874, 540m)

🔧 TUPLA GPS criada: (-20.4521, -49.3874, 540)
📊 LISTA de medições inicializada
🗂️  DICIONÁRIO de metadados salvo
📋 DATAFRAME de histórico atualizado

💾 Dados salvos em JSON: data/producao_20241015_143052.json
✅ Cadastro concluído com sucesso!
```

#### 🎯 **Dicas para Preenchimento:**

**🔹 Localização:** Seja específico (Fazenda + Setor + Talhão)
```
✅ Bom: "Fazenda Santa Maria - Setor A - Talhão 7"
❌ Ruim: "Fazenda"
```

**🔹 Produtividade Típica:** 70-100 t/ha
```
✅ Normal: 85 ha → 6.800-8.500 t
⚠️  Verificar: 85 ha → 12.000 t (muito alto)
```

**🔹 Idade da Cana:** 12-18 meses ideal
```
✅ Ideal: 14-16 meses
⚠️  Cedo: 10-11 meses (menores perdas)
⚠️  Tarde: 18+ meses (maiores perdas)
```

**🔹 Umidade do Solo:** 60-70% ideal
```
✅ Ideal: 65%
⚠️  Seco: <50% (aumenta perdas)
⚠️  Encharcado: >80% (dificulta colheita)
```

#### 🚀 Próximos Passos
Após o cadastro, você pode:
1. **Calcular perdas** (opção 2) usando os dados cadastrados
2. **Gerar relatórios** (opção 3) para análise
3. **Consultar banco** (opção 5) para ver histórico
----------------------------------------
Filtro por período:
1. Todos os dados
2. Últimos 30 dias
3. Período personalizado
Escolha (1, 2 ou 3): 1

📈 RELATÓRIO DE PERDAS (1 registros)
================================================================================
📊 Total colhido: 4,000.00 toneladas
💔 Total de perdas: 360.00 toneladas
📉 Perda média: 9.00%

🔧 Por tipo de colheita:
┌─────────────┬─────────────────────────┬──────────────────────────┬─────────────────┐
│ tipo_colheita│ qtd_colhida_toneladas  │ perda_estimada_toneladas │ percentual_perda│
├─────────────┼─────────────────────────┼──────────────────────────┼─────────────────┤
│ mecanizada  │                 4000.00 │                   360.00 │            9.00 │
└─────────────┴─────────────────────────┴──────────────────────────┴─────────────────┘
```

### 3️⃣ Recursos Avançados

#### Importar Dados JSON
```
Escolha: 2 (Calcular perdas)
Escolha: 3 (Carregar arquivo JSON)

📂 Arquivos disponíveis:
1. exemplo_producao_manual.json
2. exemplo_producao_mecanizada.json
3. producao_20241015_143000.json

Escolha o arquivo (número): 1
```

#### Gerenciar Arquivos
```
Escolha: 4

💾 GERENCIAR ARQUIVOS JSON
----------------------------------------
📂 Arquivos encontrados (3):
1. exemplo_producao_manual.json
2. exemplo_producao_mecanizada.json
3. relatorio_perdas_20241015_143500.json

Opções:
1. Ver conteúdo de um arquivo
2. Excluir um arquivo
0. Voltar
```

#### Consultar Banco Diretamente
```
Escolha: 5

🔍 CONSULTAR BANCO DE DADOS
----------------------------------------
Tipos de consulta:
1. Listar produções
2. Buscar produção por ID
3. Ver parâmetros de perdas
0. Voltar
```

### 4️⃣ Dicas de Uso

#### Para Melhores Resultados
- **Use dados reais**: Quanto mais dados você fornecer, mais preciso será o cálculo
- **Calcule regularmente**: Compare diferentes períodos e condições
- **Analise relatórios**: Use as estatísticas para identificar padrões

#### Interpretação dos Resultados
- **Perda < 5%**: Excelente eficiência
- **Perda 5-10%**: Boa eficiência (normal)
- **Perda 10-15%**: Eficiência regular (investigar causas)
- **Perda > 15%**: Problemas sérios (ação imediata necessária)

#### Backup e Segurança
- Os dados são salvos automaticamente no banco PostgreSQL
- Backups JSON são criados automaticamente
- Use `make backup` para backups manuais

## 📝 Resumo dos Comandos Essenciais

### Execução Básica (Apenas 4 Comandos!)
```bash
cd cana-colheita-system
scripts/setup.sh
docker-compose -f docker-compose-postgres.yml up -d
source venv/bin/activate && python main.py
```

### Comandos de Gerenciamento
```bash
# Status dos serviços
docker ps

# Logs do banco
docker-compose -f docker-compose-postgres.yml logs postgres-db

# Parar sistema
docker-compose -f docker-compose-postgres.yml down

# Testar conexão
python main.py --test-connection

# Backup manual
make backup

# Verificar ajuda
make help
```

### Estrutura de Arquivos Gerados
```
data/
├── producao_YYYYMMDD_HHMMSS.json      # Dados de produção
├── relatorio_perdas_YYYYMMDD_HHMMSS.json  # Relatórios de perdas
└── exemplo_*.json                      # Arquivos de exemplo
```

### Status de Funcionamento
- ✅ **Oracle**: Banco principal (robusto)
- ⚠️ **PostgreSQL**: Disponível como alternativo
- ✅ **JSON**: Backup sempre funcional
- ✅ **Interface CLI**: Menu interativo
- ✅ **Relatórios**: Estatísticas detalhadas

### Próximos Passos Após Instalação
1. **Executar**: `python main.py`
2. **Testar conexão**: Opção 6 no menu
3. **Cadastrar produção**: Opção 1 no menu
4. **Calcular perdas**: Opção 2 no menu
5. **Ver relatórios**: Opção 3 no menu

🎉 **Sistema pronto para uso!** 🌾

### ⚙️ Opções de Instalação Rápida Originais

#### Opção 1: Script Automático
```bash
cd cana-colheita-system
scripts/setup.sh
```

#### Opção 2: Makefile
```bash
cd cana-colheita-system
make setup
```

#### Opção 3: Manual Básico
```bash
cd cana-colheita-system

# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar ambiente
cp .env.example .env

# 4. Iniciar banco PostgreSQL
docker-compose -f docker-compose-postgres.yml up -d
docker-compose up -d
```

## 🎯 Execução

### 1. Iniciar o Banco de Dados
```bash
# Iniciar Oracle Database
docker-compose up -d

# Verificar se está rodando
docker-compose ps
```

### 2. Ativar Ambiente Python
```bash
source venv/bin/activate
```

### 3. Testar Conexão (Opcional)
```bash
python main.py --test-connection
```

### 4. Executar o Sistema
```bash
python main.py
```

### Comandos Úteis com Makefile
```bash
make start    # Iniciar banco
make test     # Testar conexão
make run      # Executar sistema
make logs     # Ver logs do banco
make stop     # Parar serviços
make status   # Status dos serviços
```

### Método 2: Instalação Manual

```bash
# 1. Clone e entre no diretório
git clone <url-do-repositorio>
cd cana-colheita-system

# 2. Crie ambiente virtual Python
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instale dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure ambiente
cp .env.example .env

# 5. Inicie Oracle via Docker
docker-compose up -d

# 6. Execute o sistema
python main.py
```

## ⚙️ Configuração

### Configuração do Banco Oracle

O sistema usa as seguintes configurações padrão:

```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XE
ORACLE_USERNAME=cana_user
ORACLE_PASSWORD=CanaPassword123
```

### Personalização de Parâmetros

Edite o arquivo `.env` para personalizar:

```env
# Diretório de dados
DATA_DIR=data

# Nível de logging
LOG_LEVEL=INFO

# Parâmetros de cálculo (opcional)
FATOR_BASE_MANUAL=0.05
FATOR_BASE_MECANIZADA=0.08
```

## 🖥️ Uso

### Inicialização

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar sistema
python main.py

# Testar apenas conexão
python main.py --test-connection
```

### Menu Principal

O sistema oferece as seguintes opções:

1. **📝 Cadastrar nova produção** - Inserir dados de produção de cana
2. **🧮 Calcular perdas** - Calcular perdas baseado em dados existentes
3. **📊 Gerar relatórios** - Relatórios consolidados de perdas
4. **💾 Gerenciar arquivos JSON** - Manipular arquivos de backup
5. **🔍 Consultar banco de dados** - Consultas diretas ao banco
6. **⚙️ Testar conexão banco** - Verificar conectividade
7. **🌍 Calcular com coordenadas GPS (TUPLA)** - Demonstra uso de tuplas com geolocalização
8. **📈 Analisar múltiplas medições (LISTA)** - Demonstra uso de listas com séries temporais
9. **🗃️ Relatório tabela de memória (DATAFRAME)** - Demonstra uso de DataFrames para análise
10. **📋 Estatísticas do histórico (DICIONÁRIO)** - Demonstra uso de dicionários para cache
**h. ❓ Ajuda - Como funciona o sistema** - Documentação interativa completa

### 📋 Detalhamento Completo das Opções

#### 1️⃣ **Cadastrar Nova Produção**
Permite registrar dados de uma nova colheita de cana-de-açúcar no sistema.

**Campos Obrigatórios:**
- **Localização**: Identificação específica da área (ex: "Fazenda São José - Talhão 3")
- **Área plantada (ha)**: Área em hectares da plantação colhida
- **Quantidade colhida (t)**: Total de toneladas de cana colhidas
- **Tipo de colheita**: Manual (mais precisa, menos perda) ou Mecanizada (mais rápida, mais perda)
- **Data da colheita**: Data em formato DD/MM/AAAA

**Campos Opcionais (melhoram precisão do cálculo):**
- **Variedade da cana**: Tipo genético (ex: RB92579, RB966928)
- **Idade da cana (meses)**: Tempo desde plantio (ideal: 12-18 meses)
- **Umidade do solo (%)**: Percentual de umidade (ideal: 60-70%)
- **Temperatura média (°C)**: Temperatura durante colheita (ideal: 25-30°C)
- **Precipitação (mm)**: Chuva dos últimos 30 dias (ideal: 80-125mm)
- **Coordenadas GPS**: Latitude, longitude e altitude para geolocalização

#### 2️⃣ **Calcular Perdas**
Calcula estimativa de perdas baseado em diferentes fontes de dados.

**Modos de Operação:**
- **🚀 Modo Automático**: Busca dados do banco + valores padrão inteligentes
- **📝 Modo Manual**: Usuário informa todos os dados manualmente
- **📂 Arquivo JSON**: Carrega dados de arquivo previamente salvo

**Tipos de Cálculo:**
- **Básico**: Usa apenas tipo de colheita (Manual: 5%, Mecanizada: 8%)
- **Avançado**: Considera fatores ambientais e condições da plantação

#### 3️⃣ **Gerar Relatórios**
Produz análises estatísticas consolidadas das perdas calculadas.

**Opções de Filtro:**
- **Todos os dados**: Análise completa do histórico
- **Últimos 30 dias**: Dados recentes
- **Período personalizado**: Define intervalo específico

**Conteúdo dos Relatórios:**
- Total colhido e perdas em toneladas
- Percentual médio de perdas
- Comparação por tipo de colheita
- Detalhes por produção individual

#### 4️⃣ **Gerenciar Arquivos JSON**
Administra arquivos de backup e dados salvos em formato JSON.

**Funcionalidades:**
- Listar arquivos disponíveis na pasta `data/`
- Visualizar conteúdo de arquivos específicos
- Excluir arquivos desnecessários
- Importar dados de arquivos para cálculos

#### 5️⃣ **Consultar Banco de Dados**
Acesso direto aos dados armazenados no banco Oracle/PostgreSQL.

**Tipos de Consulta:**
- **Listar produções**: Visualiza todas as produções cadastradas
- **Buscar por ID**: Localiza produção específica
- **Ver parâmetros**: Mostra fatores de cálculo configurados

#### 6️⃣ **Testar Conexão Banco**
Verifica se a comunicação com o banco de dados está funcionando.

**Verificações:**
- Conectividade de rede
- Autenticação de usuário
- Acesso às tabelas necessárias
- Status do container Docker

#### 7️⃣ **Calcular com Coordenadas GPS (TUPLA)**
**Tipo de Dado Demonstrado: TUPLA**

Utiliza coordenadas GPS armazenadas em tuplas para cálculos com geolocalização.

**Funcionalidade:**
- Coleta coordenadas GPS (latitude, longitude, altitude)
- Armazena em tupla imutável: `(-20.4521, -49.3874, 540)`
- Calcula perdas considerando localização geográfica
- Demonstra uso prático de tuplas em Python

#### 8️⃣ **Analisar Múltiplas Medições (LISTA)**
**Tipo de Dado Demonstrado: LISTA**

Processa séries temporais de medições usando listas Python.

**Funcionalidade:**
- Coleta múltiplas medições (umidade, temperatura, etc.)
- Armazena em listas: `[65.2, 67.1, 68.5, 66.8]`
- Calcula médias, máximos e mínimos
- Identifica tendências e padrões
- Demonstra manipulação de listas

#### 9️⃣ **Relatório Tabela de Memória (DATAFRAME)**
**Tipo de Dado Demonstrado: TABELA DE MEMÓRIA (DataFrame)**

Utiliza pandas DataFrame para análises estatísticas avançadas.

**Funcionalidade:**
- Carrega dados em DataFrame pandas
- Realiza agrupamentos e agregações
- Calcula estatísticas descritivas
- Gera tabelas formatadas
- Exporta para diferentes formatos
- Demonstra análise de dados estruturados

#### 🔟 **Estatísticas do Histórico (DICIONÁRIO)**
**Tipo de Dado Demonstrado: DICIONÁRIO**

Usa dicionários para cache de estatísticas e configurações.

**Funcionalidade:**
- Armazena configurações em dicionários
- Cache de estatísticas calculadas: `{"media": 8.5, "maximo": 12.3}`
- Metadados de processamento
- Parâmetros de sistema
- Demonstra uso eficiente de dicionários

#### ❓ **Ajuda - Como Funciona o Sistema**
Sistema de documentação interativa completa.

**Conteúdo da Ajuda:**
- 🎯 **Objetivo**: Propósito do sistema
- 🧮 **Cálculos**: Como funcionam os métodos básico e avançado
- 📋 **Campos**: Explicação detalhada de todos os campos
- 📊 **Tipos de Dados**: Demonstração dos 4 tipos obrigatórios
- 🚀 **Recursos**: Funcionalidades disponíveis
- 💡 **Exemplos**: Casos de uso práticos
- 🔧 **Valores Padrão**: Configurações automáticas
- 📈 **Interpretação**: Como entender os resultados

### 📋 Glossário Completo de Campos e Valores

#### **Campos de Produção**

**🔹 Localização**
- **Definição**: Identificação específica da área de cultivo
- **Formato**: "Fazenda/Usina - Setor - Talhão/Quadra"
- **Exemplo**: `"Usina Santa Rita - Setor B - Quadra 15"`
- **Importância**: Permite rastreabilidade e análise geográfica

**🔹 Área Plantada (hectares)**
- **Definição**: Extensão territorial da plantação colhida
- **Unidade**: Hectares (ha)
- **Faixa Típica**: 10-500 ha (pequenos a grandes produtores)
- **Exemplo**: `85.5` (85,5 hectares)

**🔹 Quantidade Colhida (toneladas)**
- **Definição**: Total de cana-de-açúcar efetivamente colhida
- **Unidade**: Toneladas (t)
- **Cálculo Produtividade**: Quantidade ÷ Área = t/ha
- **Exemplo**: `7695` (7.695 toneladas)

**🔹 Tipo de Colheita**
- **Manual**: 
  - Corte feito por trabalhadores com facões
  - Maior precisão, menor perda (2-6%)
  - Permite seleção de canas maduras
  - Mais lento e custoso
- **Mecanizada**: 
  - Corte feito por máquinas colheitadeiras
  - Maior velocidade, maior perda (5-12%)
  - Pode incluir impurezas (terra, folhas)
  - Menor custo operacional

**🔹 Data da Colheita**
- **Formato**: DD/MM/AAAA
- **Importância**: Relaciona com condições climáticas
- **Sazonalidade**: Safra principal (maio-novembro)
- **Exemplo**: `15/10/2024`

#### **Campos Ambientais e de Cultivo**

**🔹 Variedade da Cana**
- **Definição**: Cultivar genético específico da cana-de-açúcar
- **Exemplos Brasileiros**:
  - `RB92579`: Variedade comum, boa produtividade
  - `RB966928`: Resistente à seca
  - `SP80-1842`: Alta concentração de açúcar
  - `CTC4`: Variedade mais recente
- **Impacto**: Diferentes variedades têm diferentes resistências

**🔹 Idade da Cana (meses)**
- **Definição**: Tempo desde o plantio até a colheita
- **Faixas de Corte**:
  - `10-12 meses`: Precoce (menor rendimento)
  - `12-18 meses`: **Ideal** (melhor produtividade)
  - `18-24 meses`: Tardia (fibra mais dura)
- **Impacto nas Perdas**: Cana muito nova ou velha aumenta perdas

**🔹 Umidade do Solo (%)**
- **Definição**: Percentual de água presente no solo
- **Medição**: Sensor de umidade ou laboratório
- **Faixas**:
  - `<50%`: **Seco** (aumenta quebra dos colmos)
  - `60-70%`: **Ideal** (facilita corte e transporte)
  - `>80%`: **Encharcado** (dificulta entrada de máquinas)
- **Exemplo**: `68%`

**🔹 Temperatura Média (°C)**
- **Definição**: Temperatura média durante período de colheita
- **Medição**: Estação meteorológica ou dados históricos
- **Faixas**:
  - `<20°C`: Frio (retarda crescimento)
  - `25-30°C`: **Ideal** (melhor desenvolvimento)
  - `>35°C`: Calor excessivo (estresse da planta)
- **Exemplo**: `28.5°C`

**🔹 Precipitação (mm)**
- **Definição**: Chuva acumulada nos últimos 30 dias
- **Medição**: Pluviômetro ou dados meteorológicos
- **Faixas**:
  - `<50mm`: Seca (solo ressecado)
  - `80-125mm`: **Ideal** (umidade adequada)
  - `>200mm`: Excesso (solo encharcado)
- **Exemplo**: `75mm`

#### **Campos de Geolocalização**

**🔹 Coordenadas GPS**
- **Latitude**: Posição norte-sul (-90° a +90°)
  - Negativo: Hemisfério Sul (Brasil)
  - Exemplo: `-20.4521` (20,4521°S)
- **Longitude**: Posição leste-oeste (-180° a +180°)
  - Negativo: Oeste de Greenwich (Brasil)
  - Exemplo: `-49.3874` (49,3874°W)
- **Altitude**: Altura em relação ao nível do mar
  - Unidade: metros (m)
  - Exemplo: `540m`

#### **Valores de Resultado**

**🔹 Perda Estimada (toneladas)**
- **Definição**: Quantidade de cana perdida durante colheita
- **Cálculo**: Qtd_Colhida × Percentual_Perda ÷ (1 - Percentual_Perda)
- **Exemplo**: `615.6t` de perda em `7695t` colhidas

**🔹 Percentual de Perda (%)**
- **Definição**: Proporção de perda em relação ao total potencial
- **Interpretação**:
  - `<5%`: Excelente eficiência
  - `5-10%`: Boa eficiência (padrão da indústria)
  - `10-15%`: Eficiência regular (investigar)
  - `>15%`: Problemas graves (ação imediata)

**🔹 Produção Potencial (toneladas)**
- **Definição**: Quantidade que seria colhida sem perdas
- **Cálculo**: Qtd_Colhida ÷ (1 - Percentual_Perda)
- **Uso**: Indica potencial de melhoria

**🔹 Eficiência da Colheita (%)**
- **Definição**: Percentual de aproveitamento da produção
- **Cálculo**: (1 - Percentual_Perda) × 100
- **Meta**: >90% para operações eficientes

**🔹 Produtividade (t/ha)**
- **Definição**: Toneladas de cana por hectare
- **Cálculo**: Qtd_Colhida ÷ Área_Plantada
- **Benchmarks Brasileiros**:
  - `50-70 t/ha`: Baixa produtividade
  - `70-90 t/ha`: Produtividade média
  - `90-120 t/ha`: Alta produtividade
  - `>120 t/ha`: Excepcional

#### **Fatores de Cálculo Interno**

**🔹 Fator Base**
- **Manual**: 0.050 (5% base)
- **Mecanizada**: 0.080 (8% base)

**🔹 Fator Umidade**
- Ajuste baseado na umidade do solo
- Valores extremos aumentam o fator

**🔹 Fator Idade**
- Ajuste baseado na idade da cana
- Idades fora do ideal aumentam perdas

**🔹 Fator Clima**
- Ajuste baseado em temperatura e precipitação
- Condições adversas aumentam perdas

#### **Valores Padrão Inteligentes**

Quando campos opcionais não são fornecidos, o sistema aplica automaticamente:

```
idade_cana_meses: 14        # Idade típica para colheita no Brasil
umidade_solo: 65.0          # Umidade ideal para cana-de-açúcar  
temperatura_media: 26.5     # Temperatura média nas regiões produtoras
precipitacao_mm: 100.0      # Precipitação mensal típica (~1200mm anuais)
variedade_cana: 'RB92579'   # Variedade mais comum no Brasil
```

Estes valores são baseados em:
- 📊 **Dados do IBGE** sobre produção brasileira
- 🔬 **Estudos da EMBRAPA** sobre condições ideais
- 🏭 **Práticas do setor sucroenergético**
- 🌾 **Experiência de campo** de produtores

### Fluxo Típico de Uso

1. **Cadastrar Produção**:
   - Informar localização, área plantada, quantidade colhida
   - Escolher tipo de colheita (manual/mecanizada)
   - Adicionar dados ambientais (opcional)

2. **Calcular Perdas**:
   - Escolher fonte dos dados (novo, banco, JSON)
   - Selecionar tipo de cálculo (básico/avançado)
   - Visualizar resultados detalhados

3. **Analisar Relatórios**:
   - Filtrar por período
   - Ver estatísticas consolidadas
   - Comparar tipos de colheita

## 📁 Estrutura do Projeto

```
cana-colheita-system/
├── 📄 main.py                 # Script principal
├── 📄 requirements.txt        # Dependências Python
├── 📄 docker-compose.yml      # Configuração Docker
├── 📄 setup.sh               # Script de instalação
├── 📄 .env.example           # Exemplo de configuração
├── 📄 README.md              # Esta documentação
│
├── 📁 src/                   # Código fonte
│   ├── 📄 database.py        # Módulo banco Oracle
│   └── 📄 functions.py       # Funções de cálculo
│
├── 📁 docker/                # Configurações Docker
│   ├── 📄 init-db.sql        # Script inicialização BD
│   └── 📁 init-scripts/      # Scripts de setup
│
└── 📁 data/                  # Dados e exemplos
    ├── 📄 exemplo_producao_manual.json
    ├── 📄 exemplo_producao_mecanizada.json
    └── 📄 exemplo_relatorio_perdas.json
```

## 🧮 Tipos de Cálculo

### Cálculo Básico

Considera apenas o tipo de colheita:

- **Manual**: 5% de perda base
- **Mecanizada**: 8% de perda base

```python
# Exemplo de uso
calculadora = CalculadoraPerdas()
resultado = calculadora.calcular_perda_basica(
    qtd_colhida=1000.0,
    tipo_colheita="mecanizada"
)
# Resultado: ~80 toneladas de perda (8%)
```

### Cálculo Avançado

Considera fatores ambientais e de produção:

#### Fatores de Ajuste

1. **Umidade do Solo**:
   - Ideal: 60-70%
   - Fora da faixa: aumenta perdas

2. **Idade da Cana**:
   - Ideal: 12-18 meses
   - Muito nova/velha: mais perdas

3. **Condições Climáticas**:
   - Temperatura ideal: 25-30°C
   - Precipitação adequada: 80-125mm/mês

#### Fórmula de Cálculo

```
Perda Total = Qtd_Colhida × (Fator_Base + Fator_Umidade + Fator_Idade + Fator_Clima)
```

### Exemplos de Cenários

| Cenário | Tipo | Condições | Perda Estimada |
|---------|------|-----------|----------------|
| Ideal | Manual | Todas ideais | 5.0% |
| Problema | Manual | Solo seco, cana velha | 7.5% |
| Ideal | Mecanizada | Todas ideais | 8.0% |
| Problema | Mecanizada | Solo úmido, cana nova | 11.2% |

## 🗄️ API do Banco de Dados

### Principais Tabelas

#### `producao_cana`
```sql
- id (NUMBER) - PK autoincrement
- localizacao (VARCHAR2(100)) - Local da produção
- area_plantada_ha (NUMBER(10,2)) - Área em hectares
- qtd_colhida_toneladas (NUMBER(12,2)) - Quantidade colhida
- tipo_colheita (VARCHAR2(20)) - 'manual' ou 'mecanizada'
- data_colheita (DATE) - Data da colheita
- variedade_cana (VARCHAR2(50)) - Variedade da cana
- idade_cana_meses (NUMBER(3)) - Idade em meses
- umidade_solo (NUMBER(5,2)) - Umidade do solo (%)
- temperatura_media (NUMBER(4,1)) - Temperatura média (°C)
- precipitacao_mm (NUMBER(6,2)) - Precipitação (mm)
```

#### `perdas_colheita`
```sql
- id (NUMBER) - PK autoincrement
- producao_id (NUMBER) - FK para producao_cana
- perda_estimada_toneladas (NUMBER(10,2)) - Perda calculada
- percentual_perda (NUMBER(5,2)) - Percentual de perda
- fatores_perda (CLOB) - JSON com fatores aplicados
- metodo_calculo (VARCHAR2(50)) - Método usado
- observacoes (VARCHAR2(500)) - Observações adicionais
```

#### `parametros_perdas`
```sql
- id (NUMBER) - PK autoincrement
- tipo_colheita (VARCHAR2(20)) - Tipo de colheita
- fator_base_perda (NUMBER(4,3)) - Fator base de perda
- fator_umidade (NUMBER(4,3)) - Fator de umidade
- fator_idade (NUMBER(4,3)) - Fator de idade
- fator_clima (NUMBER(4,3)) - Fator climático
```

### Views Disponíveis

#### `vw_relatorio_perdas`
View consolidada com dados de produção e perdas calculadas.

## 💡 Exemplos

### Exemplo 1: Cálculo Manual Simples

```bash
# No menu principal, escolha:
1. Cadastrar nova produção

# Informe:
Localização: Fazenda Teste
Área plantada: 50
Quantidade colhida: 3500
Tipo: Manual (1)

# Depois escolha:
2. Calcular perdas
1. Informar dados agora (usar dados recém cadastrados)
1. Básico

# Resultado esperado: ~175 toneladas (5% de perda)
```

### Exemplo 2: Cálculo Avançado com Fatores

```bash
# Cadastre produção com dados completos:
Localização: Fazenda Avançada
Área: 100 ha
Quantidade: 8000 t
Tipo: Mecanizada
Idade da cana: 20 meses
Umidade do solo: 80%
Temperatura: 32°C
Precipitação: 150mm

# Execute cálculo avançado
# Resultado esperado: >8% devido aos fatores adversos
```

### Exemplo 3: Importar JSON

```bash
# Use arquivo exemplo fornecido
2. Calcular perdas
3. Carregar arquivo JSON
1. exemplo_producao_mecanizada.json
2. Avançado

# Visualize resultado detalhado com fatores aplicados
```

## 🔧 Troubleshooting

### Problemas Comuns

#### 1. Erro de Conexão Oracle

**Sintoma**: "Falha na conexão com banco Oracle"

**Soluções**:
```bash
# Verificar se Docker está rodando
docker ps

# Verificar logs do Oracle
docker-compose logs oracle-db

# Reiniciar serviços
docker-compose down
docker-compose up -d

# Aguardar inicialização completa (3-5 minutos)
```

#### 2. Erro cx_Oracle

**Sintoma**: "ModuleNotFoundError: No module named 'cx_Oracle'"

**Solução**:
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Reinstalar dependências
pip install --upgrade cx_Oracle
```

#### 3. Problema com Instant Client (macOS)

**Sintoma**: Erro ao inicializar cx_Oracle

**Solução**:
```bash
# Instalar Oracle Instant Client
# Baixar de: https://www.oracle.com/database/technologies/instant-client/downloads.html
# Descompactar em /opt/oracle/instantclient_21_8
# Configurar biblioteca:
export DYLD_LIBRARY_PATH=/opt/oracle/instantclient_21_8:$DYLD_LIBRARY_PATH
```

#### 4. Porta 1521 em Uso

**Sintoma**: "Port 1521 is already in use"

**Solução**:
```bash
# Verificar processo usando a porta
lsof -i :1521

# Parar Oracle local se existir
sudo systemctl stop oracle

# Ou modificar porta no docker-compose.yml
```

### Verificações de Saúde

```bash
# 1. Testar conexão Python-Oracle
python main.py --test-connection

# 2. Verificar status Docker
docker-compose ps

# 3. Verificar logs detalhados
docker-compose logs -f oracle-db

# 4. Testar conexão SQL direta
sqlplus cana_user/CanaPassword123@localhost:1521/XE
```

### Logs e Debug

```bash
# Habilitar logs detalhados
export LOG_LEVEL=DEBUG
python main.py

# Verificar arquivos de log
ls -la data/

# Ver logs do Docker
docker-compose logs --tail=50 oracle-db
```

## 🐳 Comandos Docker Úteis

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs
docker-compose logs -f oracle-db

# Executar SQL no container
docker exec -it cana-oracle-db sqlplus cana_user/CanaPassword123@XE

# Limpar volumes (CUIDADO: apaga dados)
docker-compose down -v

# Rebuildar imagens
docker-compose build --no-cache
```

## 📊 Interpretação de Resultados

### Métricas Principais

- **Perda Estimada**: Quantidade de cana perdida durante colheita
- **Percentual de Perda**: Porcentagem em relação ao total colhido
- **Produção Potencial**: Quantidade que seria colhida sem perdas
- **Eficiência da Colheita**: Percentual de aproveitamento
- **Produtividade**: Toneladas por hectare

### Benchmarks da Indústria

| Tipo de Colheita | Perda Aceitável | Perda Preocupante | Excelente |
|-------------------|----------------|-------------------|-----------|
| Manual | 3-7% | >10% | <3% |
| Mecanizada | 6-12% | >15% | <6% |

### Fatores de Melhoria

1. **Treinamento**: Capacitação de operadores
2. **Manutenção**: Equipamentos bem calibrados
3. **Timing**: Colheita no ponto ideal de maturação
4. **Condições**: Evitar períodos de chuva excessiva

## 🗃 Histórico de lançamentos

* 1.0.0 - 15/10/2024
    * 🚀 Lançamento inicial do sistema
    * ✅ Implementação completa dos 4 tipos de dados obrigatórios (Lista, Tupla, Dicionário, DataFrame)
    * ✅ Cálculo básico e avançado de perdas na colheita
    * ✅ Integração com Oracle Database e PostgreSQL via Docker
    * ✅ Interface CLI interativa com menus coloridos
    * ✅ Sistema de backup automático em JSON
    * ✅ Relatórios consolidados com estatísticas
    * ✅ Documentação interativa completa
    * ✅ Valores padrão inteligentes baseados em condições brasileiras
    * ✅ Sistema de validação robusta de dados
    * ✅ Logging detalhado para troubleshooting

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Juliagutierres29/cana-colheita-system">SISTEMA DE CÁLCULO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP - Grupo Cana Colheita System</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>