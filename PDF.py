import PyPDF2


# Open and read a pdf file.
file = open("C:\\Users\\eyas4\\Desktop\\Test1\\Test1.pdf", 'rb')
reader = PyPDF2.PdfReader(file)

# Take all the text from this pdf file and put it in single string.
all_text = []
for i in range(len(reader.pages)):
    all_text.append(reader.pages[i].extract_text())
text = " ".join(all_text)

# Divide the string by lines and put every line in index in list.
splitted_text = text.splitlines()

# All the keywords, the default values is None.
search_dictionary = {
    'ÜRE': '', 'BUN': '', 'KREATİNİN': '', 'HGFH': '',
    'ÜRİK ASİT': '', 'SODYUM': '', 'POTASYUM': '',
    'KLORÜR': '', 'KALSİYUM': '', 'FOSFOR': '',
    'MAGNEZYUM': '', 'TOTAL PROTEİN': '', 'ALBÜMİN': '',
    'DİREKT BİLİRUBİN': '', 'TOTAL BİLİRUBİN': '',
    'İNDİREKT BİLİRUBİN': '', 'ASPARTAT AMİNOTRANSFERAZ': '',
    'ALANİN AMİNOTRANSFERAZ': '',
    'ALKALEN FOSFATAZ': '', 'GAMMA GLUTAMİL TRANSFERAZ': '',
    'LAKTAT DEHİDROGENAZ': '', 'CRP': '', 'PROKALSİTONİN': '',
    'LÖKOSİT': '', 'ERİTROSİT': '', 'TROMBOSİT': '',
    'HEMOGLOBİN': '', 'HEMATOKRIT': '', 'NÖTROFIL SAYISI': '',
    'LENFOSIT SAYISI': '', 'MONOSIT SAYISI': '', 'EOZINOFIL SAYISI': '',
    'BAZOFIL SAYISI': '', 'INR': '', 'APTT': ''
                    }

# Unavailable tests.
unavailable_tests = []

# Compare each keyword with all the lines.
for key in search_dictionary.keys():
    for line in splitted_text:
        if key in line:
            index = line.index(key)
            search_dictionary[key] = line[0: index - 1]
            search_dictionary[key] = search_dictionary[key].replace(" ", "")
            search_dictionary[key] = search_dictionary[key].replace(",", ".")
            if "*" in search_dictionary[key]:
                search_dictionary[key] = search_dictionary[key].replace("*", "")
                search_dictionary[key] = "* " + search_dictionary[key]
            break
    if search_dictionary[key] == '':
        unavailable_tests.append(key)

# Delete the unavailable tests from search_dictionary.
for i in unavailable_tests:
    if i in search_dictionary:
        del search_dictionary[i]

# Get the last key of the dictionary.
search_dictionary_list = list(search_dictionary.keys())
last_key = search_dictionary_list[-1]

# Print the dictionary indexes.
for key, value in search_dictionary.items():
    if key != last_key:
        print(f"{key} {value}, ", end="")
    else:
        print(f"{key} {value}.")


# Print the unavailable tests.
print()
if not unavailable_tests:
    print('All the tests are found!!')
else:
    print('The Unavailable tests are:')
    for i in unavailable_tests:
        print(i)
