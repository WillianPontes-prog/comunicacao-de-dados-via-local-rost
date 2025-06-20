# mlt3.py
import matplotlib.pyplot as plt
import numpy as np

def encode_mlt3(binary_string):
    """Codifica uma string binária usando MLT-3."""
    mlt3_signal = []
    current_level = 0  # Pode ser 0, +1, -1
    last_non_zero_level = 0 # Usado para saber a direção do 1

    for bit in binary_string:
        if bit == '0':
            mlt3_signal.append(current_level)
        elif bit == '1':
            if current_level == 0:
                # Se veio de +1, vai para -1; se veio de -1 ou 0, vai para +1
                if last_non_zero_level == 1:
                    current_level = -1
                else:
                    current_level = 1
            elif current_level == 1:
                current_level = 0
                last_non_zero_level = 1
            elif current_level == -1:
                current_level = 0
                last_non_zero_level = -1
            mlt3_signal.append(current_level)
        else:
            raise ValueError("String binária inválida, esperados apenas '0' ou '1'.")
    return mlt3_signal

def decode_mlt3(mlt3_signal):
    """Decodifica um sinal MLT-3 para uma string binária."""
    if not mlt3_signal:
        return ""

    binary_string = []

    # Inferir o primeiro bit:
    # Se o primeiro nível do sinal MLT-3 é 0, o primeiro bit original foi '0' (assumindo estado inicial 0).
    # Se o primeiro nível é diferente de 0 (+1 ou -1), o primeiro bit original foi '1' (houve uma transição do estado inicial 0).
    if mlt3_signal[0] == 0:
        binary_string.append('0')
    else:
        binary_string.append('1')

    # Decodificar os bits subsequentes com base nas transições
    for i in range(1, len(mlt3_signal)):
        if mlt3_signal[i] == mlt3_signal[i-1]:
            binary_string.append('0') # Nenhuma mudança de nível significa um '0'
        else:
            binary_string.append('1') # Mudança de nível significa um '1'
    return ''.join(binary_string)

def plot_mlt3_signal(mlt3_signal, title="Sinal MLT-3"):
    """Gera o gráfico de um sinal MLT-3."""
    plt.figure(figsize=(10, 4))
    x = np.arange(len(mlt3_signal))
    y = np.array(mlt3_signal)

    # Plotar as linhas verticais para indicar os níveis
    plt.step(x, y, where='post', color='blue', linestyle='-', linewidth=2)
    plt.hlines([-1, 0, 1], xmin=0, xmax=len(mlt3_signal)-1, color='gray', linestyle='--', alpha=0.7)

    plt.title(title)
    plt.xlabel("Tempo/Bit")
    plt.ylabel("Nível de Tensão")
    plt.yticks([-1, 0, 1], ['-V', '0V', '+V'])
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(-1.5, 1.5) # Ajusta o limite Y para melhor visualização
    plt.show()

# Exemplo de uso:
# bin_str = "1011001"
# mlt3_encoded = encode_mlt3(bin_str)
# print(f"Binário: {bin_str}")
# print(f"MLT-3 codificado: {mlt3_encoded}")
# plot_mlt3_signal(mlt3_encoded, "Codificação MLT-3")
# mlt3_decoded = decode_mlt3(mlt3_encoded)
# print(f"MLT-3 decodificado: {mlt3_decoded}")
def plot_mlt3_signal(mlt3_signal, title="Sinal MLT-3"):
    """Gera o gráfico de um sinal MLT-3."""
    plt.figure(figsize=(10, 4))
    x = np.arange(len(mlt3_signal))
    y = np.array(mlt3_signal)

    # Plotar as linhas verticais para indicar os níveis
    plt.step(x, y, where='post', color='blue', linestyle='-', linewidth=2)
    plt.hlines([-1, 0, 1], xmin=0, xmax=len(mlt3_signal)-1, color='gray', linestyle='--', alpha=0.7)

    plt.title(title)
    plt.xlabel("Tempo/Bit")
    plt.ylabel("Nível de Tensão")
    plt.yticks([-1, 0, 1], ['-V', '0V', '+V'])
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(-1.5, 1.5) # Ajusta o limite Y para melhor visualização
    plt.show()

# Exemplo de uso:
# bin_str = "1011001"
# mlt3_encoded = encode_mlt3(bin_str)
# print(f"Binário: {bin_str}")
# print(f"MLT-3 codificado: {mlt3_encoded}")
# plot_mlt3_signal(mlt3_encoded, "Codificação MLT-3")
# mlt3_decoded = decode_mlt3(mlt3_encoded)
# print(f"MLT-3 decodificado: {mlt3_decoded}")