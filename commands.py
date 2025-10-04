# -*- coding: utf-8 -*-
from datetime import datetime
import re

# --- Função Auxiliar para criar links clicáveis ---

def linkify(text):
    """
    Encontra URLs no texto e os envolve com a tag <a> para torná-los clicáveis.
    Funciona com http, https e domínios comuns como github.com.
    """
    # Expressão regular para encontrar URLs
    pattern = r'((?:https?://|www\.|t\.me/|github\.com/)[^\s]+[a-zA-Z0-9/])'
    
    def add_protocol(match):
        url = match.group(1)
        # Garante que a URL tenha um protocolo para o link funcionar corretamente
        if not url.startswith(('http', 't.me')):
            return f'<a href="https://{url}" target="_blank">{url}</a>'
        return f'<a href="{url}" target="_blank">{url}</a>'

    return re.sub(pattern, add_protocol, text)

# --- Função Principal de Roteamento de Comandos ---

def get_command_output(command_string, client_data=None, headers=None):
    """
    Função principal que recebe a string do comando e a roteia para a função correta.
    """
    parts = command_string.split()
    command = parts[0]
    args = parts[1:]

    command_function = COMMANDS.get(command, command_not_found)
    
    if command == 'welcome' and client_data and headers:
        return command_function(args, client_data, headers)
    else:
        return command_function(args)

def command_not_found(args):
    """Retorno para comandos inválidos."""
    return "Comando não encontrado. Digite 'comandos' para ver a lista de opções."

# --- Funções de Saída para cada Comando ---

def show_welcome(args, client_data, headers):
    """Gera a mensagem de boas-vindas no estilo neofetch."""
    os, browser = parse_user_agent(headers.get('user_agent', ''))
    resolution = client_data.get('resolution', 'N/A')
    language = headers.get('language', 'N/A').split(',')[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    neofetch_output = f"""
    <span style="color: var(--purple);">joaoclaudino@terminal</span>
    --------------------
    <span style="color: var(--cyan);">OS:</span>         {os}
    <span style="color: var(--cyan);">Browser:</span>    {browser}
    <span style="color: var(--cyan);">Resolution:</span> {resolution}
    <span style="color: var(--cyan);">Language:</span>   {language}
    <span style="color: var(--cyan);">Date:</span>       {now}
    """
    return neofetch_output.strip()

def show_comandos(args):
    """Mostra todos os comandos disponíveis."""
    available_commands = " ".join([cmd for cmd in COMMANDS if cmd != 'welcome'])
    return f"Comandos disponíveis:\n{available_commands}"

def show_contato(args):
    """Retorna suas informações de contato."""
    text = """
Informações de Contato:
-----------------------
- Email:    joaoclaudino@proton.me
- GitHub:   github.com/gottenw
- Telegram: t.me/joaonaithen

PS: Potencialmente te responderei mais rápido pelo Telegram ;)
    """
    return linkify(text)

def show_portfolio(args):
    """Retorna uma lista de projetos do portfólio."""
    text = """
Meus Projetos Principais:
-------------------------
1. Terminal Web Interativo (este projeto!)
   - Descrição: Um "portfólio" pessoal com a aparência de um terminal de desenvolvedor.
   - Tecnologias: Python, Flask, JavaScript, HTML/CSS.
   - Link: [Link para o Repo no GitHub]

2. Modelo preditivo em WebApp para Handicap Asiático no Futebol (Em desenvolvimento contínuo)
   - Descrição: Um bot que utiliza a API do Footystats e modelagem preditiva para gerar fairlines em partidas de liga.
   - Tecnologias: Python e Streamlit.
   - Link: https://ollo.onrender.com

3. API com dados históricos avançados de partidas de futebol (Em desenvolvimento)
   - Descrição: Uma API para devs e analistas com um banco de dados rico sobre futebol.
   - Tecnologias: Python, FastAPI, Supabase e Uvicorn.
   - Link: contate-me.
    """
    return linkify(text)

def show_sobremim(args):
    """Retorna uma breve biografia."""
    return """
Olá, sou João Claudino! Alguns podem me conhecer como Naithèn.

Este terminal foi criado para ser uma forma legal de me apresentar.

Aposto em ligas de futebol de baixo escalão;
Faço parte do SPM (@spmbet);
Escrevo textos em formato de blog para o Vienna (@viennagroup);
Estou desenvolvendo uma API para dados avançados do esporte bretão - futebol;
Sou graduando em Licenciatura em História na UFAL. 

Gosto muito de probabilidades, ciência de dados e programação. Estou disposto á colaborar em projetos que envolvam desde criar simples bots, até automatizar modelos preditivos e/ou fazer um serviço de parceria sobre apostas.

Entre em contato! ;)
    """

def show_betting(args):
    """Detalha a proposta de parceria para apostas."""
    text = """
Em caso de interesse em uma parceria para um serviço de apostas, vai algumas informações úteis:

Tenho um registro de 446 apostas e 14.60% de yield.
Meu p-value é cerca de 0.05%, isso significa que a chance de ter atingido um yield de 14.60% em 446 apostas por pura sorte é de apenas 0.05%. Uma porcentagem muito pequena de chance.

Mais informações como odd média, taxa de acerto, CLV médio e etc. você pode buscar em:
https://docs.google.com/spreadsheets/d/14B6X-VzrvK6KlY7KgGBYN85YUfH5FUtYxXPzTaOkpC4/edit?usp=sharing

Se tiver interesse de fechar uma parceria comigo, entre em contato.

PS: dados atualizados em 03 de Outubro de 2025.
    """
    return linkify(text)

def show_temas(args):
    """Gerencia os temas do terminal."""
    if len(args) == 2 and args[0] == 'set':
        theme_name = args[1]
        available_themes = ['dracula', 'nord', 'solarized']
        if theme_name in available_themes:
            return f"Tema alterado para '{theme_name}'."
        else:
            return f"Tema '{theme_name}' não encontrado. Use 'temas' para ver as opções."
    
    return """
Gerenciador de Temas:
---------------------
Use 'temas set <nome_do_tema>' para alterar a aparência do terminal.

Temas disponíveis:
- dracula
- nord
- solarized
    """

def show_musica(args):
    """Instruções para controlar a música."""
    return """
Controle de Música:
------------------
Use 'musica on' para tocar.
Use 'musica off' para pausar.

Você também pode usar o ícone de som no topo da janela.
"""

# --- Dicionário que Mapeia a String do Comando à sua Função ---

COMMANDS = {
    'welcome': show_welcome,
    'comandos': show_comandos,
    'contato': show_contato,
    'portfolio': show_portfolio,
    'sobremim': show_sobremim,
    'betting': show_betting,
    'temas': show_temas,
    'musica': show_musica,
}

