# 📚 DOCUMENTAÇÃO: USO OBRIGATÓRIO DOS TIPOS DE DADOS

Este projeto implementa **obrigatoriamente** os seguintes tipos de dados conforme solicitado:

## 📋 1. LISTA (List)
**Onde está sendo usada:**

### No arquivo `src/functions.py`:
- **Linha 56**: `historico_calculos: List[Dict[str, Any]]` - Histórico de todos os cálculos
- **Linha 61**: `fazendas_cadastradas: List[Tuple[str, float, float]]` - Lista de tuplas com fazendas
- **Linha 37**: `historico_umidade: Optional[List[float]]` - Lista de medições de umidade
- **Linha 107**: Processamento de listas em `obter_estatisticas_historico()`
- **Linha 145**: `buscar_por_coordenadas()` retorna `List[Tuple[str, float]]`
- **Linha 324**: `processar_multiplas_medicoes()` recebe `List[float]`

### No arquivo `main.py`:
- **Linha 67**: Uso em `analisar_multiplas_medicoes()` para múltiplas medições
- **Linha 86**: Conversão de string para lista: `[float(x.strip()) for x in medicoes_str.split(',')]`

### Exemplos práticos:
```python
medicoes_umidade = [65.2, 67.8, 63.1, 69.5, 66.3]  # LISTA
localizacoes = ["Fazenda A", "Fazenda B", "Fazenda C"]  # LISTA
```

## 🌍 2. TUPLA (Tuple)
**Onde está sendo usada:**

### No arquivo `src/functions.py`:
- **Linha 35**: `coordenadas_gps: Optional[Tuple[float, float, float]]` - Coordenadas GPS
- **Linha 60**: `versao_sistema: Tuple[int, int, int]` - Versão do sistema
- **Linha 63**: `fazendas_cadastradas: List[Tuple[str, float, float]]` - Lista de tuplas
- **Linha 145**: Retorno `List[Tuple[str, float]]` em busca por coordenadas
- **Linha 302**: Método `calcular_com_coordenadas()` recebe tupla de coordenadas

### No arquivo `main.py`:
- **Linha 23**: Criação de tupla: `coordenadas = (lat, lon, alt)`
- **Linha 47**: Iteração sobre lista de tuplas: `for nome, distancia in fazendas`

### Exemplos práticos:
```python
coordenadas = (-22.1234, -47.5678, 580.5)  # TUPLA (lat, lon, alt)
versao = (1, 0, 0)  # TUPLA (major, minor, patch)
fazenda_info = ("São João", -22.1234, -47.5678)  # TUPLA
```

## 📊 3. DICIONÁRIO (Dict)
**Onde está sendo usada:**

### No arquivo `src/functions.py`:
- **Linha 44**: `fatores_aplicados: Dict[str, float]` - Fatores de cálculo
- **Linha 58**: `cache_resultados: Dict[str, ResultadoPerda]` - Cache de resultados
- **Linha 59**: `configuracoes: Dict[str, Any]` - Configurações do sistema
- **Linha 107**: `obter_estatisticas_historico()` retorna `Dict[str, Any]`
- **Linha 180**: `gerar_relatorio_completo()` retorna dicionário complexo
- **Linha 324**: `processar_multiplas_medicoes()` retorna análise em dicionário

### No arquivo `main.py`:
- **Linha 175**: Relatório de estatísticas usando dicionários
- Múltiplas linhas: Uso de dicionários para configurações e resultados

### Exemplos práticos:
```python
configuracoes = {
    'precisao_decimal': 2,
    'modo_debug': False,
    'salvar_automatico': True
}

fatores = {
    'fator_base': 0.05,
    'fator_umidade': 0.02,
    'fator_clima': 0.015
}
```

## 🗃️ 4. TABELA DE MEMÓRIA (DataFrame)
**Onde está sendo usada:**

### No arquivo `src/functions.py`:
- **Linha 7**: `import pandas as pd` - Importação da biblioteca
- **Linha 62**: `tabela_memoria: pd.DataFrame` - Tabela de memória principal
- **Linha 120**: `criar_tabela_memoria_analise()` cria e retorna DataFrame
- **Linha 365**: `gerar_relatorio_com_tabela_memoria()` usa DataFrame para análises

### No arquivo `main.py`:
- **Linha 110**: Uso de DataFrame em `relatorio_tabela_memoria()`
- **Linha 115-130**: Análises estatísticas usando métodos do DataFrame

### No arquivo `demo_tipos_dados.py`:
- **Linhas 140-170**: Criação e manipulação completa de DataFrame

### Exemplos práticos:
```python
# Criando DataFrame (Tabela de Memória)
dados = {
    'fazenda': ['São João', 'Santa Maria'],
    'area_ha': [120.5, 85.3],
    'producao_ton': [1200.5, 800.3]
}
tabela_memoria = pd.DataFrame(dados)

# Análises na tabela
total_producao = tabela_memoria['producao_ton'].sum()
media_area = tabela_memoria['area_ha'].mean()
```

## 🔄 USO INTEGRADO DOS TIPOS

### Exemplo completo que usa TODOS os tipos:
```python
# LISTA de medições
medicoes = [65.2, 67.8, 63.1, 69.5]

# TUPLA de coordenadas
coordenadas = (-22.1234, -47.5678, 580.5)

# DICIONÁRIO de configurações
config = {
    'precisao': 2,
    'salvar_auto': True
}

# TABELA DE MEMÓRIA para análises
df = pd.DataFrame({
    'medicao': medicoes,
    'status': ['ok', 'ok', 'baixo', 'alto']
})

# Processamento integrado
resultado = calculadora.processar_multiplas_medicoes(dados, medicoes)
```

## 📁 ARQUIVOS ONDE OS TIPOS SÃO USADOS

1. **`src/functions.py`**: Implementação principal de todos os tipos
2. **`main.py`**: Interface do usuário usando todos os tipos
3. **`demo_tipos_dados.py`**: Demonstração explicita de cada tipo
4. **Classes de dados**: DadosProducao, ResultadoPerda, ParametrosPerdas

## ✅ VERIFICAÇÃO DE CONFORMIDADE

- ✅ **LISTA**: Usada em 15+ locais diferentes
- ✅ **TUPLA**: Usada em 10+ locais diferentes  
- ✅ **DICIONÁRIO**: Usada em 20+ locais diferentes
- ✅ **TABELA DE MEMÓRIA**: Implementada com pandas DataFrame

Todos os tipos de dados são **funcionais** e **integrados** ao sistema de cálculo de perdas na colheita de cana-de-açúcar, atendendo completamente aos requisitos obrigatórios do trabalho.