# main.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
# Importar as classes/funções dos outros módulos
from crypto import text_to_binary, binary_to_text, vigenere_encrypt, vigenere_decrypt
from mlt3 import encode_mlt3, decode_mlt3, plot_mlt3_signal
from network import NetworkManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Comunicação MLT-3 com Criptografia")
        self.root.geometry("1200x800")

        self.network_manager = None
        self.is_server = tk.BooleanVar()
        self.is_server.set(False) # Default para cliente
        self.network_connected = False
        self.last_sent_mlt3_signal = [] # Armazenar o último sinal MLT-3 enviado para plotagem

        self._create_widgets()

    def _create_widgets(self):
        # Frame de Configuração de Rede
        network_frame = ttk.LabelFrame(self.root, text="Configuração de Rede")
        network_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(network_frame, text="IP do Host:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.host_entry = ttk.Entry(network_frame, width=20)
        self.host_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.host_entry.insert(0, "127.0.0.1") # IP padrão

        ttk.Label(network_frame, text="Porta:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.port_entry = ttk.Entry(network_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=2, sticky="ew")
        self.port_entry.insert(0, "12345")

        ttk.Radiobutton(network_frame, text="Servidor", variable=self.is_server, value=True).grid(row=0, column=4, padx=5, pady=2)
        ttk.Radiobutton(network_frame, text="Cliente", variable=self.is_server, value=False).grid(row=0, column=5, padx=5, pady=2)

        self.connect_button = ttk.Button(network_frame, text="Conectar", command=self.toggle_connection)
        self.connect_button.grid(row=0, column=6, padx=5, pady=2)
        self.status_label = ttk.Label(network_frame, text="Status: Desconectado", foreground="red")
        self.status_label.grid(row=0, column=7, padx=5, pady=2, sticky="w")

        # Frame da Mensagem Original
        input_frame = ttk.LabelFrame(self.root, text="Mensagem Original")
        input_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(input_frame, text="Mensagem:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.message_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=60, height=5)
        self.message_input.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")
        self.message_input.insert(tk.END, "Olá, mundo! Este é um teste com acentos çÇãÃ.")

        ttk.Label(input_frame, text="Chave de Criptografia:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.key_entry = ttk.Entry(input_frame, width=30, show='*') # show='*' para esconder a chave
        self.key_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
        self.key_entry.insert(0, "SENHA")

        self.process_button = ttk.Button(input_frame, text="Processar e Enviar", command=self.process_and_send)
        self.process_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Notebook para exibir as etapas do processo e os gráficos
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=5, fill="both", expand=True)

        # Tab de Transmissão (Lado Remetente)
        transmit_frame = ttk.Frame(self.notebook)
        self.notebook.add(transmit_frame, text="Transmissão")
        self._create_transmit_widgets(transmit_frame)

        # Tab de Recepção (Lado Receptor)
        receive_frame = ttk.Frame(self.notebook)
        self.notebook.add(receive_frame, text="Recepção")
        self._create_receive_widgets(receive_frame)

    def _create_transmit_widgets(self, parent_frame):
        # Exibição das etapas de Transmissão
        ttk.Label(parent_frame, text="Mensagem Criptografada:").pack(padx=5, pady=2, anchor="w")
        self.encrypted_msg_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.encrypted_msg_display.pack(padx=5, pady=2, fill="x")

        ttk.Label(parent_frame, text="Mensagem em Binário:").pack(padx=5, pady=2, anchor="w")
        self.binary_msg_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.binary_msg_display.pack(padx=5, pady=2, fill="x")

        ttk.Label(parent_frame, text="Mensagem MLT-3 (codificada):").pack(padx=5, pady=2, anchor="w")
        self.mlt3_encoded_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.mlt3_encoded_display.pack(padx=5, pady=2, fill="x")

        # Gráfico MLT-3 (Transmissão)
        ttk.Label(parent_frame, text="Forma de Onda MLT-3 (Transmissão):").pack(padx=5, pady=5, anchor="w")
        self.fig_transmit, self.ax_transmit = plt.subplots(figsize=(8, 3))
        self.canvas_transmit = FigureCanvasTkAgg(self.fig_transmit, master=parent_frame)
        self.canvas_transmit_widget = self.canvas_transmit.get_tk_widget()
        self.canvas_transmit_widget.pack(fill="both", expand=True, padx=5, pady=5)

    def _create_receive_widgets(self, parent_frame):
        # Exibição das etapas de Recepção
        ttk.Label(parent_frame, text="Sinal MLT-3 Recebido (Decodificação):").pack(padx=5, pady=2, anchor="w")
        self.mlt3_received_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.mlt3_received_display.pack(padx=5, pady=2, fill="x")

        ttk.Label(parent_frame, text="Mensagem Binária Decodificada:").pack(padx=5, pady=2, anchor="w")
        self.binary_decoded_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.binary_decoded_display.pack(padx=5, pady=2, fill="x")

        ttk.Label(parent_frame, text="Mensagem Descriptografada:").pack(padx=5, pady=2, anchor="w")
        self.decrypted_msg_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.decrypted_msg_display.pack(padx=5, pady=2, fill="x")

        ttk.Label(parent_frame, text="Mensagem Original Reconhecida:").pack(padx=5, pady=2, anchor="w")
        self.final_msg_display = scrolledtext.ScrolledText(parent_frame, wrap=tk.WORD, height=3, state="disabled")
        self.final_msg_display.pack(padx=5, pady=2, fill="x")

        # Gráfico MLT-3 (Recepção)
        ttk.Label(parent_frame, text="Forma de Onda MLT-3 (Recepção):").pack(padx=5, pady=5, anchor="w")
        self.fig_receive, self.ax_receive = plt.subplots(figsize=(8, 3))
        self.canvas_receive = FigureCanvasTkAgg(self.fig_receive, master=parent_frame)
        self.canvas_receive_widget = self.canvas_receive.get_tk_widget()
        self.canvas_receive_widget.pack(fill="both", expand=True, padx=5, pady=5)

    def update_text_widget(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert(tk.END, text)
        widget.config(state="disabled")

    def toggle_connection(self):
        if self.network_connected:
            self.network_manager.close()
            self.network_manager = None
            self.network_connected = False
            self.connect_button.config(text="Conectar")
            self.status_label.config(text="Status: Desconectado", foreground="red")
        else:
            host = self.host_entry.get()
            port = int(self.port_entry.get())
            is_server_mode = self.is_server.get()

            try:
                self.network_manager = NetworkManager(host, port, is_server=is_server_mode,
                                                      on_receive_callback=self.handle_received_mlt3_signal)
                self.network_manager.start()
                self.network_connected = True
                self.connect_button.config(text="Desconectar")
                self.status_label.config(text="Status: Conectado", foreground="green")
            except Exception as e:
                messagebox.showerror("Erro de Conexão", f"Não foi possível conectar: {e}")
                self.network_manager = None
                self.network_connected = False

    def process_and_send(self):
        if not self.network_connected:
            messagebox.showwarning("Erro", "Por favor, conecte-se à rede primeiro.")
            return

        original_msg = self.message_input.get("1.0", tk.END).strip()
        crypto_key = self.key_entry.get().strip()

        if not original_msg or not crypto_key:
            messagebox.showwarning("Entrada Inválida", "Mensagem e chave de criptografia não podem estar vazias.")
            return

        try:
            # 1. Criptografia (T4)
            encrypted_msg = vigenere_encrypt(original_msg, crypto_key)
            self.update_text_widget(self.encrypted_msg_display, encrypted_msg)

            # 2. Mensagem em Binário (T5)
            binary_msg = text_to_binary(encrypted_msg)
            self.update_text_widget(self.binary_msg_display, binary_msg)

            # 3. Aplicação do Algoritmo MLT-3 (T6)
            mlt3_signal = encode_mlt3(binary_msg)
            self.last_sent_mlt3_signal = mlt3_signal # Armazenar para o gráfico de transmissão
            self.update_text_widget(self.mlt3_encoded_display, str(mlt3_signal))

            # 4. Exibir Gráfico MLT-3 (Transmissão - T2)
            self._plot_mlt3_transmit(mlt3_signal, "Forma de Onda MLT-3 (Transmissão)")

            # 5. Enviar pela rede (T7) - Converte a lista de ints para uma string
            # Uma forma simples de enviar a lista é convertê-la para string, e o receptor converte de volta
            # Para maior robustez, pode-se usar serialização (ex: JSON, pickle)
            data_to_send = ','.join(map(str, mlt3_signal))
            self.network_manager.send_data(data_to_send)
            messagebox.showinfo("Sucesso", "Mensagem processada e enviada!")

        except Exception as e:
            messagebox.showerror("Erro de Processamento", f"Ocorreu um erro: {e}")

    def handle_received_mlt3_signal(self, received_data):
        # Este método é chamado na thread de rede, então precisamos usar `after` para atualizar a GUI
        self.root.after(0, self._process_received_data_on_gui_thread, received_data)

    def _process_received_data_on_gui_thread(self, received_data):
        crypto_key = self.key_entry.get().strip()
        if not crypto_key:
            messagebox.showwarning("Erro de Chave", "A chave de criptografia está vazia no receptor.")
            return

        try:
            # 1. Converter a string recebida de volta para lista de inteiros MLT-3
            # Filtrar entradas vazias se houver vírgulas extras no final
            mlt3_signal_received = [int(x) for x in received_data.split(',') if x.strip()]
            self.update_text_widget(self.mlt3_received_display, str(mlt3_signal_received))

            # 2. Exibir Gráfico MLT-3 (Recepção - T2)
            self._plot_mlt3_receive(mlt3_signal_received, "Forma de Onda MLT-3 (Recepção)")

            # 3. Decodificação MLT-3 (T8 - processo inverso)
            binary_decoded = decode_mlt3(mlt3_signal_received)
            self.update_text_widget(self.binary_decoded_display, binary_decoded)

            # 4. Conversão de Binário para Texto (T8 - processo inverso)
            # O texto aqui ainda está criptografado
            encrypted_text_decoded = binary_to_text(binary_decoded)
            self.update_text_widget(self.encrypted_msg_display, encrypted_text_decoded) # Atualiza o campo de criptografada no emissor tambem
            self.update_text_widget(self.decrypted_msg_display, encrypted_text_decoded) # Mostrar a msg antes de descriptografar

            # 5. Descriptografia (T8 - processo inverso)
            final_original_msg = vigenere_decrypt(encrypted_text_decoded, crypto_key)
            self.update_text_widget(self.final_msg_display, final_original_msg)

        except Exception as e:
            messagebox.showerror("Erro de Recepção", f"Erro ao processar dados recebidos: {e}")

    def _plot_mlt3_transmit(self, mlt3_signal, title):
        self.ax_transmit.clear()
        x = np.arange(len(mlt3_signal))
        y = np.array(mlt3_signal)
        self.ax_transmit.step(x, y, where='post', color='blue', linestyle='-', linewidth=2)
        self.ax_transmit.hlines([-1, 0, 1], xmin=0, xmax=len(mlt3_signal)-1, color='gray', linestyle='--', alpha=0.7)
        self.ax_transmit.set_title(title)
        self.ax_transmit.set_xlabel("Tempo/Bit")
        self.ax_transmit.set_ylabel("Nível de Tensão")
        self.ax_transmit.set_yticks([-1, 0, 1], ['-V', '0V', '+V'])
        self.ax_transmit.grid(True, linestyle=':', alpha=0.6)
        self.ax_transmit.set_ylim(-1.5, 1.5)
        self.canvas_transmit.draw_idle()

    def _plot_mlt3_receive(self, mlt3_signal, title):
        self.ax_receive.clear()
        x = np.arange(len(mlt3_signal))
        y = np.array(mlt3_signal)
        self.ax_receive.step(x, y, where='post', color='green', linestyle='-', linewidth=2) # Cor diferente para recepção
        self.ax_receive.hlines([-1, 0, 1], xmin=0, xmax=len(mlt3_signal)-1, color='gray', linestyle='--', alpha=0.7)
        self.ax_receive.set_title(title)
        self.ax_receive.set_xlabel("Tempo/Bit")
        self.ax_receive.set_ylabel("Nível de Tensão")
        self.ax_receive.set_yticks([-1, 0, 1], ['-V', '0V', '+V'])
        self.ax_receive.grid(True, linestyle=':', alpha=0.6)
        self.ax_receive.set_ylim(-1.5, 1.5)
        self.canvas_receive.draw_idle()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    # Lidar com o fechamento da janela para garantir que a rede seja fechada
    def on_closing():
        if app.network_manager:
            app.network_manager.close()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()