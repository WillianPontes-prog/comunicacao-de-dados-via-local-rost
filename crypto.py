# crypto.py ou em um módulo de utilidades

def text_to_binary(text):
    """Converte uma string para sua representação binária usando ASCII estendido."""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def binary_to_text(binary_string):
    """Converte uma string binária de volta para texto."""
    if len(binary_string) % 8 != 0:
        raise ValueError("A string binária deve ter um número de bits divisível por 8.")
    text = ""
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        text += chr(int(byte, 2))
    return text

# Exemplo de uso:
# msg = "Olá, mundo!"
# bin_msg = text_to_binary(msg)
# print(f"'{msg}' em binário: {bin_msg}")
# print(f"Binário de volta para texto: {binary_to_text(bin_msg)}")

# crypto.py

def vigenere_encrypt(text, key):
    """Criptografa texto usando a Cifra de Vigenère."""
    encrypted_text = []
    key_len = len(key)
    for i, char in enumerate(text):
        key_char = key[i % key_len]
        # Aplica a cifra mantendo o range ASCII estendido
        encrypted_char = chr((ord(char) + ord(key_char)) % 256) # Módulo 256 para ASCII estendido
        encrypted_text.append(encrypted_char)
    return ''.join(encrypted_text)

def vigenere_decrypt(encrypted_text, key):
    """Descriptografa texto usando a Cifra de Vigenère."""
    decrypted_text = []
    key_len = len(key)
    for i, char in enumerate(encrypted_text):
        key_char = key[i % key_len]
        # Aplica a cifra inversa
        decrypted_char = chr((ord(char) - ord(key_char) + 256) % 256) # Adiciona 256 para garantir positivo
        decrypted_text.append(decrypted_char)
    return ''.join(decrypted_text)

# Exemplo de uso:
# key = "CHAVE"
# msg_original = "Olá, mundo!"
# msg_criptografada = vigenere_encrypt(msg_original, key)
# print(f"Mensagem original: {msg_original}")
# print(f"Mensagem criptografada: {msg_criptografada}")
# msg_descriptografada = vigenere_decrypt(msg_criptografada, key)
# print(f"Mensagem descriptografada: {msg_descriptografada}")