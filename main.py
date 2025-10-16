#!/usr/bin/env python3
"""
Script principal do Sistema de Cálculo de Perdas na Colheita de Cana-de-Açúcar.

Este script fornece uma interface de linha de comando para:
- Cadastrar dados de produção de cana
- Calcular perdas na colheita
- Gerar relatórios
- Gerenciar dados via banco Oracle (prioridade) ou PostgreSQL
"""

import sys
import os
import logging
import argparse
from datetime import datetime, date
from typing import Dict, List, Optional
import colorlog
from tabulate import tabulate

# Adicionar o diretório src ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Tentar importar banco Oracle primeiro (prioridade), depois PostgreSQL
try:
    from src.database import OracleDatabase as Database
    DATABASE_TYPE = "Oracle"
except ImportError:
    try:
        from src.database_postgres import PostgreSQLDatabase as Database
        DATABASE_TYPE = "PostgreSQL"
    except ImportError:
        print("❌ Erro: Nenhum driver de banco disponível!")
        print("Instale cx_Oracle ou psycopg2-binary")
        sys.exit(1)

from src.functions import (
    CalculadoraPerdas, ManipuladorJSON, DadosProducao, 
    GerenciadorDados, validar_dados_producao
)


class SistemaCanaAcucar:
    """Classe principal do sistema de cálculo de perdas."""
    
    def __init__(self):
        """Inicializa o sistema."""
        self.configurar_logging()
        self.db = Database()
        self.calculadora = CalculadoraPerdas()
        self.manipulador_json = ManipuladorJSON()
        self.logger = logging.getLogger(__name__)
        
        # Informar qual banco está sendo usado
        self.logger.info(f"Usando banco de dados: {DATABASE_TYPE}")
    
    def configurar_logging(self):
        """Configura sistema de logging com cores."""
        # Configurar handler com cores
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s:%(reset)s %(message)s',
            datefmt=None,
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            secondary_log_colors={},
            style='%'
        ))
        
        # Configurar logger principal
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    
    def verificar_conexao_banco(self) -> bool:
        """Verifica se a conexão com o banco está funcionando."""
        self.logger.info(f"Verificando conexão com banco de dados {DATABASE_TYPE}...")
        
        try:
            if self.db.test_connection():
                self.logger.info(f"✅ Conexão com banco {DATABASE_TYPE} estabelecida com sucesso!")
                return True
            else:
                self.logger.error(f"❌ Falha na conexão com banco {DATABASE_TYPE}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Erro ao conectar com banco: {e}")
            if DATABASE_TYPE == "Oracle":
                self.logger.info("💡 Certifique-se de que o Docker está rodando: docker-compose up -d")
            else:
                self.logger.info("💡 Certifique-se de que o PostgreSQL está rodando: docker-compose -f docker-compose-postgres.yml up -d")
            return False
    
    def menu_principal(self):
        """Exibe menu principal e processa escolhas do usuário."""
        while True:
            print("\n" + "="*60)
            print("🌾 SISTEMA DE CÁLCULO DE PERDAS - CANA-DE-AÇÚCAR 🌾")
            print("="*60)
            print(f"💾 Banco de dados: {DATABASE_TYPE}")
            print("="*60)
            print("1. 📝 Cadastrar nova produção")
            print("2. 🧮 Calcular perdas")
            print("3. 📊 Gerar relatórios")
            print("4. 💾 Gerenciar arquivos JSON")
            print("5. 🔍 Consultar banco de dados")
            print("6. ⚙️  Testar conexão banco")
            print("7. 🌍 Calcular com coordenadas GPS (TUPLA)")
            print("8. 📈 Analisar múltiplas medições (LISTA)")
            print("9. 🗃️  Relatório tabela de memória (DATAFRAME)")
            print("10. 📋 Estatísticas do histórico (DICIONÁRIO)")
            print("h. ❓ Ajuda - Como funciona o sistema")
            print("0. 🚪 Sair")
            print("="*60)
            
            try:
                opcao = input("Escolha uma opção: ").strip()
                
                if opcao == "1":
                    self.cadastrar_producao()
                elif opcao == "2":
                    self.calcular_perdas()
                elif opcao == "3":
                    self.gerar_relatorios()
                elif opcao == "4":
                    self.gerenciar_json()
                elif opcao == "5":
                    self.consultar_banco()
                elif opcao == "6":
                    self.verificar_conexao_banco()
                elif opcao == "7":
                    self.calcular_com_gps()
                elif opcao == "8":
                    self.analisar_multiplas_medicoes()
                elif opcao == "9":
                    self.relatorio_tabela_memoria()
                elif opcao == "10":
                    self.estatisticas_historico()
                elif opcao.lower() == "h" or opcao == "?":
                    self.exibir_ajuda()
                elif opcao == "0":
                    print("👋 Obrigado por usar o sistema!")
                    break
                else:
                    print("❌ Opção inválida. Tente novamente.")
                    
            except KeyboardInterrupt:
                print("\n👋 Sistema encerrado pelo usuário.")
                break
            except Exception as e:
                self.logger.error(f"Erro inesperado: {e}")
    
    def exibir_ajuda(self):
        """Exibe ajuda detalhada sobre o sistema e cálculos."""
        print("\n" + "="*80)
        print("❓ AJUDA - SISTEMA DE CÁLCULO DE PERDAS NA COLHEITA DE CANA-DE-AÇÚCAR")
        print("="*80)
        
        print("\n🎯 OBJETIVO DO SISTEMA")
        print("-" * 50)
        print("Este sistema calcula perdas estimadas durante a colheita de cana-de-açúcar")
        print("baseado em fatores ambientais, tipo de colheita e características da produção.")
        
        print("\n🧮 COMO FUNCIONA O CÁLCULO")
        print("-" * 50)
        print("O sistema utiliza dois métodos de cálculo:")
        print()
        print("📊 MÉTODO BÁSICO:")
        print("   • Aplica fatores fixos baseados no tipo de colheita")
        print("   • Colheita Manual: 2-4% de perda")
        print("   • Colheita Mecanizada: 3-6% de perda")
        print()
        print("🔬 MÉTODO AVANÇADO (quando há dados completos):")
        print("   • Considera fatores ambientais e da plantação")
        print("   • Ajusta percentual baseado em:")
        print("     - Idade da cana (meses)")
        print("     - Umidade do solo (%)")
        print("     - Temperatura média (°C)")
        print("     - Precipitação (mm)")
        print("     - Variedade da cana")
        
        print("\n📋 CAMPOS DO SISTEMA")
        print("-" * 50)
        print("🔹 CAMPOS OBRIGATÓRIOS:")
        print("   • Localização: Identificação da área (ex: Fazenda X - Talhão 1)")
        print("   • Área plantada: Em hectares")
        print("   • Quantidade colhida: Em toneladas")
        print("   • Tipo de colheita: Manual ou Mecanizada")
        print("   • Data da colheita: Formato DD/MM/AAAA")
        print()
        print("🔹 CAMPOS OPCIONAIS (para cálculo avançado):")
        print("   • Idade da cana: Em meses (padrão: 14 meses)")
        print("   • Umidade do solo: Em % (padrão: 65%)")
        print("   • Temperatura média: Em °C (padrão: 26.5°C)")
        print("   • Precipitação: Em mm (padrão: 100mm)")
        print("   • Variedade da cana: Ex: RB92579 (padrão)")
        print("   • Coordenadas GPS: Latitude e longitude para geolocalização")
        
        print("\n📊 TIPOS DE DADOS UTILIZADOS")
        print("-" * 50)
        print("O sistema demonstra o uso de 4 tipos de dados obrigatórios:")
        print()
        print("📜 LISTAS:")
        print("   • Histórico de medições de umidade")
        print("   • Múltiplas temperaturas ao longo do dia")
        print("   • Série temporal de dados climáticos")
        print()
        print("📍 TUPLAS:")
        print("   • Coordenadas GPS (latitude, longitude)")
        print("   • Dados imutáveis de localização geográfica")
        print()
        print("🗂️  DICIONÁRIOS:")
        print("   • Cache de configurações do sistema")
        print("   • Estatísticas calculadas (média, máximo, mínimo)")
        print("   • Metadados de processamento")
        print()
        print("📊 TABELAS DE MEMÓRIA (DataFrames):")
        print("   • Análise estatística de múltiplas produções")
        print("   • Relatórios com agrupamentos e agregações")
        print("   • Exportação para diferentes formatos")
        
        print("\n🚀 RECURSOS DO SISTEMA")
        print("-" * 50)
        print("✅ Modo Automático: Busca dados do banco automaticamente")
        print("✅ Valores Padrão: Aplica condições típicas brasileiras")
        print("✅ Múltiplos Bancos: Suporte a PostgreSQL e Oracle")
        print("✅ Persistência: Salva em JSON e banco de dados")
        print("✅ Relatórios: Estatísticas e análises detalhadas")
        print("✅ Validação: Verifica dados antes dos cálculos")
        
        print("\n💡 EXEMPLOS DE USO")
        print("-" * 50)
        print("1️⃣  Para cálculo rápido: Use apenas campos obrigatórios")
        print("2️⃣  Para análise precisa: Forneça dados ambientais completos")
        print("3️⃣  Para geolocalização: Use a opção 7 com coordenadas GPS")
        print("4️⃣  Para análise histórica: Use as opções 8-10 para relatórios")
        
        print("\n🔧 VALORES PADRÃO INTELIGENTES")
        print("-" * 50)
        print("Quando campos opcionais não são fornecidos, o sistema aplica:")
        print("• Idade da cana: 14 meses (típica para colheita)")
        print("• Umidade do solo: 65% (ideal para cana-de-açúcar)")
        print("• Temperatura: 26.5°C (média brasileira)")
        print("• Precipitação: 100mm (mensal típica)")
        print("• Variedade: RB92579 (comum no Brasil)")
        
        print("\n📈 INTERPRETAÇÃO DOS RESULTADOS")
        print("-" * 50)
        print("🔸 Perda baixa (< 3%): Condições ideais de colheita")
        print("🔸 Perda média (3-5%): Condições normais")
        print("🔸 Perda alta (> 5%): Condições adversas - revisar processo")
        
        print("\n" + "="*80)
        input("📖 Pressione ENTER para voltar ao menu principal...")

    def cadastrar_producao(self):
        """Interface para cadastrar dados de produção."""
        print("\n📝 CADASTRAR NOVA PRODUÇÃO")
        print("-" * 40)
        
        try:
            # Coletar dados básicos
            localizacao = input("Localização (ex: Fazenda São José - Talhão 1): ").strip()
            if not localizacao:
                print("❌ Localização é obrigatória.")
                return
            
            area_ha = float(input("Área plantada (hectares): "))
            qtd_colhida = float(input("Quantidade colhida (toneladas): "))
            
            print("Tipo de colheita:")
            print("1. Manual")
            print("2. Mecanizada")
            tipo_opcao = input("Escolha (1 ou 2): ").strip()
            tipo_colheita = "manual" if tipo_opcao == "1" else "mecanizada"
            
            # Dados opcionais
            print("\n📋 Dados opcionais (pressione Enter para pular):")
            
            variedade = input("Variedade da cana: ").strip() or None
            
            idade_str = input("Idade da cana (meses): ").strip()
            idade_meses = int(idade_str) if idade_str else None
            
            umidade_str = input("Umidade do solo (%): ").strip()
            umidade_solo = float(umidade_str) if umidade_str else None
            
            temp_str = input("Temperatura média (°C): ").strip()
            temperatura = float(temp_str) if temp_str else None
            
            precip_str = input("Precipitação (mm): ").strip()
            precipitacao = float(precip_str) if precip_str else None
            
            # Criar objeto de dados
            dados = DadosProducao(
                localizacao=localizacao,
                area_plantada_ha=area_ha,
                qtd_colhida_toneladas=qtd_colhida,
                tipo_colheita=tipo_colheita,
                data_colheita=date.today(),
                variedade_cana=variedade,
                idade_cana_meses=idade_meses,
                umidade_solo=umidade_solo,
                temperatura_media=temperatura,
                precipitacao_mm=precipitacao
            )
            
            # Validar dados
            dados_dict = {
                'localizacao': dados.localizacao,
                'area_plantada_ha': dados.area_plantada_ha,
                'qtd_colhida_toneladas': dados.qtd_colhida_toneladas,
                'tipo_colheita': dados.tipo_colheita,
                'umidade_solo': dados.umidade_solo,
                'idade_cana_meses': dados.idade_cana_meses
            }
            
            erros = validar_dados_producao(dados_dict)
            if erros:
                print("❌ Erros encontrados:")
                for erro in erros:
                    print(f"  • {erro}")
                return
            
            # Salvar no banco se conexão disponível
            if self.verificar_conexao_banco():
                try:
                    dados_producao_dict = {
                        'localizacao': dados.localizacao,
                        'area_plantada_ha': dados.area_plantada_ha,
                        'qtd_colhida_toneladas': dados.qtd_colhida_toneladas,
                        'tipo_colheita': dados.tipo_colheita,
                        'data_colheita': dados.data_colheita,
                        'variedade_cana': dados.variedade_cana,
                        'idade_cana_meses': dados.idade_cana_meses,
                        'umidade_solo': dados.umidade_solo,
                        'temperatura_media': dados.temperatura_media,
                        'precipitacao_mm': dados.precipitacao_mm
                    }
                    
                    producao_id = self.db.inserir_producao_cana(dados_producao_dict)
                    print(f"✅ Produção cadastrada no banco com ID: {producao_id}")
                    
                except Exception as e:
                    self.logger.error(f"Erro ao salvar no banco: {e}")
                    print("⚠️  Erro ao salvar no banco, mas dados serão salvos em JSON")
            
            # Salvar em JSON como backup
            arquivo_json = self.manipulador_json.salvar_dados_producao(dados)
            print(f"💾 Dados também salvos em: {arquivo_json}")
            
        except ValueError as e:
            print(f"❌ Erro nos dados informados: {e}")
        except Exception as e:
            self.logger.error(f"Erro ao cadastrar produção: {e}")
            print("❌ Erro inesperado ao cadastrar produção.")
    
    def calcular_perdas(self):
        """Interface para calcular perdas."""
        print("\n🧮 CALCULAR PERDAS NA COLHEITA")
        print("-" * 40)
        
        print("Escolha a fonte dos dados:")
        print("1. 🚀 Modo automático (dados do banco + valores padrão)")
        print("2. 📝 Modo manual (informar todos os dados)")
        print("3. 📂 Carregar arquivo JSON")
        
        opcao = input("Escolha (1, 2 ou 3): ").strip()
        
        try:
            dados_producao = None
            
            if opcao == "1":
                dados_producao = self._modo_automatico()
            elif opcao == "2":
                dados_producao = self._modo_manual()
            elif opcao == "3":
                dados_producao = self._carregar_dados_json()
            else:
                print("❌ Opção inválida.")
                return
            
            if not dados_producao:
                print("❌ Não foi possível obter dados para cálculo.")
                return
            
            # Calcular automaticamente (sempre avançado quando temos dados suficientes)
            if self._tem_dados_para_calculo_avancado(dados_producao):
                print("\n🔬 Executando cálculo avançado (fatores ambientais incluídos)...")
                resultado = self.calculadora.calcular_perda_avancada(dados_producao)
            else:
                print("\n⚡ Executando cálculo básico (dados limitados)...")
                resultado = self.calculadora.calcular_perda_basica(
                    dados_producao.qtd_colhida_toneladas,
                    dados_producao.tipo_colheita
                )
            
            # Exibir resultados
            self._exibir_resultado_calculo(dados_producao, resultado)
            
            # Salvar resultados automaticamente
            print("\n💾 Salvando resultado automaticamente...")
            self._salvar_resultado_calculo(dados_producao, resultado)
            
        except Exception as e:
            self.logger.error(f"Erro ao calcular perdas: {e}")
            print("❌ Erro ao calcular perdas.")
    
    def _modo_automatico(self) -> Optional[DadosProducao]:
        """Modo automático: busca dados do banco e usa valores padrão."""
        print("\n🚀 MODO AUTOMÁTICO")
        print("-" * 30)
        
        if not self.verificar_conexao_banco():
            print("❌ Modo automático requer conexão com banco.")
            return None
        
        try:
            # Listar produções disponíveis
            producoes = self.db.listar_producoes(5)
            
            if not producoes:
                print("❌ Nenhuma produção encontrada no banco.")
                print("💡 Use o modo manual ou cadastre uma produção primeiro (opção 1 do menu).")
                return None
            
            print(f"\n📋 Últimas {len(producoes)} produções disponíveis:")
            headers = ["ID", "Localização", "Área (ha)", "Colhida (t)", "Tipo", "Data"]
            table_data = []
            
            for p in producoes:
                table_data.append([
                    p['id'],
                    p['localizacao'][:25] + "..." if len(p['localizacao']) > 25 else p['localizacao'],
                    p['area_plantada_ha'],
                    p['qtd_colhida_toneladas'],
                    p['tipo_colheita'],
                    p['data_colheita'].strftime('%d/%m/%Y') if hasattr(p['data_colheita'], 'strftime') else str(p['data_colheita'])
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Escolher produção (ou usar a mais recente)
            print(f"\nSelecione uma produção:")
            producao_id = input(f"ID da produção (Enter para usar a mais recente - ID {producoes[0]['id']}): ").strip()
            
            if not producao_id:
                producao_id = producoes[0]['id']
            else:
                producao_id = int(producao_id)
            
            # Buscar dados completos
            dados_dict = self.db.buscar_producao_por_id(producao_id)
            
            if not dados_dict:
                print("❌ Produção não encontrada.")
                return None
            
            print(f"\n✅ Carregando dados da produção ID {producao_id}")
            print(f"📍 Local: {dados_dict['localizacao']}")
            print(f"🌾 {dados_dict['qtd_colhida_toneladas']}t em {dados_dict['area_plantada_ha']}ha")
            
            # Completar dados que faltam com valores padrão inteligentes
            dados_completos = self._completar_com_valores_padrao(dados_dict)
            
            # Converter para DadosProducao
            return DadosProducao(
                localizacao=dados_completos['localizacao'],
                area_plantada_ha=float(dados_completos['area_plantada_ha']),
                qtd_colhida_toneladas=float(dados_completos['qtd_colhida_toneladas']),
                tipo_colheita=dados_completos['tipo_colheita'],
                data_colheita=dados_completos['data_colheita'],
                variedade_cana=dados_completos.get('variedade_cana'),
                idade_cana_meses=int(dados_completos.get('idade_cana_meses')) if dados_completos.get('idade_cana_meses') else None,
                umidade_solo=float(dados_completos.get('umidade_solo')) if dados_completos.get('umidade_solo') else None,
                temperatura_media=float(dados_completos.get('temperatura_media')) if dados_completos.get('temperatura_media') else None,
                precipitacao_mm=float(dados_completos.get('precipitacao_mm')) if dados_completos.get('precipitacao_mm') else None
            )
            
        except Exception as e:
            self.logger.error(f"Erro no modo automático: {e}")
            print(f"❌ Erro: {e}")
            return None
    
    def _modo_manual(self) -> Optional[DadosProducao]:
        """Modo manual: coleta todos os dados do usuário."""
        print("\n📝 MODO MANUAL")
        print("-" * 30)
        return self._coletar_dados_para_calculo()
    
    def _completar_com_valores_padrao(self, dados_dict: dict) -> dict:
        """Completa dados faltantes com valores padrão inteligentes."""
        
        # Criar cópia para não modificar original
        dados = dados_dict.copy()
        
        # Valores padrão baseados em condições típicas do Brasil
        valores_padrao = {
            'idade_cana_meses': 14,  # Idade típica para colheita
            'umidade_solo': 65.0,    # Umidade ideal para cana
            'temperatura_media': 26.5,  # Temperatura média no Brasil
            'precipitacao_mm': 100.0,   # Precipitação mensal típica
            'variedade_cana': 'RB92579'  # Variedade comum
        }
        
        dados_aplicados = []
        
        # Aplicar valores padrão apenas se não existirem
        for campo, valor_padrao in valores_padrao.items():
            if dados.get(campo) is None:
                dados[campo] = valor_padrao
                dados_aplicados.append(f"{campo}: {valor_padrao}")
        
        if dados_aplicados:
            print(f"\n🔧 Valores padrão aplicados:")
            for item in dados_aplicados:
                print(f"   • {item}")
            print("💡 Estes valores são baseados em condições típicas brasileiras")
        
        return dados
    
    def _tem_dados_para_calculo_avancado(self, dados: DadosProducao) -> bool:
        """Verifica se temos dados suficientes para cálculo avançado."""
        return (dados.umidade_solo is not None and 
                dados.idade_cana_meses is not None and 
                dados.temperatura_media is not None and 
                dados.precipitacao_mm is not None)
    
    def _coletar_dados_para_calculo(self) -> Optional[DadosProducao]:
        """Coleta dados diretamente do usuário para cálculo."""
        try:
            print("\n📋 Informe os dados da produção:")
            
            localizacao = input("Localização: ").strip()
            area_ha = float(input("Área plantada (ha): "))
            qtd_colhida = float(input("Quantidade colhida (toneladas): "))
            
            print("Tipo de colheita:")
            print("1. Manual")
            print("2. Mecanizada")
            tipo_opcao = input("Escolha (1 ou 2): ").strip()
            tipo_colheita = "manual" if tipo_opcao == "1" else "mecanizada"
            
            # Para cálculo avançado, coletar dados opcionais
            print("\n📊 Dados para cálculo avançado (opcional):")
            
            idade_str = input("Idade da cana (meses): ").strip()
            idade_meses = int(idade_str) if idade_str else None
            
            umidade_str = input("Umidade do solo (%): ").strip()
            umidade_solo = float(umidade_str) if umidade_str else None
            
            temp_str = input("Temperatura média (°C): ").strip()
            temperatura = float(temp_str) if temp_str else None
            
            precip_str = input("Precipitação (mm): ").strip()
            precipitacao = float(precip_str) if precip_str else None
            
            return DadosProducao(
                localizacao=localizacao,
                area_plantada_ha=area_ha,
                qtd_colhida_toneladas=qtd_colhida,
                tipo_colheita=tipo_colheita,
                data_colheita=date.today(),
                idade_cana_meses=idade_meses,
                umidade_solo=umidade_solo,
                temperatura_media=temperatura,
                precipitacao_mm=precipitacao
            )
            
        except ValueError as e:
            print(f"❌ Erro nos dados: {e}")
            return None
    
    def _carregar_dados_banco(self) -> Optional[DadosProducao]:
        """Carrega dados de produção do banco."""
        if not self.verificar_conexao_banco():
            return None
        
        try:
            # Listar produções disponíveis
            producoes = self.db.listar_producoes(10)
            
            if not producoes:
                print("❌ Nenhuma produção encontrada no banco.")
                return None
            
            print("\n📋 Produções disponíveis:")
            headers = ["ID", "Localização", "Área (ha)", "Colhida (t)", "Tipo", "Data"]
            table_data = []
            
            for p in producoes:
                table_data.append([
                    p['id'],
                    p['localizacao'][:30] + "..." if len(p['localizacao']) > 30 else p['localizacao'],
                    p['area_plantada_ha'],
                    p['qtd_colhida_toneladas'],
                    p['tipo_colheita'],
                    p['data_colheita'].strftime('%d/%m/%Y') if hasattr(p['data_colheita'], 'strftime') else str(p['data_colheita'])
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            # Escolher produção
            producao_id = int(input("\nDigite o ID da produção: "))
            
            # Buscar dados completos
            dados_dict = self.db.buscar_producao_por_id(producao_id)
            
            if not dados_dict:
                print("❌ Produção não encontrada.")
                return None
            
            # Converter para DadosProducao
            return DadosProducao(
                localizacao=dados_dict['localizacao'],
                area_plantada_ha=float(dados_dict['area_plantada_ha']),
                qtd_colhida_toneladas=float(dados_dict['qtd_colhida_toneladas']),
                tipo_colheita=dados_dict['tipo_colheita'],
                data_colheita=dados_dict['data_colheita'],
                variedade_cana=dados_dict.get('variedade_cana'),
                idade_cana_meses=int(dados_dict.get('idade_cana_meses')) if dados_dict.get('idade_cana_meses') else None,
                umidade_solo=float(dados_dict.get('umidade_solo')) if dados_dict.get('umidade_solo') else None,
                temperatura_media=float(dados_dict.get('temperatura_media')) if dados_dict.get('temperatura_media') else None,
                precipitacao_mm=float(dados_dict.get('precipitacao_mm')) if dados_dict.get('precipitacao_mm') else None
            )
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados do banco: {e}")
            return None
    
    def _carregar_dados_json(self) -> Optional[DadosProducao]:
        """Carrega dados de produção de arquivo JSON."""
        try:
            arquivos = self.manipulador_json.listar_arquivos_dados()
            
            if not arquivos:
                print("❌ Nenhum arquivo JSON encontrado.")
                return None
            
            print("\n📂 Arquivos disponíveis:")
            for i, arquivo in enumerate(arquivos, 1):
                print(f"{i}. {arquivo}")
            
            escolha = int(input("Escolha o arquivo (número): ")) - 1
            
            if 0 <= escolha < len(arquivos):
                return self.manipulador_json.carregar_dados_producao(arquivos[escolha])
            else:
                print("❌ Escolha inválida.")
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar JSON: {e}")
            return None
    
    def _exibir_resultado_calculo(self, dados, resultado):
        """Exibe resultados do cálculo de perdas."""
        print("\n" + "="*50)
        print("📊 RESULTADO DO CÁLCULO DE PERDAS")
        print("="*50)
        
        # Dados da produção
        print(f"📍 Localização: {dados.localizacao}")
        print(f"🌾 Área plantada: {dados.area_plantada_ha} ha")
        print(f"⚖️  Quantidade colhida: {dados.qtd_colhida_toneladas} t")
        print(f"🔧 Tipo de colheita: {dados.tipo_colheita}")
        
        print("\n" + "-"*50)
        print("📈 CÁLCULO DE PERDAS")
        print("-"*50)
        
        print(f"💔 Perda estimada: {resultado.perda_estimada_toneladas} toneladas")
        print(f"📉 Percentual de perda: {resultado.percentual_perda}%")
        print(f"🔬 Método: {resultado.metodo_calculo}")
        
        # Produção potencial
        producao_potencial = dados.qtd_colhida_toneladas + resultado.perda_estimada_toneladas
        eficiencia = (dados.qtd_colhida_toneladas / producao_potencial) * 100
        
        print(f"\n🎯 Produção potencial: {producao_potencial:.2f} toneladas")
        print(f"✅ Eficiência da colheita: {eficiencia:.2f}%")
        print(f"📏 Produtividade: {dados.qtd_colhida_toneladas / dados.area_plantada_ha:.2f} t/ha")
        
        if resultado.observacoes:
            print(f"\n📝 Observações: {resultado.observacoes}")
        
        # Fatores aplicados
        if resultado.fatores_aplicados:
            print(f"\n🔍 Fatores aplicados:")
            for fator, valor in resultado.fatores_aplicados.items():
                print(f"  • {fator}: {valor:.3f}")
    
    def _salvar_resultado_calculo(self, dados, resultado):
        """Salva resultado do cálculo."""
        try:
            # Salvar em JSON
            arquivo_json = self.manipulador_json.salvar_resultado_perda(resultado, dados)
            print(f"💾 Relatório salvo em: {arquivo_json}")
            
            # Salvar no banco se disponível
            if self.verificar_conexao_banco():
                try:
                    # Primeiro, buscar ou criar produção no banco
                    dados_producao_dict = {
                        'localizacao': dados.localizacao,
                        'area_plantada_ha': dados.area_plantada_ha,
                        'qtd_colhida_toneladas': dados.qtd_colhida_toneladas,
                        'tipo_colheita': dados.tipo_colheita,
                        'data_colheita': dados.data_colheita,
                        'variedade_cana': dados.variedade_cana,
                        'idade_cana_meses': dados.idade_cana_meses,
                        'umidade_solo': dados.umidade_solo,
                        'temperatura_media': dados.temperatura_media,
                        'precipitacao_mm': dados.precipitacao_mm
                    }
                    
                    producao_id = self.db.inserir_producao_cana(dados_producao_dict)
                    
                    # Salvar cálculo de perda
                    dados_perda = {
                        'producao_id': producao_id,
                        'perda_estimada_toneladas': resultado.perda_estimada_toneladas,
                        'percentual_perda': resultado.percentual_perda,
                        'fatores_perda': resultado.fatores_aplicados,
                        'metodo_calculo': resultado.metodo_calculo,
                        'observacoes': resultado.observacoes
                    }
                    
                    perda_id = self.db.inserir_perda_colheita(dados_perda)
                    print(f"💾 Cálculo também salvo no banco com ID: {perda_id}")
                    
                except Exception as e:
                    self.logger.error(f"Erro ao salvar no banco: {e}")
                    print("⚠️  Erro ao salvar no banco, mas JSON foi salvo.")
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar resultado: {e}")
            print("❌ Erro ao salvar resultado.")
    
    def gerar_relatorios(self):
        """Interface para gerar relatórios."""
        print("\n📊 GERAR RELATÓRIOS")
        print("-" * 40)
        
        if not self.verificar_conexao_banco():
            print("❌ Relatórios requerem conexão com banco de dados.")
            return
        
        try:
            # Opções de filtro de data
            print("Filtro por período:")
            print("1. Todos os dados")
            print("2. Últimos 30 dias")
            print("3. Período personalizado")
            
            opcao = input("Escolha (1, 2 ou 3): ").strip()
            
            data_inicio = None
            data_fim = None
            
            if opcao == "2":
                from datetime import timedelta
                data_inicio = date.today() - timedelta(days=30)
                data_fim = date.today()
            elif opcao == "3":
                data_inicio_str = input("Data início (dd/mm/aaaa): ").strip()
                data_fim_str = input("Data fim (dd/mm/aaaa): ").strip()
                
                if data_inicio_str:
                    data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y").date()
                if data_fim_str:
                    data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y").date()
            
            # Gerar relatório
            df_relatorio = self.db.gerar_relatorio_perdas(data_inicio, data_fim)
            
            if df_relatorio.empty:
                print("❌ Nenhum dado encontrado para o período selecionado.")
                return
            
            # Exibir relatório
            print(f"\n📈 RELATÓRIO DE PERDAS ({len(df_relatorio)} registros)")
            print("="*80)
            
            # Estatísticas gerais
            total_colhido = df_relatorio['qtd_colhida_toneladas'].sum()
            total_perdas = df_relatorio['perda_estimada_toneladas'].sum()
            perda_media = df_relatorio['percentual_perda'].mean()
            
            print(f"📊 Total colhido: {total_colhido:,.2f} toneladas")
            print(f"💔 Total de perdas: {total_perdas:,.2f} toneladas")
            print(f"📉 Perda média: {perda_media:.2f}%")
            
            # Relatório por tipo de colheita
            print("\n🔧 Por tipo de colheita:")
            relatorio_tipo = df_relatorio.groupby('tipo_colheita').agg({
                'qtd_colhida_toneladas': 'sum',
                'perda_estimada_toneladas': 'sum',
                'percentual_perda': 'mean'
            }).round(2)
            
            print(tabulate(relatorio_tipo, headers=relatorio_tipo.columns, tablefmt="grid"))
            
            # Exibir detalhes se solicitado
            ver_detalhes = input("\n🔍 Ver detalhes de cada produção? (s/n): ").strip().lower()
            if ver_detalhes == 's':
                print(f"\n📋 DETALHES DAS PRODUÇÕES")
                print("-"*80)
                
                # Preparar dados para tabela
                df_display = df_relatorio[[
                    'localizacao', 'area_plantada_ha', 'qtd_colhida_toneladas',
                    'tipo_colheita', 'perda_estimada_toneladas', 'percentual_perda'
                ]].copy()
                
                # Truncar localização para caber na tela
                df_display['localizacao'] = df_display['localizacao'].str[:25]
                
                print(tabulate(df_display, headers=df_display.columns, tablefmt="grid", showindex=False))
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            print("❌ Erro ao gerar relatório.")
    
    def gerenciar_json(self):
        """Interface para gerenciar arquivos JSON."""
        print("\n💾 GERENCIAR ARQUIVOS JSON")
        print("-" * 40)
        
        arquivos = self.manipulador_json.listar_arquivos_dados()
        
        if not arquivos:
            print("❌ Nenhum arquivo JSON encontrado.")
            return
        
        print(f"📂 Arquivos encontrados ({len(arquivos)}):")
        for i, arquivo in enumerate(arquivos, 1):
            print(f"{i}. {arquivo}")
        
        print("\nOpções:")
        print("1. Ver conteúdo de um arquivo")
        print("2. Excluir um arquivo")
        print("0. Voltar")
        
        opcao = input("Escolha: ").strip()
        
        if opcao == "1":
            self._ver_conteudo_json(arquivos)
        elif opcao == "2":
            self._excluir_arquivo_json(arquivos)
    
    def _ver_conteudo_json(self, arquivos):
        """Exibe conteúdo de arquivo JSON."""
        try:
            escolha = int(input("Número do arquivo: ")) - 1
            
            if 0 <= escolha < len(arquivos):
                arquivo = arquivos[escolha]
                caminho = os.path.join(self.manipulador_json.diretorio_dados, arquivo)
                
                with open(caminho, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                
                print(f"\n📄 Conteúdo de {arquivo}:")
                print("-" * 50)
                print(conteudo)
            else:
                print("❌ Escolha inválida.")
                
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
    
    def _excluir_arquivo_json(self, arquivos):
        """Exclui arquivo JSON."""
        try:
            escolha = int(input("Número do arquivo: ")) - 1
            
            if 0 <= escolha < len(arquivos):
                arquivo = arquivos[escolha]
                confirmar = input(f"⚠️  Confirma exclusão de '{arquivo}'? (s/n): ").strip().lower()
                
                if confirmar == 's':
                    caminho = os.path.join(self.manipulador_json.diretorio_dados, arquivo)
                    os.remove(caminho)
                    print(f"✅ Arquivo '{arquivo}' excluído.")
                else:
                    print("❌ Exclusão cancelada.")
            else:
                print("❌ Escolha inválida.")
                
        except Exception as e:
            print(f"❌ Erro ao excluir arquivo: {e}")
    
    def consultar_banco(self):
        """Interface para consultas no banco."""
        print("\n🔍 CONSULTAR BANCO DE DADOS")
        print("-" * 40)
        
        if not self.verificar_conexao_banco():
            return
        
        print("Tipos de consulta:")
        print("1. Listar produções")
        print("2. Buscar produção por ID")
        print("3. Ver parâmetros de perdas")
        print("0. Voltar")
        
        opcao = input("Escolha: ").strip()
        
        try:
            if opcao == "1":
                self._listar_producoes()
            elif opcao == "2":
                self._buscar_producao_id()
            elif opcao == "3":
                self._ver_parametros_perdas()
                
        except Exception as e:
            self.logger.error(f"Erro na consulta: {e}")
            print("❌ Erro ao consultar banco.")
    
    def _listar_producoes(self):
        """Lista produções do banco."""
        try:
            producoes = self.db.listar_producoes(20)
            
            if not producoes:
                print("❌ Nenhuma produção encontrada.")
                return
            
            print(f"\n📋 Produções cadastradas ({len(producoes)}):")
            headers = ["ID", "Localização", "Área (ha)", "Colhida (t)", "Tipo", "Data", "Produtividade"]
            table_data = []
            
            for p in producoes:
                table_data.append([
                    p['id'],
                    p['localizacao'][:25] + "..." if len(p['localizacao']) > 25 else p['localizacao'],
                    p['area_plantada_ha'],
                    p['qtd_colhida_toneladas'],
                    p['tipo_colheita'],
                    p['data_colheita'].strftime('%d/%m/%Y') if hasattr(p['data_colheita'], 'strftime') else str(p['data_colheita']),
                    f"{p['produtividade_toneladas_ha']:.1f} t/ha" if p['produtividade_toneladas_ha'] else "N/A"
                ])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
        except Exception as e:
            self.logger.error(f"Erro ao listar produções: {e}")
            print("❌ Erro ao listar produções.")
    
    def _buscar_producao_id(self):
        """Busca produção específica por ID."""
        try:
            producao_id = int(input("ID da produção: "))
            
            dados = self.db.buscar_producao_por_id(producao_id)
            
            if not dados:
                print("❌ Produção não encontrada.")
                return
            
            print(f"\n📋 Produção ID {producao_id}:")
            print("-" * 40)
            
            for chave, valor in dados.items():
                if valor is not None:
                    print(f"{chave}: {valor}")
            
        except ValueError:
            print("❌ ID deve ser um número.")
        except Exception as e:
            self.logger.error(f"Erro ao buscar produção: {e}")
            print("❌ Erro ao buscar produção.")
    
    def _ver_parametros_perdas(self):
        """Exibe parâmetros de cálculo de perdas."""
        try:
            print("\n⚙️  Parâmetros de cálculo de perdas:")
            print("-" * 50)
            
            for tipo in ['manual', 'mecanizada']:
                params = self.db.buscar_parametros_perdas(tipo)
                
                if params:
                    print(f"\n🔧 Colheita {tipo}:")
                    print(f"  • Fator base: {params['fator_base_perda']:.3f} ({params['fator_base_perda']*100:.1f}%)")
                    print(f"  • Fator umidade: {params['fator_umidade']:.3f}")
                    print(f"  • Fator idade: {params['fator_idade']:.3f}")
                    print(f"  • Fator clima: {params['fator_clima']:.3f}")
                    print(f"  • Descrição: {params['descricao']}")
                else:
                    print(f"\n❌ Parâmetros para colheita {tipo} não encontrados.")
            
        except Exception as e:
            self.logger.error(f"Erro ao buscar parâmetros: {e}")
            print("❌ Erro ao buscar parâmetros.")
    
    def calcular_com_gps(self):
        """TUPLA: Demonstra cálculo com coordenadas GPS."""
        print("\n🌍 CÁLCULO COM COORDENADAS GPS (TUPLA)")
        print("="*50)
        
        try:
            # Modo simplificado: usar dados automáticos + GPS
            print("🚀 Modo inteligente: dados do banco + coordenadas GPS")
            
            # Buscar dados automaticamente
            dados = self._modo_automatico()
            if not dados:
                print("💡 Usando dados de exemplo para demonstração...")
                dados = self._criar_dados_exemplo()
            
            # Coletando coordenadas como TUPLA
            print("\n📍 Coordenadas GPS:")
            try:
                lat = float(input("Latitude (ou Enter para -22.5): ").strip() or "-22.5")
                lon = float(input("Longitude (ou Enter para -47.8): ").strip() or "-47.8")
                alt = float(input("Altitude em metros (ou Enter para 600): ").strip() or "600")
            except:
                lat, lon, alt = -22.5, -47.8, 600.0
                print(f"🔧 Usando coordenadas padrão: ({lat}, {lon}, {alt})")
            
            # Criando TUPLA de coordenadas
            coordenadas = (lat, lon, alt)
            
            print(f"\n🔍 Calculando perdas para coordenadas: {coordenadas}")
            resultado = self.calculadora.calcular_com_coordenadas(dados, coordenadas)
            
            print(f"\n📊 RESULTADO:")
            print(f"Perda estimada: {resultado.perda_estimada_toneladas} toneladas")
            print(f"Percentual de perda: {resultado.percentual_perda}%")
            print(f"Observações: {resultado.observacoes}")
            
            # Mostrando fazendas próximas usando LISTA de TUPLAS
            fazendas = self.calculadora.gerenciador.buscar_por_coordenadas(lat, lon, 20)
            if fazendas:
                print(f"\n🏚️  Fazendas próximas (raio 20km):")
                for nome, distancia in fazendas:  # Iterando LISTA de TUPLAS
                    print(f"   • {nome}: {distancia} km")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def analisar_multiplas_medicoes(self):
        """LISTA: Demonstra análise de múltiplas medições de umidade."""
        print("\n📈 ANÁLISE DE MÚLTIPLAS MEDIÇÕES (LISTA)")
        print("="*50)
        
        try:
            # Modo simplificado: usar dados automáticos + medições
            print("🚀 Modo inteligente: dados do banco + múltiplas medições")
            
            # Buscar dados automaticamente
            dados = self._modo_automatico()
            if not dados:
                print("💡 Usando dados de exemplo para demonstração...")
                dados = self._criar_dados_exemplo()
            
            # Coletando LISTA de medições
            print("\n💧 Medições de umidade do solo:")
            print("Opções:")
            print("1. 📝 Inserir medições manualmente")
            print("2. 🎲 Usar medições de exemplo")
            
            opcao = input("Escolha (1 ou 2, Enter para exemplo): ").strip()
            
            if opcao == "1":
                print("Digite as medições separadas por vírgula (ex: 65.5, 67.2, 63.8)")
                medicoes_str = input("Medições (%): ")
                medicoes_umidade = [float(x.strip()) for x in medicoes_str.split(',')]
            else:
                # LISTA de exemplo com variações realistas
                medicoes_umidade = [64.2, 66.8, 63.5, 68.1, 65.9, 67.3, 62.8, 69.0]
                print(f"🎲 Usando medições de exemplo: {medicoes_umidade}")
            
            print(f"\n🔍 Analisando {len(medicoes_umidade)} medições...")
            
            # Processando LISTA de medições
            analise = self.calculadora.processar_multiplas_medicoes(dados, medicoes_umidade)
            
            print(f"\n📊 ANÁLISE COMPLETA:")
            print(f"Total de medições: {analise['total_medicoes']}")
            print(f"Umidade média: {analise['umidade_media']:.2f}%")
            print(f"Faixa umidade: {analise['umidade_min_max'][0]:.1f}% - {analise['umidade_min_max'][1]:.1f}%")
            print(f"Perda média: {analise['perda_media_ton']:.2f} toneladas")
            print(f"Faixa perdas: {analise['perda_min_max_ton'][0]:.2f} - {analise['perda_min_max_ton'][1]:.2f} ton")
            print(f"Percentual médio: {analise['percentual_medio']:.2f}%")
            print(f"Variação percentual: {analise['variacao_percentual']:.2f}%")
            
            print(f"\n📋 RESUMO POR MEDIÇÃO:")
            for i, detalhe in enumerate(analise['resultados_detalhados'][:5]):  # Mostrar apenas 5 para não poluir
                print(f"   {i+1}. Umidade: {detalhe['umidade']:.1f}% → "
                      f"Perda: {detalhe['perda_ton']:.2f}t ({detalhe['percentual']:.2f}%)")
            
            if len(analise['resultados_detalhados']) > 5:
                print(f"   ... e mais {len(analise['resultados_detalhados']) - 5} medições")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _criar_dados_exemplo(self) -> DadosProducao:
        """Cria dados de exemplo para demonstração."""
        return DadosProducao(
            localizacao="Fazenda Exemplo - Talhão Demo",
            area_plantada_ha=100.0,
            qtd_colhida_toneladas=8000.0,
            tipo_colheita="mecanizada",
            data_colheita=date.today(),
            variedade_cana="RB92579",
            idade_cana_meses=14,
            umidade_solo=65.0,
            temperatura_media=26.5,
            precipitacao_mm=100.0
        )
    
    def relatorio_tabela_memoria(self):
        """TABELA DE MEMÓRIA: Demonstra uso de DataFrame para análises."""
        print("\n🗃️  RELATÓRIO TABELA DE MEMÓRIA (DATAFRAME)")
        print("="*50)
        
        try:
            # Gerando relatório com TABELA DE MEMÓRIA
            relatorio = self.calculadora.gerar_relatorio_com_tabela_memoria()
            
            if 'erro' in relatorio:
                print(f"⚠️  {relatorio['erro']}")
                print("💡 Execute alguns cálculos primeiro para popular a tabela.")
                return
            
            print("📊 RESUMO DA TABELA DE MEMÓRIA:")
            resumo = relatorio['resumo_tabela']
            print(f"Total de registros: {resumo['total_registros']}")
            print(f"Colunas disponíveis: {len(resumo['colunas_disponiveis'])}")
            print(f"Memória utilizada: {resumo['memoria_utilizada_mb']:.2f} MB")
            
            print(f"\n📈 ESTATÍSTICAS NUMÉRICAS:")
            stats = relatorio['estatisticas_numericas']
            print(f"Produção total: {stats['producao_total']:.2f} toneladas")
            print(f"Perda total: {stats['perda_total']:.2f} toneladas")
            print(f"Eficiência média: {stats['eficiencia_media']:.2f}%")
            print(f"Produtividade média: {stats['produtividade_media']:.2f} ton/ha")
            print(f"Área total: {stats['area_total']:.2f} hectares")
            
            print(f"\n⏰ ANÁLISE TEMPORAL:")
            temporal = relatorio['analise_temporal']
            print(f"Período: {temporal['periodo_inicio']} até {temporal['periodo_fim']}")
            print(f"Registros por mês: {temporal['registros_por_mes']}")
            
            print(f"\n🌍 ANÁLISE GEOGRÁFICA:")
            geo = relatorio['analise_geografica']
            print(f"Localizações únicas: {geo['localizacoes_unicas']}")
            print(f"Distribuição por local: {geo['distribuicao_locais']}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def estatisticas_historico(self):
        """DICIONÁRIO: Demonstra uso de dicionários para estatísticas."""
        print("\n📋 ESTATÍSTICAS DO HISTÓRICO (DICIONÁRIO)")
        print("="*50)
        
        try:
            # Obtendo estatísticas em DICIONÁRIO
            stats = self.calculadora.gerenciador.obter_estatisticas_historico()
            
            if 'erro' in stats:
                print(f"⚠️  {stats['erro']}")
                print("💡 Execute alguns cálculos primeiro para gerar estatísticas.")
                return
            
            print("📊 ESTATÍSTICAS GERAIS:")
            print(f"Total de cálculos: {stats['total_calculos']}")
            print(f"Localizações únicas: {stats['localizacoes_unicas']}")
            print(f"Produção total: {stats['producao_total_ton']:.2f} toneladas")
            
            print(f"\n📉 ANÁLISE DE PERDAS:")
            print(f"Perda média: {stats['perda_media_ton']:.2f} toneladas")
            print(f"Perda máxima: {stats['perda_maxima_ton']:.2f} toneladas")
            print(f"Perda mínima: {stats['perda_minima_ton']:.2f} toneladas")
            print(f"Percentual médio de perdas: {stats['percentual_medio']:.2f}%")
            
            # Gerando relatório completo que usa TODOS os tipos
            print(f"\n🔍 RELATÓRIO COMPLETO (TODOS OS TIPOS):")
            relatorio_completo = self.calculadora.gerenciador.gerar_relatorio_completo()
            
            print(f"Versão do sistema: {relatorio_completo['info_sistema']['versao']}")  # TUPLA
            print(f"Fazendas cadastradas: {relatorio_completo['fazendas_cadastradas']}")  # LISTA
            print(f"Total no histórico: {relatorio_completo['historico_total']}")  # LISTA
            
            if 'analise_tabela_memoria' in relatorio_completo:
                tabela_info = relatorio_completo['analise_tabela_memoria']
                print(f"Colunas na tabela: {len(tabela_info['colunas_disponiveis'])}")  # LISTA
                print(f"Tipos de colheita: {tabela_info['tipos_colheita']}")  # DICIONÁRIO
                periodo = tabela_info['periodo_analise']  # TUPLA
                print(f"Período dos dados: {periodo[0]} até {periodo[1]}")
            
        except Exception as e:
            print(f"❌ Erro: {e}")


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Sistema de Cálculo de Perdas na Colheita de Cana-de-Açúcar"
    )
    parser.add_argument(
        "--test-connection", 
        action="store_true",
        help="Apenas testa a conexão com o banco"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Sistema Cana-de-Açúcar v1.0"
    )
    
    args = parser.parse_args()
    
    try:
        sistema = SistemaCanaAcucar()
        
        if args.test_connection:
            # Apenas testar conexão
            if sistema.verificar_conexao_banco():
                print("✅ Teste de conexão bem-sucedido!")
                sys.exit(0)
            else:
                print("❌ Teste de conexão falhou!")
                sys.exit(1)
        else:
            # Executar menu principal
            sistema.menu_principal()
            
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Erro crítico: {e}")
        print(f"❌ Erro crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()