"""
gerar_dados_manutencao.py
Gera dataset fictício de ordens de manutencao de equipamentos.
Execute para criar os arquivos CSV que serao importados no Power BI.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

os.makedirs("dados", exist_ok=True)
random.seed(42)
np.random.seed(42)

# -- Configuracoes -------------------------------------------------------------
N_ORDENS = 600

EQUIPAMENTOS = {
    "ELV-001": "Elevador Social Bloco A",
    "ELV-002": "Elevador Social Bloco B",
    "ELV-003": "Elevador de Carga",
    "ESC-001": "Escada Rolante Terminal 1",
    "ESC-002": "Escada Rolante Terminal 2",
    "PLT-001": "Plataforma Elevatória P1",
    "PLT-002": "Plataforma Elevatória P2",
}
TIPOS = ["Manutenção Preventiva", "Manutenção Corretiva", "Inspeção", "Modernização"]
TECNICOS = {
    "T01": "Carlos Silva",
    "T02": "Ana Souza",
    "T03": "Roberto Lima",
    "T04": "Fernanda Costa",
    "T05": "Lucas Mendes",
}
CLIENTES = [
    "Condomínio Residencial Aurora",
    "Shopping Center Plaza",
    "Hospital São Lucas",
    "Aeroporto Regional",
    "Edifício Comercial Centro",
    "Universidade Federal",
    "Hotel Grand Palace",
]
FALHAS = [
    "Cabo de aço desgastado",
    "Porta com falha no sensor",
    "Motor com superaquecimento",
    "Botão de chamada inoperante",
    "Nível de óleo baixo",
    "Freio com desgaste",
    "Sistema elétrico com falha",
    None, None, None,  # maioria sem falha específica
]
STATUS = ["Concluída", "Concluída", "Concluída", "Em andamento", "Aguardando peça"]
DATA_INICIO = datetime(2024, 1, 1)
DATA_FIM = datetime(2024, 12, 31)

# -- Geracao das ordens --------------------------------------------------------
ordens = []

for i in range(1, N_ORDENS + 1):
    tipo = random.choices(TIPOS, weights=[40, 35, 20, 5])[0]
    equip_cod = random.choice(list(EQUIPAMENTOS.keys()))
    tecnico_id = random.choice(list(TECNICOS.keys()))
    cliente = random.choice(CLIENTES)
    status = random.choice(STATUS)

    abertura = DATA_INICIO + timedelta(days=random.randint(0, (DATA_FIM - DATA_INICIO).days))

    # Tempo de execucao varia por tipo
    tempo_base = {"Manutenção Preventiva": 4, "Manutenção Corretiva": 8,
                  "Inspeção": 2, "Modernização": 24}
    tempo_exec = round(tempo_base[tipo] + random.uniform(-1, 4), 1)

    # Prazo SLA em horas
    sla = {"Manutenção Preventiva": 6, "Manutenção Corretiva": 12,
           "Inspeção": 4, "Modernização": 48}
    sla_horas = sla[tipo]
    dentro_sla = tempo_exec <= sla_horas

    # Custo da ordem
    custo_base = {"Manutenção Preventiva": 350, "Manutenção Corretiva": 800,
                  "Inspeção": 150, "Modernização": 5000}
    custo = round(custo_base[tipo] * random.uniform(0.7, 1.5), 2)

    # Satisfacao do cliente (1-5)
    satisfacao = random.choices([1, 2, 3, 4, 5], weights=[5, 8, 15, 40, 32])[0] if status == "Concluída" else None

    # Reincidencia
    reincidente = random.random() < (0.25 if tipo == "Manutenção Corretiva" else 0.08)

    falha = random.choice(FALHAS) if tipo == "Manutenção Corretiva" else None

    ordens.append({
        "id_ordem": f"OS{i:05d}",
        "data_abertura": abertura.strftime("%Y-%m-%d"),
        "mes": abertura.strftime("%Y-%m"),
        "tipo_manutencao": tipo,
        "cod_equipamento": equip_cod,
        "equipamento": EQUIPAMENTOS[equip_cod],
        "cliente": cliente,
        "tecnico_id": tecnico_id,
        "tecnico": TECNICOS[tecnico_id],
        "status": status,
        "tempo_execucao_h": tempo_exec,
        "sla_horas": sla_horas,
        "dentro_sla": dentro_sla,
        "custo_rs": custo,
        "satisfacao": satisfacao,
        "reincidente": reincidente,
        "falha_identificada": falha,
    })

df = pd.DataFrame(ordens)
df.to_csv("dados/ordens_manutencao.csv", index=False, encoding="utf-8-sig")

print(f"Dataset gerado: {N_ORDENS} ordens de manutenção")
print(f"Arquivo: dados/ordens_manutencao.csv")
print(f"\n Resumo:")
print(f"Tipos: {df['tipo_manutencao'].value_counts().to_dict()}")
print(f"Status: {df['status'].value_counts().to_dict()}")
print(f"SLA cumprido: {df['dentro_sla'].mean()*100:.1f}%")
print(f"Custo total: R$ {df['custo_rs'].sum():,.2f}")
