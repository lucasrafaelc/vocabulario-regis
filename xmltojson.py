
import json
import os

from tqdm import tqdm
from xml.dom import minidom

def get_lista_arquivos(path, extensao):
    caminhos = [os.path.join(path, nome) for nome in os.listdir(path)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq) and arq.lower().endswith(f".{extensao}")]
    return arquivos

def converte_xml_json(args):
    lista_arquivos = get_lista_arquivos(args.input, "xml")
    for arquivo in tqdm(lista_arquivos):
        file = minidom.parse(arquivo)

        dados = {}
        campos = file.getElementsByTagName('field')
        for campo in campos:
            dados[campo.attributes['name'].value] = campo.firstChild.data

        texto_doc = ""
        campos_texto = file.getElementsByTagName("item")
        for campo in campos_texto:
            if campo.attributes['type'].value == "text" and campo.firstChild is not None:
                texto_doc += campo.firstChild.data + "\n"

        dados["text"] = texto_doc

        with open(os.path.join(args.output, dados['docid'] + ".json"), "w", encoding="utf-8") as saida:
            json.dump(dados, saida, indent=4)

