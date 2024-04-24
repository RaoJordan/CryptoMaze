def hex_to_int(c):
    first = ord(c) // 16 - 3
    second = ord(c) % 16
    result = first * 10 + second
    if result > 9:
        result -= 1
    return result

def hex_to_ascii(c, d):
    high = hex_to_int(c) * 16
    low = hex_to_int(d)
    return high + low

def main_ascii(st):
    length = len(st)
    j = 0
    buf = '\x00'
    string_print = []
    for i in range(length):
        if i % 2 != 0:
            string_print.append(chr(hex_to_ascii(buf, st[i])))
            j += 1
        else:
            buf = st[i]
    return ''.join(string_print)

# Example usage:
# st = "48656C6C6F3B"
# result = main_ascii(st)
# print(result)
