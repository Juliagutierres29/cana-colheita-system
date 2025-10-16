"""
Módulo com funções para cálculo de perdas na colheita de cana-de-açúcar.
Sistema de Cálculo de Perdas na Colheita de Cana-de-Açúcar.
"""

import json
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import os
import pandas as pd


@dataclass
class ParametrosPerdas:
    """Classe para armazenar parâmetros de cálculo de perdas."""
    tipo_colheita: str
    fator_base_perda: float
    fator_umidade: float = 0.0
    fator_idade: float = 0.0
    fator_clima: float = 0.0
    descricao: str = ""


@dataclass
class DadosProducao:
    """Classe para dados de produção de cana."""
    localizacao: str
    area_plantada_ha: float
    qtd_colhida_toneladas: float
    tipo_colheita: str
    data_colheita: date
    variedade_cana: Optional[str] = None
    idade_cana_meses: Optional[int] = None
    umidade_solo: Optional[float] = None
    temperatura_media: Optional[float] = None
    precipitacao_mm: Optional[float] = None
    # TUPLA: Coordenadas geográficas (latitude, longitude, altitude)
    coordenadas_gps: Optional[Tuple[float, float, float]] = None
    # LISTA: Histórico de medições de umidade
    historico_umidade: Optional[List[float]] = None


@dataclass
class ResultadoPerda:
    """Classe para resultado do cálculo de perdas."""
    perda_estimada_toneladas: float
    percentual_perda: float
    fatores_aplicados: Dict[str, float]
    metodo_calculo: str
    observacoes: str = ""


class GerenciadorDados:
    """Classe para demonstrar uso de LISTA, TUPLA, DICIONÁRIO e TABELA DE MEMÓRIA."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # LISTA: Histórico de todos os cálculos realizados
        self.historico_calculos: List[Dict[str, Any]] = []
        
        # DICIONÁRIO: Cache de resultados por localização
        self.cache_resultados: Dict[str, ResultadoPerda] = {}
        
        # DICIONÁRIO: Parâmetros de configuração
        self.configuracoes: Dict[str, Any] = {
            'precisao_decimal': 2,
            'modo_debug': False,
            'salvar_automatico': True,
            'formato_data': '%Y-%m-%d'
        }
        
        # TUPLA: Versão do sistema (major, minor, patch)
        self.versao_sistema: Tuple[int, int, int] = (1, 0, 0)
        
        # TABELA DE MEMÓRIA: DataFrame para análises estatísticas
        self.tabela_memoria: pd.DataFrame = pd.DataFrame()
        
        # LISTA de TUPLAS: Coordenadas de fazendas cadastradas
        self.fazendas_cadastradas: List[Tuple[str, float, float]] = [
            ("Fazenda São João", -22.1234, -47.5678),
            ("Fazenda Santa Maria", -23.4567, -46.8910),
            ("Fazenda Boa Vista", -21.9876, -48.1234)
        ]
    
    def adicionar_calculo_historico(self, dados: DadosProducao, resultado: ResultadoPerda) -> None:
        """
        LISTA: Adiciona um cálculo ao histórico usando lista.
        
        Args:
            dados: Dados da produção
            resultado: Resultado do cálculo
        """
        # Criando um registro para adicionar à LISTA
        registro = {
            'timestamp': datetime.now().isoformat(),
            'localizacao': dados.localizacao,
            'area_ha': dados.area_plantada_ha,
            'producao_ton': dados.qtd_colhida_toneladas,
            'perda_ton': resultado.perda_estimada_toneladas,
            'percentual_perda': resultado.percentual_perda,
            'tipo_colheita': dados.tipo_colheita,
            'coordenadas': dados.coordenadas_gps  # TUPLA dentro da lista
        }
        
        # Adicionando à LISTA
        self.historico_calculos.append(registro)
        
        # Atualizando DICIONÁRIO de cache
        self.cache_resultados[dados.localizacao] = resultado
        
        self.logger.info(f"Cálculo adicionado ao histórico. Total: {len(self.historico_calculos)}")
    
    def obter_estatisticas_historico(self) -> Dict[str, Any]:
        """
        LISTA + DICIONÁRIO: Calcula estatísticas do histórico usando lista e retorna dicionário.
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.historico_calculos:  # Verificando se a LISTA está vazia
            return {'erro': 'Nenhum cálculo no histórico'}
        
        # Processando dados da LISTA
        perdas = [calc['perda_ton'] for calc in self.historico_calculos]
        percentuais = [calc['percentual_perda'] for calc in self.historico_calculos]
        producoes = [calc['producao_ton'] for calc in self.historico_calculos]
        
        # DICIONÁRIO com estatísticas
        estatisticas = {
            'total_calculos': len(self.historico_calculos),
            'perda_media_ton': sum(perdas) / len(perdas),
            'perda_maxima_ton': max(perdas),
            'perda_minima_ton': min(perdas),
            'percentual_medio': sum(percentuais) / len(percentuais),
            'producao_total_ton': sum(producoes),
            'localizacoes_unicas': len(set(calc['localizacao'] for calc in self.historico_calculos))
        }
        
        return estatisticas
    
    def criar_tabela_memoria_analise(self) -> pd.DataFrame:
        """
        TABELA DE MEMÓRIA: Cria DataFrame (tabela de memória) com dados do histórico.
        
        Returns:
            DataFrame com dados estruturados
        """
        if not self.historico_calculos:  # Verificando LISTA
            return pd.DataFrame()
        
        # Convertendo LISTA de DICIONÁRIOS em TABELA DE MEMÓRIA (DataFrame)
        self.tabela_memoria = pd.DataFrame(self.historico_calculos)
        
        # Adicionando colunas calculadas na TABELA DE MEMÓRIA
        if not self.tabela_memoria.empty:
            self.tabela_memoria['eficiencia_colheita'] = (
                self.tabela_memoria['producao_ton'] / 
                (self.tabela_memoria['producao_ton'] + self.tabela_memoria['perda_ton'])
            ) * 100
            
            self.tabela_memoria['produtividade_ha'] = (
                self.tabela_memoria['producao_ton'] / self.tabela_memoria['area_ha']
            )
            
            # Convertendo timestamp para datetime na TABELA DE MEMÓRIA
            self.tabela_memoria['timestamp'] = pd.to_datetime(self.tabela_memoria['timestamp'])
        
        self.logger.info(f"Tabela de memória criada com {len(self.tabela_memoria)} registros")
        return self.tabela_memoria
    
    def buscar_por_coordenadas(self, latitude: float, longitude: float, raio_km: float = 10) -> List[Tuple[str, float]]:
        """
        LISTA + TUPLA: Busca fazendas próximas usando lista de tuplas.
        
        Args:
            latitude: Latitude de referência
            longitude: Longitude de referência
            raio_km: Raio de busca em km
            
        Returns:
            Lista de tuplas (nome_fazenda, distancia_km)
        """
        fazendas_proximas: List[Tuple[str, float]] = []
        
        # Iterando pela LISTA de TUPLAS
        for nome, lat, lon in self.fazendas_cadastradas:
            # Cálculo simples de distância (aproximado)
            diff_lat = abs(latitude - lat)
            diff_lon = abs(longitude - lon)
            distancia_aprox = ((diff_lat ** 2 + diff_lon ** 2) ** 0.5) * 111  # km aproximado
            
            if distancia_aprox <= raio_km:
                # Adicionando TUPLA à LISTA
                fazendas_proximas.append((nome, round(distancia_aprox, 2)))
        
        # Ordenando LISTA de TUPLAS por distância
        fazendas_proximas.sort(key=lambda x: x[1])
        
        return fazendas_proximas
    
    def gerar_relatorio_completo(self) -> Dict[str, Any]:
        """
        TODOS OS TIPOS: Demonstra uso de lista, tupla, dicionário e tabela de memória.
        
        Returns:
            Dicionário com relatório completo
        """
        # TABELA DE MEMÓRIA
        df = self.criar_tabela_memoria_analise()
        
        # DICIONÁRIO principal do relatório
        relatorio = {
            'info_sistema': {
                'versao': self.versao_sistema,  # TUPLA
                'configuracoes': self.configuracoes  # DICIONÁRIO
            },
            'estatisticas': self.obter_estatisticas_historico(),  # DICIONÁRIO
            'fazendas_cadastradas': len(self.fazendas_cadastradas),  # LISTA de TUPLAS
            'historico_total': len(self.historico_calculos)  # LISTA
        }
        
        # Análises da TABELA DE MEMÓRIA
        if not df.empty:
            relatorio['analise_tabela_memoria'] = {
                'colunas_disponiveis': list(df.columns),  # LISTA
                'tipos_colheita': df['tipo_colheita'].value_counts().to_dict(),  # DICIONÁRIO
                'media_eficiencia': df['eficiencia_colheita'].mean(),
                'media_produtividade': df['produtividade_ha'].mean(),
                'periodo_analise': (  # TUPLA
                    df['timestamp'].min().isoformat(),
                    df['timestamp'].max().isoformat()
                )
            }
        
        return relatorio


class CalculadoraPerdas:
    """Classe principal para cálculo de perdas na colheita."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Integração com GerenciadorDados para usar todos os tipos obrigatórios
        self.gerenciador = GerenciadorDados()
        
        # Parâmetros padrão para cálculo de perdas
        self.parametros_padrao = {
            'manual': ParametrosPerdas(
                tipo_colheita='manual',
                fator_base_perda=0.05,  # 5% de perda base
                fator_umidade=0.02,     # Fator adicional por umidade
                fator_idade=0.01,       # Fator adicional por idade da cana
                fator_clima=0.015,      # Fator adicional por condições climáticas
                descricao='Colheita manual - menor perda mas depende da experiência'
            ),
            'mecanizada': ParametrosPerdas(
                tipo_colheita='mecanizada',
                fator_base_perda=0.08,  # 8% de perda base
                fator_umidade=0.025,    # Maior sensibilidade à umidade
                fator_idade=0.015,      # Maior impacto da idade
                fator_clima=0.02,       # Maior impacto das condições climáticas
                descricao='Colheita mecanizada - maior eficiência mas perdas mecânicas'
            )
        }
    
    def calcular_perda_basica(self, 
                             qtd_colhida: float, 
                             tipo_colheita: str,
                             parametros: Optional[ParametrosPerdas] = None) -> ResultadoPerda:
        """
        Calcula perda básica baseada apenas no tipo de colheita.
        
        Args:
            qtd_colhida: Quantidade colhida em toneladas
            tipo_colheita: 'manual' ou 'mecanizada'
            parametros: Parâmetros customizados (opcional)
            
        Returns:
            ResultadoPerda com o cálculo básico
        """
        if tipo_colheita not in ['manual', 'mecanizada']:
            raise ValueError("Tipo de colheita deve ser 'manual' ou 'mecanizada'")
        
        # Usar parâmetros fornecidos ou padrão
        params = parametros or self.parametros_padrao[tipo_colheita]
        
        # Cálculo básico
        perda_toneladas = qtd_colhida * params.fator_base_perda
        percentual = params.fator_base_perda * 100
        
        fatores = {
            'fator_base': params.fator_base_perda,
            'tipo_colheita': tipo_colheita
        }
        
        return ResultadoPerda(
            perda_estimada_toneladas=round(perda_toneladas, 2),
            percentual_perda=round(percentual, 2),
            fatores_aplicados=fatores,
            metodo_calculo='basico',
            observacoes=f"Cálculo básico para colheita {tipo_colheita}"
        )
    
    def calcular_perda_avancada(self, 
                               dados_producao: DadosProducao,
                               parametros: Optional[ParametrosPerdas] = None) -> ResultadoPerda:
        """
        Calcula perda considerando fatores ambientais e de produção.
        
        Args:
            dados_producao: Dados completos da produção
            parametros: Parâmetros customizados (opcional)
            
        Returns:
            ResultadoPerda com cálculo avançado
        """
        if dados_producao.tipo_colheita not in ['manual', 'mecanizada']:
            raise ValueError("Tipo de colheita deve ser 'manual' ou 'mecanizada'")
        
        # Usar parâmetros fornecidos ou padrão
        params = parametros or self.parametros_padrao[dados_producao.tipo_colheita]
        
        # Fator base
        fator_total = params.fator_base_perda
        fatores_aplicados = {'fator_base': params.fator_base_perda}
        
        # Ajuste por umidade do solo
        if dados_producao.umidade_solo is not None:
            fator_umidade = self._calcular_fator_umidade(
                dados_producao.umidade_solo, params.fator_umidade
            )
            fator_total += fator_umidade
            fatores_aplicados['fator_umidade'] = fator_umidade
        
        # Ajuste por idade da cana
        if dados_producao.idade_cana_meses is not None:
            fator_idade = self._calcular_fator_idade(
                dados_producao.idade_cana_meses, params.fator_idade
            )
            fator_total += fator_idade
            fatores_aplicados['fator_idade'] = fator_idade
        
        # Ajuste por condições climáticas
        if dados_producao.temperatura_media is not None and dados_producao.precipitacao_mm is not None:
            fator_clima = self._calcular_fator_climatico(
                dados_producao.temperatura_media,
                dados_producao.precipitacao_mm,
                params.fator_clima
            )
            fator_total += fator_clima
            fatores_aplicados['fator_clima'] = fator_clima
        
        # Limitação do fator total (não pode exceder 25%)
        fator_total = min(fator_total, 0.25)
        
        # Cálculo final
        perda_toneladas = dados_producao.qtd_colhida_toneladas * fator_total
        percentual = fator_total * 100
        
        observacoes = self._gerar_observacoes_avancadas(dados_producao, fatores_aplicados)
        
        resultado = ResultadoPerda(
            perda_estimada_toneladas=round(perda_toneladas, 2),
            percentual_perda=round(percentual, 2),
            fatores_aplicados=fatores_aplicados,
            metodo_calculo='avancado',
            observacoes=observacoes
        )
        
        # USANDO TODOS OS TIPOS: Salvando no histórico
        self.gerenciador.adicionar_calculo_historico(dados_producao, resultado)
        
        return resultado
    
    def calcular_com_coordenadas(self, dados_producao: DadosProducao, 
                                coordenadas: Tuple[float, float, float]) -> ResultadoPerda:
        """
        TUPLA: Calcula perdas incluindo coordenadas GPS.
        
        Args:
            dados_producao: Dados da produção
            coordenadas: Tupla com (latitude, longitude, altitude)
            
        Returns:
            ResultadoPerda com informações geográficas
        """
        # Atualizando dados com TUPLA de coordenadas
        dados_producao.coordenadas_gps = coordenadas
        
        # Cálculo normal
        resultado = self.calcular_perda_avancada(dados_producao)
        
        # LISTA + TUPLA: Buscando fazendas próximas
        lat, lon, alt = coordenadas  # Desempacotando TUPLA
        fazendas_proximas = self.gerenciador.buscar_por_coordenadas(lat, lon, 15)
        
        # Adicionando informação geográfica às observações
        if fazendas_proximas:  # Verificando se LISTA não está vazia
            nomes_fazendas = [nome for nome, dist in fazendas_proximas]  # LISTA de strings
            resultado.observacoes += f" | Fazendas próximas: {', '.join(nomes_fazendas)}"
        
        return resultado
    
    def processar_multiplas_medicoes(self, dados_base: DadosProducao, 
                                   medicoes_umidade: List[float]) -> Dict[str, Any]:
        """
        LISTA + DICIONÁRIO: Processa múltiplas medições de umidade.
        
        Args:
            dados_base: Dados base da produção
            medicoes_umidade: Lista de medições de umidade
            
        Returns:
            Dicionário com resultados das análises
        """
        # Atualizando dados com LISTA de medições
        dados_base.historico_umidade = medicoes_umidade
        
        # LISTA para armazenar resultados
        resultados_medicoes: List[ResultadoPerda] = []
        
        # Processando cada medição da LISTA
        for umidade in medicoes_umidade:
            dados_temp = DadosProducao(
                localizacao=dados_base.localizacao,
                area_plantada_ha=dados_base.area_plantada_ha,
                qtd_colhida_toneladas=dados_base.qtd_colhida_toneladas,
                tipo_colheita=dados_base.tipo_colheita,
                data_colheita=dados_base.data_colheita,
                umidade_solo=umidade,  # Usando valor específico da LISTA
                idade_cana_meses=dados_base.idade_cana_meses,
                temperatura_media=dados_base.temperatura_media,
                precipitacao_mm=dados_base.precipitacao_mm
            )
            
            resultado = self.calcular_perda_avancada(dados_temp)
            resultados_medicoes.append(resultado)  # Adicionando à LISTA
        
        # DICIONÁRIO com análise dos resultados
        perdas = [r.perda_estimada_toneladas for r in resultados_medicoes]  # LISTA
        percentuais = [r.percentual_perda for r in resultados_medicoes]  # LISTA
        
        analise = {
            'total_medicoes': len(medicoes_umidade),  # Tamanho da LISTA
            'umidade_media': sum(medicoes_umidade) / len(medicoes_umidade),  # LISTA
            'umidade_min_max': (min(medicoes_umidade), max(medicoes_umidade)),  # TUPLA
            'perda_media_ton': sum(perdas) / len(perdas),  # LISTA
            'perda_min_max_ton': (min(perdas), max(perdas)),  # TUPLA
            'percentual_medio': sum(percentuais) / len(percentuais),  # LISTA
            'variacao_percentual': max(percentuais) - min(percentuais),  # LISTA
            'medicoes_originais': medicoes_umidade,  # LISTA original
            'resultados_detalhados': [  # LISTA de DICIONÁRIOS
                {
                    'umidade': medicoes_umidade[i],
                    'perda_ton': resultados_medicoes[i].perda_estimada_toneladas,
                    'percentual': resultados_medicoes[i].percentual_perda
                }
                for i in range(len(medicoes_umidade))
            ]
        }
        
        return analise
    
    def gerar_relatorio_com_tabela_memoria(self) -> Dict[str, Any]:
        """
        TABELA DE MEMÓRIA + DICIONÁRIO: Gera relatório usando DataFrame.
        
        Returns:
            Dicionário com análise da tabela de memória
        """
        # Criando TABELA DE MEMÓRIA
        df = self.gerenciador.criar_tabela_memoria_analise()
        
        if df.empty:
            return {'erro': 'Nenhum dado na tabela de memória'}
        
        # DICIONÁRIO com análises da TABELA DE MEMÓRIA
        relatorio = {
            'resumo_tabela': {
                'total_registros': len(df),  # Linhas da tabela
                'colunas_disponiveis': list(df.columns),  # LISTA de colunas
                'tipos_dados': df.dtypes.to_dict(),  # DICIONÁRIO de tipos
                'memoria_utilizada_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
            },
            'estatisticas_numericas': {
                'producao_total': df['producao_ton'].sum(),
                'perda_total': df['perda_ton'].sum(),
                'eficiencia_media': df['eficiencia_colheita'].mean(),
                'produtividade_media': df['produtividade_ha'].mean(),
                'area_total': df['area_ha'].sum()
            },
            'analise_temporal': {
                'periodo_inicio': df['timestamp'].min().isoformat(),
                'periodo_fim': df['timestamp'].max().isoformat(),
                'registros_por_mes': df.groupby(df['timestamp'].dt.month).size().to_dict()
            },
            'analise_geografica': {
                'localizacoes_unicas': df['localizacao'].nunique(),
                'distribuicao_locais': df['localizacao'].value_counts().to_dict()
            }
        }
        
        return relatorio
    
    def _calcular_fator_umidade(self, umidade_solo: float, fator_base: float) -> float:
        """
        Calcula fator de ajuste baseado na umidade do solo.
        
        Args:
            umidade_solo: Percentual de umidade do solo (0-100)
            fator_base: Fator base para umidade
            
        Returns:
            Fator de ajuste para umidade
        """
        # Umidade ideal está entre 60-70%
        if 60 <= umidade_solo <= 70:
            return 0.0  # Condições ideais
        elif umidade_solo < 60:
            # Solo muito seco aumenta perdas
            return fator_base * (60 - umidade_solo) / 30
        else:
            # Solo muito úmido também aumenta perdas
            return fator_base * (umidade_solo - 70) / 30
    
    def _calcular_fator_idade(self, idade_meses: int, fator_base: float) -> float:
        """
        Calcula fator de ajuste baseado na idade da cana.
        
        Args:
            idade_meses: Idade da cana em meses
            fator_base: Fator base para idade
            
        Returns:
            Fator de ajuste para idade
        """
        # Idade ideal está entre 12-18 meses
        if 12 <= idade_meses <= 18:
            return 0.0  # Idade ideal
        elif idade_meses < 12:
            # Cana muito nova
            return fator_base * (12 - idade_meses) / 6
        else:
            # Cana muito velha (mais dura, mais perdas)
            return fator_base * (idade_meses - 18) / 12
    
    def _calcular_fator_climatico(self, temperatura: float, precipitacao: float, fator_base: float) -> float:
        """
        Calcula fator baseado em condições climáticas.
        
        Args:
            temperatura: Temperatura média em Celsius
            precipitacao: Precipitação acumulada em mm
            fator_base: Fator base para clima
            
        Returns:
            Fator de ajuste climático
        """
        fator_temp = 0.0
        fator_chuva = 0.0
        
        # Temperatura ideal entre 25-30°C
        if temperatura < 25:
            fator_temp = fator_base * (25 - temperatura) / 10
        elif temperatura > 30:
            fator_temp = fator_base * (temperatura - 30) / 10
        
        # Precipitação ideal entre 1000-1500mm anuais
        # Ajustando para valores mensais aproximados
        precipitacao_ideal_min = 80   # ~1000mm/12 meses
        precipitacao_ideal_max = 125  # ~1500mm/12 meses
        
        if precipitacao < precipitacao_ideal_min:
            fator_chuva = fator_base * (precipitacao_ideal_min - precipitacao) / precipitacao_ideal_min
        elif precipitacao > precipitacao_ideal_max:
            fator_chuva = fator_base * (precipitacao - precipitacao_ideal_max) / precipitacao_ideal_max
        
        return (fator_temp + fator_chuva) / 2
    
    def _gerar_observacoes_avancadas(self, dados: DadosProducao, fatores: Dict[str, float]) -> str:
        """Gera observações detalhadas sobre o cálculo."""
        observacoes = [f"Cálculo avançado para colheita {dados.tipo_colheita}"]
        
        if 'fator_umidade' in fatores and fatores['fator_umidade'] != 0:
            if dados.umidade_solo < 60:
                observacoes.append(f"Solo seco ({dados.umidade_solo}%) aumentou perdas")
            elif dados.umidade_solo > 70:
                observacoes.append(f"Solo muito úmido ({dados.umidade_solo}%) aumentou perdas")
        
        if 'fator_idade' in fatores and fatores['fator_idade'] != 0:
            if dados.idade_cana_meses < 12:
                observacoes.append(f"Cana jovem ({dados.idade_cana_meses} meses) gerou mais perdas")
            elif dados.idade_cana_meses > 18:
                observacoes.append(f"Cana madura ({dados.idade_cana_meses} meses) gerou mais perdas")
        
        if 'fator_clima' in fatores and fatores['fator_clima'] != 0:
            observacoes.append("Condições climáticas adversas identificadas")
        
        return "; ".join(observacoes)


class ManipuladorJSON:
    """Classe para manipulação de arquivos JSON."""
    
    def __init__(self, diretorio_dados: str = "data"):
        self.diretorio_dados = diretorio_dados
        self.logger = logging.getLogger(__name__)
        
        # Criar diretório se não existir
        os.makedirs(diretorio_dados, exist_ok=True)
    
    def salvar_dados_producao(self, dados: DadosProducao, arquivo: str = None) -> str:
        """
        Salva dados de produção em arquivo JSON.
        
        Args:
            dados: Dados de produção
            arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = f"producao_{timestamp}.json"
        
        caminho_arquivo = os.path.join(self.diretorio_dados, arquivo)
        
        # Converter para dicionário
        dados_dict = {
            'localizacao': dados.localizacao,
            'area_plantada_ha': dados.area_plantada_ha,
            'qtd_colhida_toneladas': dados.qtd_colhida_toneladas,
            'tipo_colheita': dados.tipo_colheita,
            'data_colheita': dados.data_colheita.isoformat(),
            'variedade_cana': dados.variedade_cana,
            'idade_cana_meses': dados.idade_cana_meses,
            'umidade_solo': dados.umidade_solo,
            'temperatura_media': dados.temperatura_media,
            'precipitacao_mm': dados.precipitacao_mm,
            'timestamp_exportacao': datetime.now().isoformat()
        }
        
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Dados de produção salvos em: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar dados de produção: {e}")
            raise
    
    def carregar_dados_producao(self, arquivo: str) -> DadosProducao:
        """
        Carrega dados de produção de arquivo JSON.
        
        Args:
            arquivo: Nome ou caminho do arquivo
            
        Returns:
            DadosProducao carregados
        """
        # Se só o nome foi fornecido, assumir que está no diretório de dados
        if not os.path.dirname(arquivo):
            arquivo = os.path.join(self.diretorio_dados, arquivo)
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados_dict = json.load(f)
            
            # Converter data de string para date
            data_colheita = datetime.fromisoformat(dados_dict['data_colheita']).date()
            
            dados = DadosProducao(
                localizacao=dados_dict['localizacao'],
                area_plantada_ha=dados_dict['area_plantada_ha'],
                qtd_colhida_toneladas=dados_dict['qtd_colhida_toneladas'],
                tipo_colheita=dados_dict['tipo_colheita'],
                data_colheita=data_colheita,
                variedade_cana=dados_dict.get('variedade_cana'),
                idade_cana_meses=dados_dict.get('idade_cana_meses'),
                umidade_solo=dados_dict.get('umidade_solo'),
                temperatura_media=dados_dict.get('temperatura_media'),
                precipitacao_mm=dados_dict.get('precipitacao_mm')
            )
            
            self.logger.info(f"Dados de produção carregados de: {arquivo}")
            return dados
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados de produção: {e}")
            raise
    
    def salvar_resultado_perda(self, resultado: ResultadoPerda, dados_producao: DadosProducao, arquivo: str = None) -> str:
        """
        Salva resultado de cálculo de perda em arquivo JSON.
        
        Args:
            resultado: Resultado do cálculo
            dados_producao: Dados originais da produção
            arquivo: Nome do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if not arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = f"relatorio_perdas_{timestamp}.json"
        
        caminho_arquivo = os.path.join(self.diretorio_dados, arquivo)
        
        # Compilar dados completos
        relatorio = {
            'dados_producao': {
                'localizacao': dados_producao.localizacao,
                'area_plantada_ha': dados_producao.area_plantada_ha,
                'qtd_colhida_toneladas': dados_producao.qtd_colhida_toneladas,
                'tipo_colheita': dados_producao.tipo_colheita,
                'data_colheita': dados_producao.data_colheita.isoformat()
            },
            'calculo_perdas': {
                'perda_estimada_toneladas': resultado.perda_estimada_toneladas,
                'percentual_perda': resultado.percentual_perda,
                'fatores_aplicados': resultado.fatores_aplicados,
                'metodo_calculo': resultado.metodo_calculo,
                'observacoes': resultado.observacoes
            },
            'resumo': {
                'producao_potencial_toneladas': dados_producao.qtd_colhida_toneladas + resultado.perda_estimada_toneladas,
                'eficiencia_colheita': round((dados_producao.qtd_colhida_toneladas / (dados_producao.qtd_colhida_toneladas + resultado.perda_estimada_toneladas)) * 100, 2),
                'produtividade_ha': round(dados_producao.qtd_colhida_toneladas / dados_producao.area_plantada_ha, 2)
            },
            'timestamp_calculo': datetime.now().isoformat()
        }
        
        try:
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(relatorio, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Relatório de perdas salvo em: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar relatório de perdas: {e}")
            raise
    
    def listar_arquivos_dados(self) -> List[str]:
        """
        Lista arquivos JSON no diretório de dados.
        
        Returns:
            Lista de nomes de arquivos JSON
        """
        try:
            arquivos = [f for f in os.listdir(self.diretorio_dados) if f.endswith('.json')]
            return sorted(arquivos)
        except Exception as e:
            self.logger.error(f"Erro ao listar arquivos: {e}")
            return []


def validar_dados_producao(dados: Dict[str, Any]) -> List[str]:
    """
    Valida dados de produção de cana.
    
    Args:
        dados: Dicionário com dados a validar
        
    Returns:
        Lista de erros encontrados (vazia se dados válidos)
    """
    erros = []
    
    # Campos obrigatórios
    campos_obrigatorios = [
        'localizacao', 'area_plantada_ha', 'qtd_colhida_toneladas', 'tipo_colheita'
    ]
    
    for campo in campos_obrigatorios:
        if campo not in dados or dados[campo] is None:
            erros.append(f"Campo obrigatório '{campo}' não fornecido")
    
    # Validações específicas
    if 'area_plantada_ha' in dados and dados['area_plantada_ha'] is not None:
        if dados['area_plantada_ha'] <= 0:
            erros.append("Área plantada deve ser maior que zero")
    
    if 'qtd_colhida_toneladas' in dados and dados['qtd_colhida_toneladas'] is not None:
        if dados['qtd_colhida_toneladas'] < 0:
            erros.append("Quantidade colhida não pode ser negativa")
    
    if 'tipo_colheita' in dados and dados['tipo_colheita'] is not None:
        if dados['tipo_colheita'] not in ['manual', 'mecanizada']:
            erros.append("Tipo de colheita deve ser 'manual' ou 'mecanizada'")
    
    # Validações opcionais
    if 'umidade_solo' in dados and dados['umidade_solo'] is not None:
        if not (0 <= dados['umidade_solo'] <= 100):
            erros.append("Umidade do solo deve estar entre 0 e 100%")
    
    if 'idade_cana_meses' in dados and dados['idade_cana_meses'] is not None:
        if dados['idade_cana_meses'] <= 0:
            erros.append("Idade da cana deve ser maior que zero")
    
    return erros