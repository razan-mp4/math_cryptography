import numpy as np

# Параметри генератора
num_registers = 12
register_size = 7
table_size = 2**num_registers
sample_size = 20000

# Ініціалізація зсувних регістрів
registers = [np.random.randint(0, 2, register_size) for _ in range(num_registers)]

# Заповнення таблиці з рівною кількістю нулів та одиниць
table = np.zeros(table_size, dtype=int)
half_size = table_size // 2
table[:half_size] = 1
np.random.shuffle(table)

# Функція для отримання адреси з регістрів
def get_address(registers):
    address = 0
    for i, reg in enumerate(registers):
        address = (address << 1) | reg[0]
    return address

# Функція зсуву регістрів
def shift_register(register):
    new_bit = register[1] ^ register[4]  # приклад простого LFSR
    return np.roll(register, -1), new_bit

# Генерація псевдовипадкової послідовності
sequence = []
for _ in range(sample_size):
    address = get_address(registers)
    sequence.append(table[address])
    for i in range(num_registers):
        registers[i], _ = shift_register(registers[i])

# Перетворення послідовності в масив numpy для аналізу
sequence = np.array(sequence)

# Тестування послідовності
def frequency_test(sequence):
    return np.mean(sequence)

def differential_test(sequence):
    return np.mean(sequence[:-1] ^ sequence[1:])

def rank_test(sequence, window_size=3):
    counts = {}
    for i in range(len(sequence) - window_size + 1):
        window = tuple(sequence[i:i+window_size])
        if window in counts:
            counts[window] += 1
        else:
            counts[window] = 1
    return counts

freq_result = frequency_test(sequence)
diff_result = differential_test(sequence)
rank_result = rank_test(sequence)

print(f"Frequency test result: {freq_result}")
print(f"Differential test result: {diff_result}")
print(f"Rank test result: {rank_result}")

# Лінійна складність (спрощений підхід)
def linear_complexity(sequence):
    n = len(sequence)
    lfsr = np.zeros(n, dtype=int)
    for i in range(n):
        lfsr[i] = sequence[i]
    return np.sum(lfsr)

lin_complexity = linear_complexity(sequence)

print(f"Linear complexity: {lin_complexity}")
