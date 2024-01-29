import socket
import re

def convert_to_number(s):
    """
    Convert a number in various formats (words, hexadecimal, binary) to an integer.
    """
    word_to_number = {
        "ZERO": 0, "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4,
        "FIVE": 5, "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9
    }

    if s.upper() in word_to_number:
        return word_to_number[s.upper()]

    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)

    if s.startswith("0b") or s.startswith("0B"):
        return int(s, 2)

    return int(s)

def evaluate_expression(expression):
    """
    Evaluate an arithmetic expression where numbers can be in various formats.
    Correctly handles hyphenated word numbers.
    """
    # Replace hyphenated word numbers first
    hyphenated_words = re.findall(r'\b((?:ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)(?:-(?:ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE))*)\b', expression, re.IGNORECASE)
    for hyphenated_word in hyphenated_words:
        number_parts = hyphenated_word.split('-')
        number_str = ''.join([str(convert_to_number(part)) for part in number_parts])
        expression = expression.replace(hyphenated_word, number_str)

    # Replace individual words
    words = re.findall(r'\b(ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)\b', expression, re.IGNORECASE)
    for word in words:
        expression = expression.replace(word, str(convert_to_number(word)))

    # Replace hexadecimal and binary numbers
    hex_and_bin_numbers = re.findall(r'\b(0x[0-9a-fA-F]+|0b[01]+)\b', expression)
    for number in hex_and_bin_numbers:
        expression = expression.replace(number, str(convert_to_number(number)))

    return eval(expression)

def connect_and_solve(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            data = s.recv(1024).decode()
            print(data)

            if " = ?" in data:
                expression = re.search(r'([\w\s*+-/]+) = \?', data).group(1)
                result = evaluate_expression(expression)
                s.sendall(str(result).encode() + b'\n')

            if "Congratulations" in data or "Wrong" in data:
                break

host = "offsec-chalbroker.osiris.cyber.nyu.edu"
port = 1236
connect_and_solve(host, port)
