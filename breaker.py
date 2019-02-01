import re
import collections

plaintext = [[4, 19], [19, 19]] # [[t h], [h e]] inversed!

alphabet = "abcdefghijklmnopqrstuvwxyz"

english_words = set(open("english_words.txt").read().splitlines())


def matrix_multiplication(A, B):
    output=[
        [A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
        [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]
    ]
    return output


def modulo_of_matrix(A, modulo):
    return [[A[0][0] % modulo, A[0][1] % modulo], [A[1][0] % modulo, A[1][1] % modulo]]


def digram_to_matrix(digrams):

    text_one = [alphabet.find(digrams[0][0]), alphabet.find(digrams[0][1])]
    text_two = [alphabet.find(digrams[1][0]), alphabet.find(digrams[1][1])]

    output = [
        [text_one[0], text_two[0]],
        [text_one[1], text_two[1]]
    ]

    return output


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def inverse_matrix(A):
    det_A = (A[0][0]*A[1][1] - A[0][1]*A[1][0]) % 26
    inverse_det_A = modinv(det_A, 26)
    A_inversed = [
        [inverse_det_A*A[1][1], -inverse_det_A*A[0][1]],
        [-inverse_det_A*A[1][0], inverse_det_A*A[0][0]]
    ]
    mod_A_inversed = modulo_of_matrix(A_inversed, 26)
    return mod_A_inversed


def cipher_matrix_to_text(A):
    output = ""
    output += alphabet[A[0][0]]
    output += alphabet[A[1][0]]
    output += alphabet[A[0][1]]
    output += alphabet[A[1][1]]
    return output


def find_top_digrams(digram_list):
    counter = collections.Counter(digram_list)
    most_common = counter.most_common(20)
    return [digram[0] for digram in most_common]


def convert_text_to_digrams(text):
    digram_list = []
    digram = ""
    for index in range(len(text)):
        digram += text[index]
        if (index + 1) % 2 == 0:
            digram_list.append(digram)
            digram = ""
        if index == len(text) - 1 and digram != "":
            digram += "z"
            digram_list.append(digram)
    return digram_list


def decrypt_digram(digram, key):
    val = [alphabet.find(digram[0]), alphabet.find(digram[1])]
    decrypted_values = [key[0][0]*val[0]+key[0][1]*val[1], key[1][0]*val[0]+key[1][1]*val[1]]
    decrypted = ""
    for val in decrypted_values:
        decrypted += alphabet[val % 26]
    return decrypted

def find_possible_keys(digrams):
    possible_keys=[]
    for first in range(len(digrams)):
        for second in range(len(digrams)):
            if first != second:
                matrix = digram_to_matrix([digrams[first], digrams[second]])
                pos_key = matrix_multiplication(matrix, plaintext)
                possible_keys.append(modulo_of_matrix(pos_key, 26))
    return possible_keys


def decrypt_text(filename):
    cipher = open(filename).read()
    cipher = cipher.lower()
    first_space_index = cipher.find(" ")
    regex = re.compile("[^a-z]")
    cipher = regex.sub("", cipher)

    digram_list = convert_text_to_digrams(cipher)

    top_digrams = find_top_digrams(digram_list)

    possible_keys = find_possible_keys(top_digrams)

    for key in possible_keys:

        try:
            inverse_key = inverse_matrix(key)
        except Exception:
            continue

        decrypted = ""
        for digram in digram_list:
            decrypted += decrypt_digram(digram, inverse_key)

        first_word = decrypted[:first_space_index]
        if first_word in english_words:
            print("\n\n\nFound a candidate key!")
            print("Word: " + first_word)
            print("Key: " + str(key))
            print("Inversed key: " + str(inverse_key))
            print("Decrypted: " + decrypted + "\n\n\n")


decrypt_text("2.txt")
