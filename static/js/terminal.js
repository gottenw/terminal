// static/js/terminal.js

document.addEventListener('DOMContentLoaded', () => {
    const outputContainer = document.getElementById('output-container');
    const userInput = document.getElementById('user-input');
    const terminal = document.getElementById('terminal');

    const prompt = '> ';
    const initialCommand = 'comandos';

    // Foca no input assim que a página carrega
    userInput.focus();
    terminal.addEventListener('click', () => userInput.focus());

    // Função para adicionar uma nova linha ao terminal
    function addLine(text, isCommand = false) {
        const line = document.createElement('div');
        line.className = 'output-line';

        if (isCommand) {
            line.innerHTML = `<span class="prompt">${prompt}</span><span class="command-text">${text}</span>`;
        } else {
            // Usar <pre> para manter a formatação do texto de resposta
            const pre = document.createElement('pre');
            pre.textContent = text;
            line.appendChild(pre);
        }
        outputContainer.appendChild(line);
        // Rola a tela para a parte de baixo
        terminal.scrollTop = terminal.scrollHeight;
    }

    // Função que simula o efeito de digitação
    function typeEffect(text, onComplete) {
        let i = 0;
        userInput.disabled = true; // Desabilita o input durante a digitação
        const interval = setInterval(() => {
            if (i < text.length) {
                userInput.value += text[i];
                i++;
            } else {
                clearInterval(interval);
                userInput.disabled = false;
                userInput.focus();
                if (onComplete) {
                    onComplete();
                }
            }
        }, 100); // Velocidade da digitação (em milissegundos)
    }

    // Função para enviar o comando para o back-end
    async function executeCommand(command) {
        if (command.trim() === '') return;

        addLine(command, true); // Mostra o comando digitado
        userInput.value = ''; // Limpa o input

        // Comando 'limpar' ou 'clear' é tratado no front-end
        if (command.toLowerCase() === 'limpar' || command.toLowerCase() === 'clear') {
            outputContainer.innerHTML = '';
            return;
        }

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            addLine(data.output);
        } catch (error) {
            console.error('Error executing command:', error);
            addLine('Erro ao conectar com o servidor.');
        }
    }

    // Listener para o evento de pressionar 'Enter'
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Impede o comportamento padrão do Enter
            executeCommand(userInput.value);
        }
    });

    // Função de inicialização
    function init() {
        const welcomeMessage = "Bem-vindo ao meu terminal!\nIniciando sistema...";
        addLine(welcomeMessage);
        
        // Simula a digitação e execução do comando inicial
        setTimeout(() => {
            typeEffect(initialCommand, () => {
                setTimeout(() => {
                    executeCommand(initialCommand);
                }, 300); // Pequeno delay antes de executar
            });
        }, 1000); // Delay para iniciar a digitação
    }

    // Inicia o terminal
    init();
});