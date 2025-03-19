import json
import nltk
import numpy as np
import os

from tqdm import tqdm
from util import Contador
from xmltojson import get_lista_arquivos

nltk.download('punkt')
nltk.download('punkt_tab')

DIRETORIO_CONTAGENS = "contagens"

def processar_arquivo(file):
    contagens = Contador()
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        texto = data.get('text', '')
        tokens = nltk.word_tokenize(texto, language='portuguese')
        tokens = np.array([token.lower() for token in tokens if token.isalpha()])

        contagens.incrementar_todos(tokens)

    # Salva as contagens em um arquivo
    contagens_ordenado = {chave: contagens[chave] for chave in sorted(contagens)}
    file = file.split("\\")[1]
    with open(f"{DIRETORIO_CONTAGENS}/{file}", "w", encoding='utf-8') as json_file:
        json.dump(contagens_ordenado, json_file, indent=4)

    return contagens

def montar_vocabulario(diretorio_entrada):
    contagem_geral = Contador()
    termo_docs = {}

    if not os.path.exists(DIRETORIO_CONTAGENS):
        os.mkdir(DIRETORIO_CONTAGENS)

    arquivos = get_lista_arquivos(diretorio_entrada, "json")
    for arquivo in tqdm(arquivos):
        c = processar_arquivo(arquivo)
        contagem_geral += c
        for chave in c:
            if chave in termo_docs:
                termo_docs[chave].append(arquivo)
            else:
                termo_docs[chave] = [arquivo]

    # DESCOMENTAR AQUI PARA SALVAR O VOCABULÁRIO GERAL E A LISTA DE TERMOS POR DOC
    '''
    contagens_ordenado = {chave: contagem_geral[chave] for chave in sorted(contagem_geral)}
    with open(f"vocabulario.json", "w", encoding='utf-8') as json_file:
        json.dump(contagens_ordenado, json_file, indent=4)

    docs_ordenado = {chave: termo_docs[chave] for chave in sorted(termo_docs)}
    with open(f"vocabulario_docs.json", "w", encoding='utf-8') as json_file:
        json.dump(docs_ordenado, json_file, indent=4)
    '''


def percentual_palavras_unicas(diretorio_colecao, arquivo_vocabulario):
    with open(arquivo_vocabulario, 'r', encoding='utf-8') as arquivo:
        contador_palavras = json.load(arquivo)

    arquivos = get_lista_arquivos(diretorio_colecao, "json")

    saida = {}
    for arquivo in tqdm(arquivos):
        arquivo = arquivo.split("\\")[1]
        with open(f"{DIRETORIO_CONTAGENS}/{arquivo}", 'r', encoding='utf-8') as json_file:
            c = json.load(json_file)

        contador = 0
        for valor in c:
            if valor not in contador_palavras or contador_palavras[valor] == 1:
                print(f'{valor} palavra unica | contagem no doc: {c[valor]}')
                contador += 1

        print(f"{contador} palavras únicas no arquivo {arquivo}. Proporção de {contador / len(c)}%")
        if len(c) != 0:
            porc = contador / len(c)

        saida[arquivo] = porc

    with open("percent_palavras_unicas.txt", 'w', encoding='utf-8') as arquivo:
        for entry in sorted(saida, key=saida.get, reverse=True):
            arquivo.write(f"{entry}\t{saida[entry]:.3f}\n")
