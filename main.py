import regex as re
from flask import Flask, request, jsonify
from libs.banco import *

app = Flask(__name__)

@app.route('/cadastro', methods=['POST'])
def rota_cadastro():
    data = request.get_json()
    user = data.get('usuario')
    senha = data.get('senha')
    email = data.get('email')
    telefone = data.get('telefone')

    if not all([user, senha, email, telefone]):
        return jsonify({'erro': 'Você precisa preencher todos os campos'})

    caracter_especial = re.search(r"[!@#$%&*,.?]", senha)
    caracter_letra = re.search(r"[A-Z]", senha)
    caracter_email = re.search(r"\w+@\w+\.\w+", email)

    if not caracter_email:
        return jsonify({'erro': 'Email inválido. Tente usar: exemplo@email.com'})
    
    if caracter_especial and caracter_letra and caracter_email:
        return jsonify({'mensagem': 'Usuário cadastrado com sucesso'})
    
    else:
        return jsonify({
            'erro': 'Senha precisa conter pelo menos um caracter especial (Ex: #@!) e uma letra MAIÚSCULA.'
        })

@app.route('/users', methods=['GET'])
def view_users():
    return jsonify(view_tabela())

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('usuario')
    senha = data.get('senha')

    if not all([user, senha]):
        return jsonify({'erro': 'Usuário e senha são obrigatórios'})

    if validar_login(user, senha):
        return jsonify({'mensagem': 'Seja bem-vindo(a)!'})
    else:
        return jsonify({'erro': 'Usuário ou senha inválidos'})


if __name__ == '__main__':
    app.run(debug=True, port=51153)