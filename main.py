import argparse

import xmltojson
import vocabulario

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Conversor de XML para JSON')
    parser.add_argument('--input',
                        type=str,
                        default='input/',
                        help='path to input directory')

    parser.add_argument('--output',
                        type=str,
                        default='output/',
                        help='path to output directory')
    args = parser.parse_args()

    xmltojson.converte_xml_json(args)

    vocabulario.montar_vocabulario(args.output)

    arquivo_vocabulario = "vocabulario.json"
    vocabulario.percentual_palavras_unicas(args.output, arquivo_vocabulario)