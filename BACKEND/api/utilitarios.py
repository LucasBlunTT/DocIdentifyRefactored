import cv2
import re
import pytesseract

LINHAS_PROCURADAS = {
    "nome": "2 e 1 NOME E SOBRENOME",
    "nome1": "— NOME",
    "data": "3 DATA, LOCAL E UF DE NASCIMENTO",
    "data1": "CPF DATA NASGIMENTO » o"
}

def caminho_tesseract():
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def tratar_imagem(imagem):
    
    imagem_documento = cv2.imread(imagem)

    # Converter a imagem colorida para escala de cinza
    cinza = cv2.cvtColor(imagem_documento, cv2.COLOR_BGR2GRAY)

    # Aplicar limiarização usando o método de Otsu
    limiar = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    umbral = cv2.adaptiveThreshold(limiar, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

    return umbral

def extrair_texto_documento(imagem):  

    umbral = tratar_imagem(imagem)
    config = "--psm 4"
    texto_extraido = pytesseract.image_to_string(umbral, config=config, lang="por")

    return texto_extraido

def buscar_cpf(texto):

    regex_cpf = r"\d{3}\s?\.\s?\d{3}\s?\.\s?\d{3}\s?\-\s?\d{2}"
    for linha in texto:
        cpf_cliente = re.findall(regex_cpf, linha)
        if len(cpf_cliente) > 0: #Verifica se existe o CPF
            return cpf_cliente
    else:
        return 'CPF não encontrado.'

def buscar_nome_primeira_habilitacao(imagem):

    nome_e_primeira_habilitacao = None

    texto_extraido = extrair_texto_documento(imagem)
    linhas = texto_extraido.split('\n')
    linhas = [linha for linha in linhas if linha]

    for linha in linhas:

        if (LINHAS_PROCURADAS["nome"]) in linha:
            indice = linhas.index(linha) + 1
            nome_e_primeira_habilitacao = linhas[indice].split('|')
            break
        elif LINHAS_PROCURADAS["nome1"] in linha:
            indice = linhas.index(linha) + 1
            nome_e_primeira_habilitacao = linhas[indice].split("| E")
            break

    return nome_e_primeira_habilitacao, linhas

def buscar_demais_dados(linhas):
    
    regex_data = r"\d{2}\/\d{2}\/\d{4}"
    data_nascimento = None
    cidade = None
    estado = None

    for linha in linhas:
        if LINHAS_PROCURADAS["data"] in linha:
            indice_data = linhas.index(linha) + 1
            dados = linhas[indice_data].split(",")
            data_nascimento = re.findall(regex_data, dados[0])
            cidade = str(dados[1]).replace("|", "")
            estado = str(dados[2]).replace("|", "")
            break
        
    for linha in linhas:
        if LINHAS_PROCURADAS["data1"] in linha:
            indice_data = linhas.index(linha) + 1
            dados = linhas[indice_data].split(",")
            data_nascimento = re.findall(regex_data, dados[0])
            break

    return data_nascimento, estado, cidade

def extrair_dados_documento(caminho):

    #Carrega o caminho do tesseract
    caminho_tesseract()
    
    #A função buscar_nome_primeira_habilitacao irá retornar o nome e também as linhas,
    #Para que não tenhamos que passar o OCR novamente na imagem
    nome_e_primeira_habilitacao, linhas = buscar_nome_primeira_habilitacao(caminho)

    data_nascimento, estado, cidade = buscar_demais_dados(linhas)

    cpf_cliente = buscar_cpf(linhas)

    return {
        'nome': nome_e_primeira_habilitacao[0].strip("|") if (nome_e_primeira_habilitacao is not None) else '',
        'primeiraHabilitacao': nome_e_primeira_habilitacao[1] if (nome_e_primeira_habilitacao is not None) else '',
        'cpf': cpf_cliente[0],
        'nascimento': data_nascimento[0] if (data_nascimento is not None) else 'Carteira sem Data de Nascimento',
        'cidadeNascimento': cidade if (cidade is not None) else 'Cidade não encontrada',
        'estadoNascimento': estado if (estado is not None) else 'Estado não encontrado',
        #'dtVencimentoCnh': datas[1] if dt_venc == None else dt_venc
    }