import streamlit as st
from mpmath import mp
from datetime import datetime
import locale
from babel.dates import format_date

# Configurer mpmath pour calculer un grand nombre de décimales de pi
mp.dps = 1000000  # Nombre de décimales de précision

# Fonction pour obtenir les premières décimales de pi
@st.cache_data
def get_pi_decimals():
    return str(mp.pi)[2:]  # Ignorer "3."

# Interpréteur Brainfuck
def brainfuck_interpreter(code, input_data=''):
    code = ''.join(filter(lambda x: x in ['>', '<', '+', '-', '.', ',', '[', ']'], code))
    tape = [0] * 30000
    code_pointer = 0
    tape_pointer = 0
    input_pointer = 0
    output = []
    stack = []
    log = []

    while code_pointer < len(code):
        command = code[code_pointer]
        log.append((code_pointer, command, tape_pointer, tape[tape_pointer]))

        if command == '>':
            tape_pointer += 1
        elif command == '<':
            tape_pointer -= 1
        elif command == '+':
            tape[tape_pointer] = (tape[tape_pointer] + 1) % 256
        elif command == '-':
            tape[tape_pointer] = (tape[tape_pointer] - 1) % 256
        elif command == '.':
            output.append(chr(tape[tape_pointer]))
        elif command == ',':
            if input_pointer < len(input_data):
                tape[tape_pointer] = ord(input_data[input_pointer])
                input_pointer += 1
            else:
                tape[tape_pointer] = 0
        elif command == '[':
            if tape[tape_pointer] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    code_pointer += 1
                    if code[code_pointer] == '[':
                        open_brackets += 1
                    elif code[code_pointer] == ']':
                        open_brackets -= 1
            else:
                stack.append(code_pointer)
        elif command == ']':
            if tape[tape_pointer] != 0:
                code_pointer = stack[-1]
            else:
                stack.pop()

        code_pointer += 1

    return ''.join(output), log

# Fonction pour rechercher une séquence dans les décimales de pi
def find_in_pi(sequence, pi_decimals):
    index = pi_decimals.find(sequence)
    return index

# Fonction pour obtenir la date de naissance formatée en français
def get_french_birthdate(birthdate):
    try:
        date_obj = datetime.strptime(birthdate, "%d%m%Y")
        # Utiliser Babel pour formater la date en français
        formatted_date = format_date(date_obj, format='full', locale='fr_FR')
        return formatted_date
    except ValueError:
        return None

# Fonction pour calculer la somme des n premières décimales de pi
def sum_of_decimals(pi_decimals, n):
    return sum(int(digit) for digit in pi_decimals[:n])

# Interface utilisateur Streamlit
st.title("Interpréteur Brainfuck et Calculs avec Pi")

# Interpréteur Brainfuck
st.header("Interpréteur Brainfuck")
code = st.text_area("Entrez votre code Brainfuck ici:")
input_data = st.text_input("Entrez les données d'entrée (si nécessaire):")

if st.button("Exécuter"):
    try:
        result, log = brainfuck_interpreter(code, input_data)
        st.text_area("Sortie:", result, height=200)
        st.text_area("Logs d'exécution:", "\n".join([f"Code Pointer: {step[0]}, Commande: {step[1]}, Tape Pointer: {step[2]}, Tape Value: {step[3]}" for step in log]), height=400)
    except Exception as e:
        st.error(f"Erreur lors de l'exécution du code Brainfuck: {e}")

# Recherche de date de naissance dans Pi
st.header("Recherche de Date de Naissance dans Pi")
birthdate = st.text_input("Entrez votre date de naissance (format JJMMYYYY):")

if st.button("Rechercher dans Pi"):
    if len(birthdate) == 8 and birthdate.isdigit():
        pi_decimals = get_pi_decimals()
        index = find_in_pi(birthdate, pi_decimals)
        if index != -1:
            st.success(f"Votre date de naissance se trouve à la position {index} dans les décimales de Pi.")
        else:
            st.error("Votre date de naissance ne se trouve pas dans le premier million de décimales de Pi.")
        
        # Calculer et afficher le jour de la semaine et la date en français
        formatted_date = get_french_birthdate(birthdate)
        if formatted_date:
            st.write(f"Vous êtes né(e) le {formatted_date}.")
        else:
            st.error("Format de date de naissance invalide. Veuillez entrer une date au format JJMMYYYY.")
    else:
        st.error("Format de date de naissance invalide. Veuillez entrer une date au format JJMMYYYY.")

# Calculs avec Pi
st.header("Calculs avec les Décimales de Pi")
pi_decimals = get_pi_decimals()

# Calculer la somme des 20 premières décimales de pi
sum_20 = sum_of_decimals(pi_decimals, 20)
st.write(f"La somme des 20 premières décimales de pi est : {sum_20}")

# Calculer la somme des 144 premières décimales de pi (12²)
sum_144 = sum_of_decimals(pi_decimals, 144)
# Utiliser Unicode pour afficher 12²
st.write(f"La somme des 12\u00B2 premières décimales de pi est : {sum_144}")

# Ajouter une vidéo expliquant la somme de tous les nombres entiers naturels
st.header("Vidéo explicative : La somme de tous les nombres entiers naturels est égale à -1/12")
st.video("https://www.youtube.com/watch?v=w-I6XTVZXww")
