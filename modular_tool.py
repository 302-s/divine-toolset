from cicada_functions import *
import sys
import json
import itertools
from collections import Counter
import math

# Get filename from system args
filename = sys.argv[1]

# Open JSON file and retrieve the data
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

# Define ciphertext from JSON
ciphertext = data["ciphertext"]

# Currently available algorithms in the tool
available_algos = ['Vigenere', 'Atbash', 'Autokey', 'Eulers', 'Shift']

# Initialise some variables
decrypt_results = []
used_encryptions = []
previous_result = ""

# Define the main decryption function for later than first time use.
# Need ciphertext, encryption method from available alogs, certian parameter dictionary and analysis dictionary
def decrypt(ciphertext,encryption_method,params,analysis):

    # Basic switch between decryptions
    # Every decryption gets the result from the function. See cicada_functions.py to see what the variables are for
   
    # Perform analysis functions based on parameters (or don't)
    match encryption_method:
        case "Vigenere":
            result_ciphertext = vigenere(ciphertext,params.get("key"),True,params.get("skips"), False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Atbash":
            result_ciphertext = atbash(ciphertext,False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Eulers":
            result_ciphertext = eulers(ciphertext,False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Autokey":
            if params.get("source") == "Ciphertext":
                result_ciphertext = autokey(ciphertext,False, params.get("reversed"))
                previous_result = result_ciphertext
                analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Shift":
            result_ciphertext = shift(ciphertext,params.get("shift"),False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))

# The tool can handle multiple encryptions at the same time, as seen in examlpe json.
# results from all are printed after which it is possible to chain-link to one of the results.

for encryption in data["encryption"]:
    encryption_method = encryption.get("type")
    params = encryption.get("params")
    analysis = encryption.get("analysis")
    phonetic = params.get("phonetic")
    used_encryptions.append(encryption_method)
    match encryption_method:
        case "Vigenere":
            result_ciphertext = vigenere(ciphertext,params.get("key"),True,params.get("skips"), False)
            decrypt_results.append(result_ciphertext)
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Atbash":
            result_ciphertext = atbash(ciphertext,False)
            decrypt_results.append(result_ciphertext)
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Eulers":
            result_ciphertext = eulers(ciphertext,False)
            decrypt_results.append(result_ciphertext)
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
        case "Autokey":
            if params.get("source") == "Ciphertext":
                result_ciphertext = autokey(ciphertext,False, params.get("reversed"))
                decrypt_results.append(result_ciphertext)
                analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == "True":
                print(direct_translation(result_ciphertext))
    print("\n\n")


chaining = True
first_time = True

current_text = ""

# Holy spaghetti code
while chaining:
    option = input("Chain a result? (y/n)")
    if option == "n" or option == "no":
        break
    else:
        if first_time:
            old_algo = input("Select algo to chain from {0}[1-{1}]: ".format(used_encryptions, len(used_encryptions)))
            current_text = decrypt_results[int(old_algo)-1]
            previous_result = decrypt_results[int(old_algo)-1]
            algo = input("Select algo to chain to {0}[1-{1}]: ".format(available_algos, len(available_algos)))
            first_time = False
        else:
            algo = input("Select algo to chain to {0}[1-{1}]: ".format(available_algos, len(available_algos)))
            current_text = previous_result

        selected_algo = available_algos[int(algo)-1]


        # Define mandatory variables for the functions
        match selected_algo:
            case "Vigenere":
                skips = input("Insert skips (e.g. 61,73,118): ")
                key = input("Insert Vigenere key in runes: ")
                phonetic = input("Show phonetics? (True/False): ")
                parameters = {"skips": skips, "key":key, "phonetic":phonetic}
            case "Atbash":
                phonetic = input("Show phonetics? (True/False): ")
                parameters = {"skips": [], "phonetic": phonetic}
            case "Eulers":
                phonetic = input("Show phonetics? (True/False): ")
                parameters = {"phonetic": phonetic}
            case "Autokey":
                reversed = input("Reverse? (True/False): ")
                phonetic = input("Show phonetics? (True/False): ")
                parameters = {"skip": [], "source":"Ciphertext", "phonetic": phonetic, "reversed": reversed}
            case "Shift":
                shifts = input("Shift value: ")
                phonetic = input("Show phonetics? (True/False): ")
                parameters = {"shift":int(shifts), "phonetic": phonetic}

        analysis = encryption.get("analysis")

        # Set analysis parameters, IC2 not implemented
        ioc = input("IoC? (True/False): ")
        ic2 = False
        freq = input("Frequency? (True/False)")

        analysis = {"IoC": ioc, "IC2": ic2, "Frequency": freq}
        decrypt(current_text,selected_algo,parameters,analysis)