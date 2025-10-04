# -*- coding: utf-8 -*-
from datetime import datetime

# --- Funções Auxiliares para o "Neofetch" ---

def parse_user_agent(user_agent):
    """Analisa a string User-Agent para extrair o OS e o Navegador de forma simples."""
    os = "Desconhecido"
    browser = "Desconhecido"

    # Detecção do OS
    if "Windows" in user_agent:
        os = "Windows"
    elif "Macintosh" in user_agent:
        os = "macOS"
    elif "Linux" in user_agent:
        os = "Linux"
    elif "Android" in user_agent:
        os = "Android"
    elif "iPhone" in user_agent or "iPad" in user_agent:
        os = "iOS"

    # Detecção do Navegador
    if "Chrome" in user_agent and "Edg" not in user_agent:
        browser = "Chrome"
    elif "Firefox" in user_agent:
        browser = "Firefox"
    elif "Safari" in user_agent and "Chrome" not in user_agent:
        browser = "Safari"
    elif "Edg" in user_agent:
        browser = "Edge"
    
    return os, browser

# --- Função Principal de Roteamento de Comandos ---

def get_command_output(command_string, client_data=None, headers=None):
    """
    Função principal que recebe a string do comando e a roteia para a função correta.
    """
    parts = command_string.split()
    command = parts[0]
    args = parts[1:]

    # Passa os dados do cliente para a função do comando, se ela aceitar
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
    
    # Pega o horário atual do servidor
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
    # Exclui o comando 'welcome' da lista pública
    available_commands = " ".join([cmd for cmd in COMMANDS if cmd != 'welcome'])
    return f"Comandos disponíveis:\n{available_commands}"

def show_contato(args):
    """Retorna suas informações de contato."""
    return """
Informações de Contato:
-----------------------
- Email:    joaoclaudino@proton.me
- GitHub:   github.com/gottenw
- Telegram: t.me/joaonaithen

PS: Potencialmente te responderei mais rápido pelo Telegram ;)
    """

def show_portfolio(args):
    """Retorna uma lista de projetos do portfólio."""
    return """
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
    return """
Em caso de interesse em uma parceria para um serviço de apostas, vai algumas informações úteis:

Tenho um registro de 446 apostas e 14.60% de yield.
Meu p-value é cerca de 0.05%, isso significa que a chance de ter atingido um yield de 14.60% em 446 apostas por pura sorte é de apoenas 0.05%. Uma porcentagem muito pequena de chance.

Mais informações como odd média, taxa de acerto, CLV médio e etc. você pode buscar em:
https://docs.google.com/spreadsheets/d/14B6X-VzrvK6KlY7KgGBYN85YUfH5FUtYxXPzTaOkpC4/edit?usp=sharing

Se tiver interesse de fechar uma parceria comigo, entre em contato.

PS: dados atualizados até 03/out/2025.
    """

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

# --- Dicionário que Mapeia a String do Comando à sua Função ---

COMMANDS = {
    'welcome': show_welcome,  # Comando "secreto" para a tela inicial
    'comandos': show_comandos,
    'contato': show_contato,
    'portfolio': show_portfolio,
    'sobremim': show_sobremim,
    'betting': show_betting,
    'temas': show_temas,
}