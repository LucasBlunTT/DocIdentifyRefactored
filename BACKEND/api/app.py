from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from main import main


app = Flask(__name__)
CORS(app)

app.config['UPLOADED_FOLDER'] = 'BACKEND/static/images/'

@app.route('/upload', methods=['POST'])
def upload():
    try:      
        if 'image' not in request.files:
            mensagem = {"mensagem": "Erro ao enviar a imagem.", "status": 400}
            return jsonify(mensagem)
        
        arquivo = request.files['image']
        if arquivo.filename == '':
            mensagem = {"mensagem": "Arquivo inválido ou nenhum arquivo foi selecionado.", "status": 400}
            return jsonify(mensagem)    
        
        #Pega o nome do arquivo e salva na pasta configurada
        nome_arquivo = secure_filename(arquivo.filename)
        caminho_arquivo = os.path.join(app.config['UPLOADED_FOLDER'], nome_arquivo)
        arquivo.save(caminho_arquivo)

        #Caminho para o arquivo
        dados_documento = main(caminho_arquivo).json
        #dados_documento = dados_documento.json   
        return jsonify(dados_documento) 
        
    except Exception as e:
        app.logger.error(f"Erro durante o upload: {str(e)}")
        mensagem = {"mensagem": "Erro ao salvar ou processar a imagem", "log": str(e), "status": 500}
        return jsonify(mensagem) 
        
 
if __name__ == '__main__':
    app.run()