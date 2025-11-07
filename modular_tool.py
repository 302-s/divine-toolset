from cicada_functions import *
import sys
import json
import itertools
from collections import Counter
import math

# Get filename from system args

print(r"""
______  _         _                _____              _  _     _  _   
|  _  \(_)       (_)              |_   _|            | || |   (_)| |  
| | | | _ __   __ _  _ __    ___    | |  ___    ___  | || | __ _ | |_ 
| | | || |\ \ / /| || '_ \  / _ \   | | / _ \  / _ \ | || |/ /| || __|
| |/ / | | \ V / | || | | ||  __/   | || (_) || (_) || ||   < | || |_ 
|___/  |_|  \_/  |_||_| |_| \___|   \_/ \___/  \___/ |_||_|\_\|_| \__|
      
               For divine analysis and decryption purposes
      """)


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
            if params.get("phonetic") == True:
                print(direct_translation(result_ciphertext))
        case "Atbash":
            result_ciphertext = atbash(ciphertext,False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == True:
                print(direct_translation(result_ciphertext))
        case "Eulers":
            result_ciphertext = eulers(ciphertext,False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == True:
                print(direct_translation(result_ciphertext))
        case "Autokey":
            if params.get("source") == "Ciphertext":
                result_ciphertext = autokey(ciphertext,False, params.get("reversed"))
                previous_result = result_ciphertext
                analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == True:
                print(direct_translation(result_ciphertext))
        case "Shift":
            result_ciphertext = shift(ciphertext,params.get("shift"),False)
            previous_result = result_ciphertext
            analysis_functions(analysis,result_ciphertext)
            if params.get("phonetic") == True:
                print(direct_translation(result_ciphertext))

def analysis_main(ciphertext):
    ioc = input("IoC? (Y/n): ")
    if ioc == "n":
        ioc = False
    else:
        ioc = True
    ic2 = False
    freq = input("Frequency? (Y/n): ")
    if freq == "n":
        freq = False
    else:
        freq = True

        analysis = {"IoC": ioc, "IC2": ic2, "Frequency": freq}
    analysis_functions(analysis,ciphertext)

def input_ciphertext():
    ciphertext_lines = []
    print("Ciphertext (Enter twice when done): ")
    while True:
        ciphertext = input()
        if not ciphertext:
            break
        ciphertext_lines.append(ciphertext)
    ciphertext = ""
    for line in ciphertext_lines:
        ciphertext = ciphertext + line
    return ciphertext

def get_skips():
    skips = input("Insert skips (e.g. 61,73,118): ")
    skips_arr = []
    skips_split = skips.split(",")
    for item in skips_split:
        skips_arr.append(int(item))
    return skips_arr

def questions():
    phonetic = input("Phonetic? (Y/n): ")
    if phonetic == "n":
        phonetic = False
    else:
        phonetic = True
    analysis = input("Analysis? (Y/n): ")
    if analysis == "n":
        analysis = False
    else:
        analysis = True
    return analysis,phonetic

def menu_choices(selection, chained, *args):
    print("\n")
    result_ciphertext = ""
    match selection:
        case 1:
            filename = input("Filename (e.g. jpg.JSON): ")
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
                            if params.get("phonetic") == True:
                                print(direct_translation(result_ciphertext))
                        case "Atbash":
                            result_ciphertext = atbash(ciphertext,False)
                            decrypt_results.append(result_ciphertext)
                            analysis_functions(analysis,result_ciphertext)
                            if params.get("phonetic") == True:
                                print(direct_translation(result_ciphertext))
                        case "Eulers":
                            result_ciphertext = eulers(ciphertext,False)
                            decrypt_results.append(result_ciphertext)
                            analysis_functions(analysis,result_ciphertext)
                            if params.get("phonetic") == True:
                                print(direct_translation(result_ciphertext))
                        case "Autokey":
                            if params.get("source") == "Ciphertext":
                                result_ciphertext = autokey(ciphertext,False, params.get("reversed"))
                                decrypt_results.append(result_ciphertext)
                                analysis_functions(analysis,result_ciphertext)
                            if params.get("phonetic") == True:
                                print(direct_translation(result_ciphertext))
                    print("\n\n")

                    chaining = True
                    first_time = True

                    current_text = ""

                    # Holy spaghetti code
                    while chaining:
                        option = input("Chain a result? (Y/n)")
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
                                    skips_arr = []
                                    skips_split = skips.split(",")
                                    for item in skips_split:
                                        skips_arr.append(int(item))
                                    key = input("Insert Vigenere key in runes: ")
                                    phonetic = input("Show phonetics? (Y/n): ")
                                    if phonetic == "n":
                                        phonetic = False
                                    else:
                                        phonetic = True

                                    parameters = {"skips": skips_arr, "key":key, "phonetic":phonetic}

                                case "Atbash":
                                    phonetic = input("Show phonetics? (Y/n): ")
                                    if phonetic == "n":
                                        phonetic = False
                                    else:
                                        phonetic = True

                                    parameters = {"skips": [], "phonetic": phonetic}
                                case "Eulers":
                                    phonetic = input("Show phonetics? (Y/n): ")
                                    if phonetic == "n":
                                        phonetic = False
                                    else:
                                        phonetic = True

                                    parameters = {"phonetic": phonetic}

                                case "Autokey":
                                    reversed = input("Reverse? (Y/n): ")
                                    if reversed == "n":
                                        reversed = False
                                    else:
                                        reversed = True

                                    phonetic = input("Show phonetics? (Y/n): ")
                                    if phonetic == "n":
                                        phonetic = False
                                    else:
                                        phonetic = True
                                    parameters = {"skip": [], "source":"Ciphertext", "phonetic": phonetic, "reversed": reversed}

                                case "Shift":
                                    shifts = input("Shift value: ")
                                    phonetic = input("Show phonetics? (Y/n): ")
                                    if phonetic == "n":
                                        phonetic = False
                                    else:
                                        phonetic = True
                                    ic2 = False
                                    parameters = {"shift":int(shifts), "phonetic": phonetic}

                            analysis = encryption.get("analysis")

                            # Set analysis parameters, IC2 not implemented
                            ioc = input("IoC? (Y/n): ")
                            if ioc == "n":
                                ioc = False
                            else:
                                ioc = True
                            ic2 = False
                            freq = input("Frequency? (Y/n)")
                            if freq == "n":
                                freq = False
                            else:
                                freq = True

                            analysis = {"IoC": ioc, "IC2": ic2, "Frequency": freq}
                            decrypt(current_text,selected_algo,parameters,analysis)

        case 2:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            analysis_main(ciphertext)

        case 3:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            key = input("Key in runes: ")
            analysis, phonetic = questions()
            skips = get_skips()
            result_ciphertext = vigenere(ciphertext,key,True,skips, False)

            if analysis:
                analysis_main(result_ciphertext)
            if phonetic == True:
                print(direct_translation(result_ciphertext))

        case 4:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            result_ciphertext = atbash(ciphertext,False)
            phonetic = input("Phonetic? (Y/n): ")
            if phonetic == "n":
                phonetic = False
            else:
                phonetic = True
            analysis = input("Analysis? (Y/n): ")
            if analysis == "n":
                analysis = False
            else:
                analysis = True
            if analysis:
                analysis_main(result_ciphertext)
            if phonetic == True:
                print(direct_translation(result_ciphertext))

        case 5:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            result_ciphertext = atbash(ciphertext,False)
            analysis, phonetic = questions()
            if analysis:
                analysis_main(result_ciphertext)
            if phonetic == True:
                print(direct_translation(result_ciphertext))
        
        case 6:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            result_ciphertext = eulers(ciphertext,False)

            analysis, phonetic = questions()

            if analysis:
                analysis_main(result_ciphertext)
            if phonetic == True:
                print(direct_translation(result_ciphertext))
        
        case 7:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            shift_amount = input("Shift amount: ")
            result_ciphertext = shift(ciphertext,int(shift_amount),False)

            analysis, phonetic = questions()
            if analysis:
                analysis_main(result_ciphertext)
            if phonetic == True:
                print(direct_translation(result_ciphertext))
 
        case 8:
            n = input("Give n for nth prime: ")
            print("Nth prime: {0}".format(nthprime(int(n))))
            return False, ""
 
        case 9:
            n = input("Give a prime number: ")
            print("Primes position: {0}".format(prime_position(int(n))))
            return False, ""
 
        case 10:
            if chained:
                ciphertext = args[0]
            else:
                ciphertext = input_ciphertext()
            result_ciphertext = direct_translation(ciphertext)

            analysis, phonetic = questions()
            if analysis:
                analysis_main(result_ciphertext)

    print("\n")
    chain_bool = input("Chain decrypted text? (Y/n): ")
    if chain_bool == "n":
        chain_bool = False
        return chain_bool, ""
    else:
        chain_bool = True
        return chain_bool, result_ciphertext
def menu():
    while True:
        print("\n")
        selection = input("Choose what to perform.\n[1] Use a JSON file (see example.json)\n[2] Crypto analysis (IoC, IC2, Frequency)\n[3] Vigenere\n[4] Atbash\n[5] Autokey\n[6] Eulers\n[7] Shift\n[8] Get nth prime\n[9] Prime position\n[10] Direct Translation\n[99] Quit\nSelection: ")
        try:
            num = int(selection)
            if num == 99:
                break
            if num in range(11):
                result, decrypted_text = menu_choices(num, False)
                while result:
                    chain_select = input("Choose what to chain with (JSON not supported).\n[1] Use a JSON file (see example.json)\n[2] Crypto analysis (IoC, IC2, Frequency)\n[3] Vigenere\n[4] Atbash\n[5] Autokey\n[6] Eulers\n[7] Shift\n[8] Get nth prime\n[9] Prime position\n[10] Direct Translation\n[99] Quit\nSelection: ")
                    num2 = int(chain_select)
                    if num2 == 99:
                        break
                    if num2 in range(11):
                        result, decrypted_text = menu_choices(num2, True, decrypted_text)
                continue
                    
            else:
                continue
        except ValueError:
            print("\nPlease enter a valid number.\n")
            continue

if __name__ == "__main__":
    menu()