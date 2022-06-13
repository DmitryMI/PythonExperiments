alphabet = [
    '4',    # A
    '6',    # B
    '<',    # C
    '|)',   # D
    '3',    # E
    '|=',   # F
    '(;',   # G
    '|-|',  # H
    '!',    # I
    '_|',   # J
    '|{',   # K 
    '|_',   # L
    '|\/|', # M
    '|\|',  # N
    '0',    # O
    '|>',   # P
    'O_',   # Q
    '|?',   # R
    '5',    # S
    "'|'",  # T
    '(_)',  # U
    '\/',   # V
    '\|/',  # W
    '><',   # X
    "`|",   # Y
    '2'     # Z
]

def get_leet_for_char(current_char):
    index = ord(current_char) - 65
    sub_alphabet = alphabet[index]
    leet_symbol = choice(sub_alphabet)

    return leet_symbol


def respects_phano():
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            if i == j:
                continue
            if alphabet[i].startswith(alphabet[j]):
                return False, i, j

    return True, None, None

def get_index_of_letter(letter):
    symbol = letter.lower()
    index = ord(symbol) - ord('a')
    return index

def get_letter_from_index(index):
    ascii_code = index + ord('a')
    return chr(ascii_code)

def forward_conversion(text):
    result = ""
    for i in text:
        index = get_index_of_letter(i)

        if i == ' ':
            result += '___ '
        elif index < 0 or index > len(alphabet):
            pass
        else:
            result += alphabet[index] + ' '
    return result

def backward_conversion(leet_untrimmed):
    leet = ""
    for i, symbol in enumerate(leet_untrimmed):
        if symbol != ' ' or i == len(leet) - 1:
            leet += symbol
        elif leet_untrimmed[i + 1] == ' ':
            leet += ' '

    result = ""

    code_accumulator = ""
    for i, symbol in enumerate(leet):

        if symbol == " ":
            result += " "
            continue

        code_accumulator += symbol
        code_match = False
        for code_index, code in enumerate(alphabet):
            if code_accumulator == code:                
                code_match = True
                letter = get_letter_from_index(code_index)
                result += letter
                break
        if code_match:
            code_accumulator = ""      

    return result


phano_respected, codeA, codeB = respects_phano()
if not phano_respected:
    print(f"Warning! Phano rule is violated by {get_letter_from_index(codeA)} {alphabet[codeA]} and {get_letter_from_index(codeB)} {alphabet[codeB]}")

while True:
    text = input("Text: ")    
    leet = forward_conversion(text)
    print(leet)

    leet = input("Leet: ")
    text = backward_conversion(leet)
    print(text)