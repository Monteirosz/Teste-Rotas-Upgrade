import regex as re
from datetime import datetime
from flask import Flask, request, jsonify, session
from libs.banco import *

app = Flask(__name__)
app.secret_key = 'f1e1f5e3524301435c10ffe339a3ae481aa31bda73b6ae78f721729cfab5a58b'

hora = {} #Armazenar o que tiver na variável em um dicionário

@app.route('/cadastro', methods=['POST']) #Rota de cadastro, POST para enviar informações
def rota_cadastro():
    data = request.get_json() #Extrai os dados em formato JSON
    user = data.get('usuario') #Dado extraído
    senha = data.get('senha')
    email = data.get('email')
    telefone = data.get('telefone')

    if not all([user, senha, email, telefone]):
        return jsonify({'erro': 'Você precisa preencher todos os campos'}) #Verifica se todos os itens da lista são "True"

    caracter_especial = re.search(r"[!@#$%&*,.?]", senha) #Verificando se tem algum caracter especial na senha
    caracter_letra = re.search(r"[A-Z]", senha) #Verificando se tem alguma letra maiúscula na senha
    caracter_email = re.search(r"\w+@\w+\.\w+", email) #Verificação de @ e . para email
    caracter_telefone = re.fullmatch(r"\(?\d{2}\)?\s?9\d{4}-?\d{4}", telefone) #Verificação de todos os caracters necessários para número de telefone

    if not caracter_email:
        return jsonify({'erro': 'Email inválido. Tente usar: exemplo@email.com'})
    
    if not caracter_telefone:
        return jsonify({'erro': 'Telefone inválido. Tente usar: (27) 99999-9999'})
    
    if caracter_especial and caracter_letra and caracter_email and caracter_telefone:
        inserir_usuario(user, senha, email, telefone)
        return jsonify({'mensagem': 'Usuário cadastrado com sucesso'})
    
    else:
        return jsonify({
            'erro': 'Senha precisa conter pelo menos um caracter especial (Ex: #@!) e uma letra MAIÚSCULA.'
        })
    

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('usuario')
    senha = data.get('senha')

    if not all([user, senha]):
        return jsonify({'erro': 'Usuário e senha são obrigatórios'})

    if validar_login(user, senha):
        session['usuario'] = user #Colocando o usuário dentro de uma session (cookies)
        hora_atual = datetime.datetime.now() #Informando a data de AGORA
        hora[user] = {'login': hora_atual, 'logout': None} #Para cada usuário logado, aparece a hora de login
        return jsonify({'mensagem': f'Seja bem-vindo(a) {user}!', 'login': hora_atual.strftime("%H:%M:%S")})
    else:
        return jsonify({'erro': 'Usuário ou senha inválidos'})
    
@app.route('/deslogar', methods=['POST'])
def desconectar():
    if 'usuario' not in session: #Se não houver nenhum usuário dentro da session aparecer a mensagem de erro
        return jsonify({'erro': 'Nenhum usuário está logado'})

    user = session.pop('usuario') #Remove e retorna o valor associado
    hora_atual = datetime.datetime.now()

    if user in hora: #Para cada usuário regitrar a hora de saída
        hora[user]['logout'] = hora_atual
    else:
        hora[user] = {'logout': hora_atual}

    return jsonify({'mensagem': f'Usuário {user} deslogado com sucesso!', 'logout': hora_atual.strftime("%H:%M:%S")})
    
@app.route('/users', methods=['GET'])
def tabela():
    dados = view_tabela()
    
    usuarios = []
    for user, senha, email, telefone in dados:
        sessao = hora.get(user, {})
        login = sessao.get('login')
        logout = sessao.get('logout')

        usuarios.append({
            'usuario': user,
            'senha': senha,
            'email': email,
            'telefone': telefone,
            'login': login.strftime('%H:%M:%S'),
            'logout': logout.strftime('%H:%M:%S'),
            'tempo_sessao': str(logout - login)
        })

    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(debug=True, port=51153)