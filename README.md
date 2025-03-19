# Vocabulário da REGIS

## Como rodar:
 - Instalar os pacotes que estão no ``requirements.txt``
 - Rodar o arquivo main.py, da seguinte forma:

``python main.py --input <diretorio_arquivos_xml> --output <diretorio_arquivos_json>``

 - Este código irá popular o diretório informado em ``--output`` com os arquivos json correspondentes a cada documento xml no diretório informado em ``input``
 - Ele vai calcular o percentual de palavras únicas em cada documento e vai salvar o resultado no arquivo ``percent_palavras_unicas.txt``
