from utilitarios import extrair_dados_documento
from flask import jsonify

def main(caminho):

    # Chamar a função para processar a imagem do documento
    dados_documento = extrair_dados_documento(caminho)
    
    return jsonify(dados_documento)

if __name__ == '__main__':
    main()