# Comunicação de Dados com MLT-3 e Criptografia

Este projeto é uma aplicação gráfica (GUI) feita em Python que simula a transmissão de mensagens utilizando criptografia (Cifra de Vigenère) e codificação de linha MLT-3, com envio e recepção de dados via rede (TCP).

## Funcionalidades

- **Criptografia:** Utiliza a cifra de Vigenère para proteger a mensagem.
- **Conversão Binária:** Transforma o texto criptografado em binário.
- **Codificação MLT-3:** Aplica o algoritmo MLT-3 para simular transmissão física.
- **Transmissão em Rede:** Envia o sinal codificado via TCP (pode ser cliente ou servidor).
- **Visualização:** Exibe todas as etapas do processo e gráficos das formas de onda MLT-3.
- **Recepção e Decodificação:** Recebe, decodifica e descriptografa a mensagem, mostrando o resultado final.

## Como executar

1. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

2. Execute o programa:
   ```sh
   python main.py
   ```

3. Configure como **Servidor** ou **Cliente** na interface, conecte e envie mensagens!

## Estrutura dos Arquivos

- [`main.py`](main.py): Interface gráfica e lógica principal.
- [`crypto.py`](crypto.py): Funções de criptografia e conversão binária.
- [`mlt3.py`](mlt3.py): Algoritmos de codificação/decodificação MLT-3 e plotagem.
- [`network.py`](network.py): Gerenciamento de conexão de rede TCP.

## Observações

- O `tkinter` já vem com o Python padrão.
- Para comunicação, execute uma instância como servidor e outra como cliente.
- O projeto suporta caracteres acentuados e ASCII estendido.