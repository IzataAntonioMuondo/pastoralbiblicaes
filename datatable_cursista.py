import spacy

# Carregar o modelo de linguagem em português
nlp = spacy.load("pt_core_news_sm")

# Função para gerar o texto da atividade
def gerar_texto_atividade(info):
    # Extrair informações
    nome_atividade = info["nome_atividade"]
    data_inicio = info["data_inicio"]
    hora_inicio = info["hora_inicio"]
    data_termino = info["data_termino"]
    hora_termino = info["hora_termino"]
    local = info["local"]
    status = info["status"]
    num_participantes = info["num_participantes"]

    # Criar o texto usando SpaCy
    doc = nlp(f"A atividade '{nome_atividade}' está marcada para ocorrer no dia {data_inicio} às {hora_inicio}. "
              f"Irá terminar no dia {data_termino} às {hora_termino} no local {local}. "
              f"O status atual da atividade é '{status}' e está prevista a participação de {num_participantes} participantes.")

    # Retornar o texto gerado
    return doc.text

# Informações da atividade (substitua com suas próprias informações)
info_atividade = {
    "nome_atividade": "Reunião Mensal",
    "data_inicio": "2023-09-25",
    "hora_inicio": "14:00",
    "data_termino": "2023-09-25",
    "hora_termino": "16:00",
    "local": "Sala de Conferências",
    "status": "Confirmada",
    "num_participantes": 20
}

# Gerar e imprimir o texto da atividade
texto_atividade = gerar_texto_atividade(info_atividade)
print(texto_atividade)
