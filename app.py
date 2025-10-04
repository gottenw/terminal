# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, request
import commands  # Importa nosso módulo de comandos customizado

# Inicializa a aplicação Flask
app = Flask(__name__)

@app.route('/')
def index():
    """
    Rota principal que renderiza a página do terminal (index.html).
    """
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute_command():
    """
    Endpoint da API que recebe um comando via POST, processa-o
    usando o módulo 'commands' e retorna a saída em formato JSON.
    """
    data = request.json
    command_string = data.get('command', '').lower().strip()
    
    # Recebe os dados do cliente (para o neofetch) e os headers da requisição
    client_data = data.get('client_data', {})
    headers = {
        'user_agent': request.headers.get('User-Agent'),
        'language': request.headers.get('Accept-Language')
    }

    if not command_string:
        return jsonify({'output': ''})

    # Obtém a saída do comando do nosso módulo, passando os dados do cliente
    output = commands.get_command_output(command_string, client_data, headers)

    return jsonify({'output': output})

if __name__ == '__main__':
    # Roda a aplicação em modo de debug
    app.run(debug=True)