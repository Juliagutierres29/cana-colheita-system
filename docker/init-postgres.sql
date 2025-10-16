-- Script de inicialização para PostgreSQL
-- Sistema de Cálculo de Perdas - Cana-de-Açúcar

-- Criar tabela principal de produção de cana
CREATE TABLE producao_cana (
    id SERIAL PRIMARY KEY,
    localizacao VARCHAR(100) NOT NULL,
    area_plantada_ha DECIMAL(10,2) NOT NULL CHECK (area_plantada_ha > 0),
    qtd_colhida_toneladas DECIMAL(12,2) NOT NULL CHECK (qtd_colhida_toneladas >= 0),
    tipo_colheita VARCHAR(20) NOT NULL CHECK (tipo_colheita IN ('manual', 'mecanizada')),
    data_colheita DATE NOT NULL,
    variedade_cana VARCHAR(50),
    idade_cana_meses INTEGER CHECK (idade_cana_meses > 0),
    umidade_solo DECIMAL(5,2) CHECK (umidade_solo BETWEEN 0 AND 100),
    temperatura_media DECIMAL(4,1),
    precipitacao_mm DECIMAL(6,2) CHECK (precipitacao_mm >= 0),
    produtividade_toneladas_ha DECIMAL(6,2) GENERATED ALWAYS AS (qtd_colhida_toneladas / area_plantada_ha) STORED,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela para armazenar cálculos de perdas
CREATE TABLE perdas_colheita (
    id SERIAL PRIMARY KEY,
    producao_id INTEGER NOT NULL,
    perda_estimada_toneladas DECIMAL(10,2) NOT NULL CHECK (perda_estimada_toneladas >= 0),
    percentual_perda DECIMAL(5,2) NOT NULL CHECK (percentual_perda BETWEEN 0 AND 100),
    fatores_perda JSONB, -- JSON com fatores que contribuíram para a perda
    metodo_calculo VARCHAR(50) NOT NULL,
    observacoes TEXT,
    calculado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producao_id) REFERENCES producao_cana(id) ON DELETE CASCADE
);

-- Criar tabela para parâmetros de cálculo de perdas
CREATE TABLE parametros_perdas (
    id SERIAL PRIMARY KEY,
    tipo_colheita VARCHAR(20) NOT NULL CHECK (tipo_colheita IN ('manual', 'mecanizada')),
    fator_base_perda DECIMAL(4,3) NOT NULL CHECK (fator_base_perda BETWEEN 0 AND 1),
    fator_umidade DECIMAL(4,3) DEFAULT 0,
    fator_idade DECIMAL(4,3) DEFAULT 0,
    fator_clima DECIMAL(4,3) DEFAULT 0,
    descricao VARCHAR(200),
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (tipo_colheita, ativo)
);

-- Inserir parâmetros padrão para cálculo de perdas
INSERT INTO parametros_perdas (tipo_colheita, fator_base_perda, fator_umidade, fator_idade, fator_clima, descricao) VALUES
('manual', 0.05, 0.02, 0.01, 0.015, 'Parâmetros para colheita manual - perda base 5%');

INSERT INTO parametros_perdas (tipo_colheita, fator_base_perda, fator_umidade, fator_idade, fator_clima, descricao) VALUES
('mecanizada', 0.08, 0.025, 0.015, 0.02, 'Parâmetros para colheita mecanizada - perda base 8%');

-- Criar índices para melhor performance
CREATE INDEX idx_producao_data ON producao_cana(data_colheita);
CREATE INDEX idx_producao_tipo ON producao_cana(tipo_colheita);
CREATE INDEX idx_producao_local ON producao_cana(localizacao);
CREATE INDEX idx_perdas_producao ON perdas_colheita(producao_id);

-- Criar view para relatórios consolidados
CREATE OR REPLACE VIEW vw_relatorio_perdas AS
SELECT 
    p.id,
    p.localizacao,
    p.area_plantada_ha,
    p.qtd_colhida_toneladas,
    p.tipo_colheita,
    p.data_colheita,
    p.produtividade_toneladas_ha,
    l.perda_estimada_toneladas,
    l.percentual_perda,
    l.metodo_calculo,
    l.calculado_em,
    (p.qtd_colhida_toneladas + l.perda_estimada_toneladas) AS producao_potencial_toneladas
FROM producao_cana p
LEFT JOIN perdas_colheita l ON p.id = l.producao_id
ORDER BY p.data_colheita DESC;

-- Inserir dados de exemplo para teste
INSERT INTO producao_cana (localizacao, area_plantada_ha, qtd_colhida_toneladas, tipo_colheita, data_colheita, variedade_cana, idade_cana_meses, umidade_solo, temperatura_media, precipitacao_mm) VALUES
('Fazenda São José - Talhão 1', 50.5, 4040.0, 'mecanizada', '2024-07-15', 'RB92579', 12, 65.5, 28.5, 1250.0);

INSERT INTO producao_cana (localizacao, area_plantada_ha, qtd_colhida_toneladas, tipo_colheita, data_colheita, variedade_cana, idade_cana_meses, umidade_solo, temperatura_media, precipitacao_mm) VALUES
('Fazenda Boa Vista - Setor A', 25.0, 1750.0, 'manual', '2024-08-10', 'SP813250', 14, 58.0, 29.0, 980.5);

INSERT INTO producao_cana (localizacao, area_plantada_ha, qtd_colhida_toneladas, tipo_colheita, data_colheita, variedade_cana, idade_cana_meses, umidade_solo, temperatura_media, precipitacao_mm) VALUES
('Usina Central - Área 3', 120.0, 10800.0, 'mecanizada', '2024-09-05', 'CTC4', 11, 72.0, 27.5, 1450.2);