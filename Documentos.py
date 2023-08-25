import cv2
import pytesseract
import re

# Definir o caminho para o executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def mostrar_imagem(imagem, titulo='Minha Imagem'):
    # Função para redimensionar e mostrar uma imagem em uma janela
    largura_desejada = 800
    altura_desejada = 600

    # Redimensionar a imagem para o tamanho desejado
    imagem_redimensionada = cv2.resize(imagem, (largura_desejada, altura_desejada))

    # Mostrar a imagem redimensionada em uma janela
    cv2.imshow(titulo, imagem_redimensionada)

    # Esperar por uma tecla e depois fechar a janela
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def filtrar_data_cpf(texto):
    # Regex para pegar todas as datas
    r_data = r"\d{2}\/\d{2}\/\d{4}"
    datas = re.findall(r_data, texto)
    if(len(datas) == 4):
        dt_venc = datas[-1]
    else: 
        dt_venc = None


    # Regex para pegar todos os CPFs
    r_cpf = r"\d{3}\s?\.\s?\d{3}\s?\.\s?\d{3}\s?\-\s?\d{2}"
    cpf_cliente = re.findall(r_cpf, texto)
    
    # Formatar CPF removendo caracteres extras
    cpf_cliente = ''.join(cpf_cliente).replace(" ", "").replace(".", "").replace("-", "")

    return datas, cpf_cliente, dt_venc

def extrair_nome(texto):
    # Utilizar expressão regular para buscar padrão de nome
    padrao_nome = r'\|\s*([A-Z\s]+)\s*\|'
    match = re.search(padrao_nome, texto)

    if match:
        nome_completo = match.group(1)
        return nome_completo.strip()

def extrair_dados_documento(imagem):
    # Carregar a imagem do documento
    imagem_documento = cv2.imread(imagem)

    # Converter a imagem colorida para escala de cinza
    cinza = cv2.cvtColor(imagem_documento, cv2.COLOR_BGR2GRAY)
    mostrar_imagem(cinza, titulo='Imagem em Escala de Cinza')

    # Aplicar limiarização usando o método de Otsu
    limiar = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    mostrar_imagem(limiar, titulo='Imagem apos Limiarizacao de Otsu')

    # Aplicar limiarização adaptativa usando o método Gaussiano
    umbral = cv2.adaptiveThreshold(limiar, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)
    mostrar_imagem(umbral, titulo='Imagem após Limiarizacao Adaptativa')

    # Realizar OCR na imagem para extrair texto
    config = "--psm 4"
    texto_extraido = pytesseract.image_to_string(umbral, config=config, lang="por")
    print(texto_extraido)

    datas, cpf_cliente, dt_venc = filtrar_data_cpf(texto_extraido)
    nome = extrair_nome(texto_extraido)

    return {
        'nome': nome,
        'cpf': cpf_cliente,
        'nascimento': datas[0] if dt_venc == None else 'Carteira sem Data de Nascimento',
        'dtVencimentoCnh': datas[1] if dt_venc == None else dt_venc
    }

#path do caminho da imagem
imagem_path = ".//images//cnh.jpg"
#imagem_path = ".//images//cnh2.jpg"
#imagem_path = ".//images//cnh3.jpeg"

# Chamar a função para processar a imagem do documento
dados_documento = extrair_dados_documento(imagem_path)

print(dados_documento)
