from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config['UPLOADED_FOLDER'] = 'BACKEND/static/images'

@app.route('/upload', methods=['POST'])
def upload():
    try:      
        if 'image' not in request.files:
            mensagem = {"mensagem": "Erro ao enviar a imagem.", "status": 400}
            return jsonify(mensagem)
        
        file = request.files['image']
        if file.filename == '':
            mensagem = {"mensagem": "Nenhum arquivo foi selecionado.", "status": 400}
            return jsonify(mensagem)    
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOADED_FOLDER'], filename))
        mensagem = {"mensagem": "Imagem salva com sucesso.", "status": 200}

    except Exception as e:
        mensagem = {"mensagem": "Erro ao salvar a imagem", "log": str(e), "status": 400}
    return jsonify(mensagem)


    
if __name__ == '__main__':
    app.run()