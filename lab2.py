import random
from sympy import isprime, mod_inverse

def generate_prime_candidate(length):
    """ Генерує випадкове непарне число """
    p = random.getrandbits(length)
    # встановлюємо старший та молодший біти в 1
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=16):
    """ Генерує просте число довжиною `length` бітів """
    p = 4
    # генеруємо, поки число не стане простим
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

def generate_rsa_keys(bit_length):
    p = generate_prime_number(bit_length // 2)
    q = generate_prime_number(bit_length // 2)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randrange(1, phi_n)
    # забезпечуємо, щоб e було взаємно простим з phi_n та 1 < e < phi_n
    g = gcd(e, phi_n)
    while g != 1:
        e = random.randrange(1, phi_n)
        g = gcd(e, phi_n)

    d = mod_inverse(e, phi_n)

    return (e, n), (d, n)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def encrypt(message, pub_key):
    e, n = pub_key
    return pow(message, e, n)

def decrypt(ciphertext, priv_key):
    d, n = priv_key
    return pow(ciphertext, d, n)

# Генеруємо RSA ключі
public_key, private_key = generate_rsa_keys(32)

# Приклад використання
message = 65
print("Оригінальне повідомлення:", message)

encrypted_msg = encrypt(message, public_key)
print("Зашифроване повідомлення:", encrypted_msg)

decrypted_msg = decrypt(encrypted_msg, private_key)
print("Розшифроване повідомлення:", decrypted_msg)

# Виводимо ключі
print("Відкритий ключ (e, n):", public_key)
print("Закритий ключ (d, n):", private_key)
