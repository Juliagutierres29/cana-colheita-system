"""
Módulo para conexão com PostgreSQL.
Sistema de Cálculo de Perdas na Colheita de Cana-de-Açúcar.
"""

import psycopg2
import psycopg2.extras
import logging
import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager
import pandas as pd


class PostgreSQLDatabase:
    """Classe para gerenciar conexões e operações com banco PostgreSQL."""
    
    def __init__(self, 
                 host: str = "localhost",
                 port: int = 5432,
                 database: str = "cana_db",
                 username: str = "cana_user",
                 password: str = "CanaPassword123"):
        """
        Inicializa a conexão com o banco PostgreSQL.
        
        Args:
            host: Endereço do servidor PostgreSQL
            port: Porta de conexão
            database: Nome do banco de dados
            username: Nome do usuário
            password: Senha do usuário
        """
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def get_connection(self):
        """
        Context manager para conexões com o banco.
        
        Yields:
            psycopg2.Connection: Conexão ativa com o banco
        """
        connection = None
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            connection.autocommit = True
            self.logger.info("Conexão PostgreSQL estabelecida com sucesso")
            yield connection
        except psycopg2.Error as e:
            self.logger.error(f"Erro de banco PostgreSQL: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}")
            raise
        finally:
            if connection:
                connection.close()
                self.logger.info("Conexão PostgreSQL fechada")
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com o banco.
        
        Returns:
            bool: True se conexão for bem-sucedida
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
                return result['test'] == 1
        except Exception as e:
            self.logger.error(f"Falha no teste de conexão: {e}")
            return False
    
    def inserir_producao_cana(self, dados_producao: Dict[str, Any]) -> int:
        """
        Insere dados de produção de cana no banco.
        
        Args:
            dados_producao: Dicionário com dados da produção
            
        Returns:
            int: ID do registro inserido
        """
        sql = """
        INSERT INTO producao_cana 
        (localizacao, area_plantada_ha, qtd_colhida_toneladas, tipo_colheita, 
         data_colheita, variedade_cana, idade_cana_meses, umidade_solo, 
         temperatura_media, precipitacao_mm)
        VALUES 
        (%(localizacao)s, %(area_plantada_ha)s, %(qtd_colhida_toneladas)s, %(tipo_colheita)s,
         %(data_colheita)s, %(variedade_cana)s, %(idade_cana_meses)s, %(umidade_solo)s,
         %(temperatura_media)s, %(precipitacao_mm)s)
        RETURNING id
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Preparar dados
                dados_sql = {
                    'localizacao': dados_producao['localizacao'],
                    'area_plantada_ha': dados_producao['area_plantada_ha'],
                    'qtd_colhida_toneladas': dados_producao['qtd_colhida_toneladas'],
                    'tipo_colheita': dados_producao['tipo_colheita'],
                    'data_colheita': dados_producao.get('data_colheita', datetime.now().date()),
                    'variedade_cana': dados_producao.get('variedade_cana'),
                    'idade_cana_meses': dados_producao.get('idade_cana_meses'),
                    'umidade_solo': dados_producao.get('umidade_solo'),
                    'temperatura_media': dados_producao.get('temperatura_media'),
                    'precipitacao_mm': dados_producao.get('precipitacao_mm')
                }
                
                cursor.execute(sql, dados_sql)
                registro_id = cursor.fetchone()['id']
                
                self.logger.info(f"Produção inserida com ID: {registro_id}")
                return registro_id
                
        except Exception as e:
            self.logger.error(f"Erro ao inserir produção: {e}")
            raise
    
    def inserir_perda_colheita(self, dados_perda: Dict[str, Any]) -> int:
        """
        Insere cálculo de perda no banco.
        
        Args:
            dados_perda: Dicionário com dados da perda calculada
            
        Returns:
            int: ID do registro de perda inserido
        """
        sql = """
        INSERT INTO perdas_colheita 
        (producao_id, perda_estimada_toneladas, percentual_perda, 
         fatores_perda, metodo_calculo, observacoes)
        VALUES 
        (%(producao_id)s, %(perda_estimada_toneladas)s, %(percentual_perda)s,
         %(fatores_perda)s, %(metodo_calculo)s, %(observacoes)s)
        RETURNING id
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Converter fatores_perda para JSON se for dict
                fatores_json = dados_perda.get('fatores_perda', {})
                if isinstance(fatores_json, dict):
                    fatores_json = json.dumps(fatores_json)
                
                dados_sql = {
                    'producao_id': dados_perda['producao_id'],
                    'perda_estimada_toneladas': dados_perda['perda_estimada_toneladas'],
                    'percentual_perda': dados_perda['percentual_perda'],
                    'fatores_perda': fatores_json,
                    'metodo_calculo': dados_perda.get('metodo_calculo', 'sistema_automatico'),
                    'observacoes': dados_perda.get('observacoes')
                }
                
                cursor.execute(sql, dados_sql)
                registro_id = cursor.fetchone()['id']
                
                self.logger.info(f"Perda inserida com ID: {registro_id}")
                return registro_id
                
        except Exception as e:
            self.logger.error(f"Erro ao inserir perda: {e}")
            raise
    
    def buscar_producao_por_id(self, producao_id: int) -> Optional[Dict[str, Any]]:
        """
        Busca dados de produção por ID.
        
        Args:
            producao_id: ID da produção
            
        Returns:
            Dict com dados da produção ou None se não encontrada
        """
        sql = """
        SELECT id, localizacao, area_plantada_ha, qtd_colhida_toneladas,
               tipo_colheita, data_colheita, variedade_cana, idade_cana_meses,
               umidade_solo, temperatura_media, precipitacao_mm, produtividade_toneladas_ha,
               data_criacao, data_atualizacao
        FROM producao_cana 
        WHERE id = %(producao_id)s
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, {'producao_id': producao_id})
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao buscar produção {producao_id}: {e}")
            raise
    
    def buscar_parametros_perdas(self, tipo_colheita: str) -> Optional[Dict[str, Any]]:
        """
        Busca parâmetros para cálculo de perdas por tipo de colheita.
        
        Args:
            tipo_colheita: 'manual' ou 'mecanizada'
            
        Returns:
            Dict com parâmetros ou None se não encontrados
        """
        sql = """
        SELECT tipo_colheita, fator_base_perda, fator_umidade, 
               fator_idade, fator_clima, descricao
        FROM parametros_perdas 
        WHERE tipo_colheita = %(tipo_colheita)s AND ativo = true
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, {'tipo_colheita': tipo_colheita})
                row = cursor.fetchone()
                
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            self.logger.error(f"Erro ao buscar parâmetros para {tipo_colheita}: {e}")
            raise
    
    def listar_producoes(self, limite: int = 50) -> List[Dict[str, Any]]:
        """
        Lista produções cadastradas.
        
        Args:
            limite: Número máximo de registros a retornar
            
        Returns:
            Lista de dicionários com dados das produções
        """
        sql = """
        SELECT id, localizacao, area_plantada_ha, qtd_colhida_toneladas,
               tipo_colheita, data_colheita, produtividade_toneladas_ha
        FROM producao_cana 
        ORDER BY data_colheita DESC
        LIMIT %(limite)s
        """
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, {'limite': limite})
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Erro ao listar produções: {e}")
            raise
    
    def gerar_relatorio_perdas(self, data_inicio: date = None, data_fim: date = None) -> pd.DataFrame:
        """
        Gera relatório consolidado de perdas.
        
        Args:
            data_inicio: Data inicial para filtro (opcional)
            data_fim: Data final para filtro (opcional)
            
        Returns:
            DataFrame do pandas com dados do relatório
        """
        sql = """
        SELECT * FROM vw_relatorio_perdas
        WHERE 1=1
        """
        
        params = {}
        
        if data_inicio:
            sql += " AND data_colheita >= %(data_inicio)s"
            params['data_inicio'] = data_inicio
            
        if data_fim:
            sql += " AND data_colheita <= %(data_fim)s"
            params['data_fim'] = data_fim
            
        sql += " ORDER BY data_colheita DESC"
        
        try:
            conn_str = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            return pd.read_sql(sql, conn_str, params=params)
                
        except Exception as e:
            self.logger.error(f"Erro ao gerar relatório: {e}")
            raise
    
    def executar_sql_customizado(self, sql: str, params: Dict = None) -> List[Tuple]:
        """
        Executa SQL customizado (apenas SELECT).
        
        Args:
            sql: Comando SQL SELECT
            params: Parâmetros para o SQL
            
        Returns:
            Lista de tuplas com resultados
        """
        if not sql.strip().upper().startswith('SELECT'):
            raise ValueError("Apenas comandos SELECT são permitidos")
        
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or {})
                return cursor.fetchall()
                
        except Exception as e:
            self.logger.error(f"Erro ao executar SQL customizado: {e}")
            raise