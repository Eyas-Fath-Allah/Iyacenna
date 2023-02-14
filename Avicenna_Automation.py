import PyPDF2
import copy
import os


file_paths_with_new_file_name = {}

folder_path = 'test_path'
for i in os.listdir(folder_path):
    if '.pdf' in i:
        new_file_name = i.replace('.pdf', '')
        file_path = f'{folder_path}\\{i}'
        file_paths_with_new_file_name[file_path] = new_file_name


# All the keywords, the default values is None.
search_dictionary = {
    'PH': '', 'ÜRE': '', 'BUN': '', 'KREATİNİN': '', 'HGFH': '',
    'ÜRİK ASİT': '', 'SODYUM': '', 'POTASYUM': '',
    'KLORÜR': '', 'KALSİYUM': '', 'FOSFOR': '',
    'MAGNEZYUM': '', 'TOTAL PROTEİN': '', 'ALBÜMİN': '',
    'DİREKT BİLİRUBİN': '', 'TOTAL BİLİRUBİN': '',
    'İNDİREKT BİLİRUBİN': '', 'ASPARTAT AMİNOTRANSFERAZ': '',
    'ALANİN AMİNOTRANSFERAZ': '', 'ALKALEN FOSFATAZ': '', 'GAMMA GLUTAMİL TRANSFERAZ': '',
    'LAKTAT DEHİDROGENAZ': '', 'CRP': '', 'PROKALSİTONİN': '',
    'LÖKOSİT': '', 'ERİTROSİT': '', 'TROMBOSİT': '',
    'HEMOGLOBİN': '', 'HEMATOKRIT': '', 'NÖTROFIL SAYISI': '',
    'LENFOSIT SAYISI': '', 'MONOSIT SAYISI': '', 'EOZINOFIL SAYISI': '',
    'BAZOFIL SAYISI': '', 'INR': '', 'APTT': '', 'CK-MB': '', 'MİYOGLOBİN': '',
    'TROPONİN T': '', 'BNP': '', 'D-DİMER': '', 'FİBRİNOJEN': '', 'FERRİTİN': '',
    'TRİGLİSERİD': '', 'KOLESTEROL VLDL': '', 'HDL KOLESTEROL': '', 'TOTAL KOLESTEROL': '',
    'LDL KOLESTEROL': '', 'NON-HDL KOLESTEROL': '', 'UIBC': '', 'Transferrin Saturasyonu': '',
    'TOTAL DEMİR BAĞLAMA KAPASİTESİ': '', 'SERUM DEMİRİ': '', 'B12 VİTAMİNİ': '',
    'FOLİK ASİT': '', 'TSH': '', 'SERBEST T4': '', 'SERBEST T3': '',
                    }

# dictionary for synonyms.
synonyms_dictionary = {
    'SODYUM': 'NA+', 'POTASYUM': 'K+', 'KALSİYUM': 'CA2+'
                        }


for file_path, new_file_name in file_paths_with_new_file_name.items():

    # Open and read a pdf file.
    file = open(file_path, 'rb')
    reader = PyPDF2.PdfReader(file)

    # Take all the text from this pdf file and put it in single string.
    all_text = []
    for i in range(len(reader.pages)):
        all_text.append(reader.pages[i].extract_text())
    text = " ".join(all_text)

    # Divide the string by lines and put every line in index in list.
    splitted_text = text.splitlines()

    # Unavailable tests.
    unavailable_tests = []

    new_search_dictionary = {}
    # Compare each keyword with all the lines.
    for key in search_dictionary.keys():
        for line in splitted_text:
            if 'KAN GAZLARI' in line:
                line = ''
            if 'SERUM DEMİRİ VE TOTAL DEMİR' in line:
                line = ''
            if 'Transferrin Saturasyonu' in line:
                line = line.replace('%SATURASYON (', '')
            if key in line:
                index = line.index(key)
                new_search_dictionary[key] = line[: index - 1]
                new_search_dictionary[key] = new_search_dictionary[key].replace(" ", "")
                new_search_dictionary[key] = new_search_dictionary[key].replace(",", ".")
                if "*" in new_search_dictionary[key]:
                    new_search_dictionary[key] = new_search_dictionary[key].replace("*", "")
                    new_search_dictionary[key] = "* " + new_search_dictionary[key]
                break

    # Get the unavilable test:
    for i in search_dictionary:
        if i not in new_search_dictionary.keys():
            unavailable_tests.append(i)

    # Delete the available synonyms from the unavilable_tests list.
    unavailable_tests_copy = copy.copy(unavailable_tests)
    for i in unavailable_tests_copy:
        if i in synonyms_dictionary.values() or i in synonyms_dictionary.keys():
            unavailable_tests.remove(i)
            continue

    # Get the last key of the dictionary.
    new_search_dictionary_list = list(new_search_dictionary.keys())
    if new_search_dictionary_list:
        last_key = new_search_dictionary_list[-1]
    else:
        last_key = ''

    with open(f"{folder_path}\\{new_file_name}.txt", "w", encoding='utf-8') as file:
        # Print the dictionary indexes:
        for key, value in new_search_dictionary.items():
            if key != last_key:
                file.write(f"{key} {value}, ")
            else:
                file.write(f"{key} {value}.\n")

        # Print the unavailable tests.
        file.write('\n')
        if not unavailable_tests:
            file.write('All the tests are found!!\n')
        else:
            file.write('The Unavailable tests are:\n')
            for i in unavailable_tests:
                file.write(f'{i} \n')
