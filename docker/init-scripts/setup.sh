#!/bin/bash
# Script de inicialização do banco Oracle para o sistema de cana-de-açúcar

echo "Aguardando Oracle Database estar disponível..."

# Aguardar banco estar disponível
until sqlplus -L system/OraclePassword123@//localhost:1521/XE @/dev/null; do
  echo "Oracle ainda não está disponível. Aguardando..."
  sleep 10
done

echo "Oracle Database disponível! Executando scripts de inicialização..."

# Executar script de inicialização
sqlplus system/OraclePassword123@//localhost:1521/XE @/opt/oracle/scripts/startup/init-db.sql

echo "Scripts de inicialização executados com sucesso!"

# Manter o container rodando
tail -f /dev/null