import struct
import sys

binary_file_path = "test_binary_file.bin"

signed_values = [32767, -32768]

results = []
for value in signed_values:
    with open(binary_file_path, "wb") as bin_file:
        bin_file.write(struct.pack("h", value))

    with open(binary_file_path, "rb") as bin_file:
        unsigned_value = struct.unpack("H", bin_file.read(2))[0]
        results.append((value, unsigned_value))

print(results)

'''
При записи числа в формате знакового двухбайтного (16-бит) числа, оно хранится в двоичном виде.
При чтении его как беззнакового число интерпретируется по тем же битам, но как положительное значение. Для −32768,
которое в двоичном представлении 
1000000000000000, в беззнаковом представлении интерпретируется как 32768
'''

binary_file_path1 = "test_binary_file1.bin"

signed_values = [-32641, 0]

results = []
for value in signed_values:
    with open(binary_file_path1, "wb") as bin_file:
        bin_file.write(struct.pack("h", value))

    with open(binary_file_path1, "rb") as bin_file:
        unsigned_value = struct.unpack("H", bin_file.read(2))[0]
        results.append((value, unsigned_value))

print(results)

bytes_part1 = struct.pack("h", -32641)
bytes_part2 = struct.pack("h", 0)

combined_bytes = bytes_part1 + bytes_part2

original_float = struct.unpack(">f", combined_bytes)[0]

print(original_float)

'''
Полученное значение после чтения данных как вещественного числа в формате float с порядком байт big-endian равно бесконечности (inf).
Это указывает на то, что сочетание байт, представляющих числа −32641 и 0,
в большинстве стандартов представления чисел с плавающей точкой (например, IEEE 754) кодирует бесконечность.
Это может быть связано с тем, что старшие биты числа (в данном случае -32641, представленные как 1000 0000 0000 0011 в двоичной системе)
соответствуют значению экспоненты для бесконечности или NaN (не число) в стандарте IEEE 754 для чисел одинарной точности.
'''

float_file_path = "test_float_file.bin"

float_values = [sys.float_info.max, -sys.float_info.max, 0.0, 1.0, -1.0, 1e-10, 3.141592653589793]

float_results = []
for f_value in float_values:
    with open(float_file_path, "wb") as bin_file:
        bin_file.write(struct.pack("f", f_value))

    with open(float_file_path, "rb") as bin_file:
        binary_data = bin_file.read(4)
        int_part1, int_part2 = struct.unpack("hh", binary_data)
        float_results.append((f_value, int_part1, int_part2))

print(float_values)

'''
Максимальное и минимальное значения float: Наблюдаемые значения экспонент указывают на специальные случаи
(бесконечность, очень большие числа), где младшие биты (первые два байта) остаются нулевыми,
а старшие биты (вторые два байта) отображают экстремальные значения экспоненты.
Нулевое значение: Как ожидалось, все биты равны нулю.
Положительные и отрицательные значения: Положительное и отрицательное значения 1.0 и -1.0 показывают,
что младшие биты (первые два байта) остаются нулевыми, что указывает на небольшие значения экспоненты,
а знак числа отображается в старших битах (вторые два байта).
Маленькое положительное значение и значение π: Показывают как мантиссу, так и экспоненту числа,
представленные в двух парах байт.

Это демонстрирует, как вещественные числа представляются в памяти компьютера в соответствии с IEEE 754,
и как разные части числа (мантисса и экспонента) могут быть интерпретированы при чтении как целые числа.
'''

int1 = -32641
int2 = 0

bytes_part1 = struct.pack('>h', int1)
bytes_part2 = struct.pack('>h', int2)

full_bytes = bytes_part1 + bytes_part2

result_float = struct.unpack('>f', full_bytes)[0]
print(result_float)
