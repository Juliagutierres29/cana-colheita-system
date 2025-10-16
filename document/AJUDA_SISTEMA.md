# 📖 SISTEMA DE AJUDA

## Como Acessar a Ajuda

No menu principal do sistema, digite:
- `h` ou `H` para acessar a ajuda completa
- `?` também funciona como atalho para ajuda

## O que a Ajuda Inclui

### 🎯 Objetivo do Sistema
Explicação clara sobre o propósito do sistema de cálculo de perdas na colheita de cana-de-açúcar.

### 🧮 Como Funciona o Cálculo
Detalhamento dos dois métodos de cálculo:

**Método Básico:**
- Colheita Manual: 2-4% de perda
- Colheita Mecanizada: 3-6% de perda

**Método Avançado:**
- Considera fatores ambientais
- Ajusta baseado em idade, umidade, temperatura, precipitação e variedade

### 📋 Campos do Sistema

**Campos Obrigatórios:**
- Localização
- Área plantada (ha)
- Quantidade colhida (t)
- Tipo de colheita
- Data da colheita

**Campos Opcionais:**
- Idade da cana (meses)
- Umidade do solo (%)
- Temperatura média (°C)
- Precipitação (mm)
- Variedade da cana
- Coordenadas GPS

### 📊 Tipos de Dados Demonstrados

1. **LISTAS:** Histórico de medições, múltiplas temperaturas
2. **TUPLAS:** Coordenadas GPS (latitude, longitude)
3. **DICIONÁRIOS:** Cache de configurações, estatísticas
4. **DATAFRAMES:** Análise estatística, relatórios

### 🚀 Recursos do Sistema
- Modo automático com banco de dados
- Valores padrão inteligentes
- Suporte PostgreSQL e Oracle
- Persistência em JSON e banco
- Relatórios detalhados

### 💡 Exemplos de Uso
Orientações práticas sobre como usar cada funcionalidade do sistema.

### 🔧 Valores Padrão
Lista dos valores padrão aplicados automaticamente baseados em condições típicas brasileiras.

### 📈 Interpretação dos Resultados
Guia para entender os resultados:
- Perda baixa (< 3%): Condições ideais
- Perda média (3-5%): Condições normais  
- Perda alta (> 5%): Condições adversas

## Demonstração da Ajuda

Para ver a ajuda em ação sem precisar navegar pelo menu:

```bash
python demo_ajuda.py
```

Este script demonstra toda a funcionalidade de ajuda de forma independente.

## Interface Amigável

A ajuda é apresentada com:
- ✅ Formatação clara e organizada
- 🎯 Emojis para facilitar navegação visual
- 📖 Pausa para leitura confortável
- 🔄 Retorno automático ao menu principal