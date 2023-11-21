# Importar os módulos necessários
from utilitarios import extrair_dados_documento
from flask import jsonify

def main(caminho):
    # Definir o caminho para o executável do Tesseract OCR
    

    # Caminho da imagem
    #imagem_path = ".//BACKEND//data//images//cnh.jpg"  
    #caminho = ".//BACKEND//data//images//cnh2.jpeg"

    # Chamar a função para processar a imagem do documento
    dados_documento = extrair_dados_documento(caminho)

    #mostrar dados do documento
    
    return jsonify(dados_documento)

if __name__ == '__main__':
    main()