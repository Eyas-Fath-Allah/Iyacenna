import PyPDF2
import os


def get_pdf_files(path):
    files_path_with_new_file_name = {}
    pdf_files = [f for f in os.listdir(path) if os.path.splitext(f)[1] == '.pdf']
    for pdf_file in pdf_files:
        txt_file = pdf_file.replace('.pdf', '.txt')
        if txt_file not in os.listdir(path):
            new_file_name = os.path.splitext(pdf_file)[0]
            file_path = os.path.join(path, pdf_file)
            files_path_with_new_file_name[file_path] = new_file_name
    return files_path_with_new_file_name


def extract_all_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        all_text = []
        for i in range(len(reader.pages)):
            all_text.append(reader.pages[i].extract_text())
        text = " ".join(all_text)
        return text.splitlines(), text


def correct_the_errors(pdf_text, error_list):
    for error in error_list:
        for index, line in enumerate(pdf_text):
            if error in line:
                corrected_line = line.replace(error, '')
                pdf_text[index] = corrected_line
                break


def extract_search_dictionary_from_text(pdf_text, errors, search_dictionary, synonyms_dictionary):
    control_result = {}
    result = {}
    abnormals = {}
    correct_the_errors(pdf_text, errors)
    for key in search_dictionary.keys():
        for line in pdf_text:
            if key in line:
                # Correct errors using error_dictionary and error_dictionary2 :
                if key in error_dictionary.keys() and error_dictionary[key] in line:
                    continue
                # Correct error for ALANİN :
                if key == 'ALANİN' and ('FENİLALANİN' in line or 'AMİNOTRANSFERAZ' in line):
                    continue
                # Continue searching :
                index = line.index(key)
                if key in synonyms_dictionary.keys() and use_synonyms:
                    if convert_to_uppercase:
                        key1 = synonyms_dictionary[key].upper()
                    elif convert_to_lowercase:
                        key1 = synonyms_dictionary[key].lower()
                    else:
                        key1 = synonyms_dictionary[key]
                else:
                    if convert_to_uppercase:
                        key1 = key.upper()
                    elif convert_to_lowercase:
                        key1 = key.lower()
                    else:
                        key1 = key.title()
                result[key1] = line[: index - 1].replace(" ", "").replace(",", ".")
                control_result[key] = result[key1]
                if key in convert_list and '*' not in result[key1] and convert_1000:
                    result[key1] = 1000 * float(result[key1])
                    result[key1] = int(result[key1])
                    result[key1] = str(result[key1])
                if "*" in result[key1]:
                    result[key1] = result[key1].replace("*", "")
                    if key in convert_list and convert_1000:
                        result[key1] = 1000 * float(result[key1])
                        result[key1] = int(result[key1])
                        result[key1] = str(result[key1])
                    if prefix_with_asterisk:
                        result[key1] = f'* {result[key1]}'
                        abnormals[key1] = result[key1]
                    else:
                        abnormals[key1] = result[key1]
                    control_result[key] = result[key1]
                break
    return result, control_result, abnormals


def get_blood_gas(pdf_text, blood_gas_dict):
    for key in blood_gas_dict.keys():
        for line in pdf_text:
            if key in line:
                index = line.index(key)
                blood_gas_result[key] = line[: index - 1].replace(" ", "").replace(",", ".")
                break


def get_unavailable_tests(control_result, search_dictionary):
    unavailable_tests = []
    for i in search_dictionary:
        if i not in control_result.keys():
            unavailable_tests.append(i)
    return unavailable_tests


def last_key(dict):
    return list(dict.keys())[-1]


def multiple_error(text):
    x = False
    y = False
    z = False
    if 'İDRARDA KANTİTATIF AMINOASIT ANALIZI' in text:
        x = True
    if 'KARNİTİN/AÇİLKARNİTİN ANALİZİ' in text:
        y = True
    if 'BETA-AMİNOBUTİRİK ASİT' in text:
        z = True
    return x, y, z


def advanced_print(path, name, ver, pdf_text, dict, gas_dict, abnormals, error1, error2, error3):
    with open(f"{path}\\{name}.txt", "w", encoding='utf-8') as file:
        file.write(f'İyacenna {ver}\n\n')
        file.write(f'{pdf_text[0]}\n\n')
        # Print Blood Result.
        if just_print_the_abnormals:
            if abnormals:
                last_abnormal = last_key(abnormals)
                for key, value in abnormals.items():
                    if key != last_abnormal:
                        file.write(f"{key} {value}, ")
                    else:
                        file.write(f"{key} {value}\n")
        else:
            if dict:
                last = last_key(dict)
                for key, value in dict.items():
                    if key != last:
                        file.write(f"{key} {value}, ")
                    else:
                        file.write(f"{key} {value}\n")
        # Print Blood Gas Result.
        if gas_dict and print_blood_gases:
            last1 = last_key(gas_dict)
            file.write(f'Kan Gazları: ')
            for key1, value1 in gas_dict.items():
                if key1 != last1:
                    file.write(f"{key1} {value1}, ")
                else:
                    file.write(f"{key1} {value1}\n")
        if error1 and error2:
            file.write('\nhem "İDRARDA KANTİTATIF AMINOASIT ANALIZI" hem de "KARNİTİN/AÇİLKARNİTİN ANALİZİ" istenmiş.\nKontrol etmeniz gerekmektedir.')
        if error3:
            file.write('\npdf içinde "BETA-AMİNOBUTİRİK ASİT" vardır.')
        # Print the unavailable tests.
        if print_the_unavailable_tests:
            file.write('\n\n')
            if unavailable_tests:
                file.write('The Unavailable tests are:\n\n')
                for i in unavailable_tests:
                    file.write(f'{i} \n')
            else:
                file.write('All the tests are found!!\n\n')


# Control Panel:
folder_path = 'C:\\Users\\eyas4\\Desktop\\Test1\\İyacenna'
version = 'v.3.0.1-Pediatri-Metabolizma'
prefix_with_asterisk = True  # Default is True.
print_the_unavailable_tests = False  # Default is False.
use_synonyms = True  # Default is True.
print_blood_gases = True  # Default is True.
just_print_the_abnormals = False  # Default is False.
convert_to_uppercase = False  # Default is False.
convert_to_lowercase = False  # Default is False.
convert_1000 = True  # Default is True


search_dictionary = {
    'ÜRE': '', 'BUN': '', 'KREATİNİN': '', 'HGFH': '',
    'ÜRİK ASİT': '', 'SODYUM': '', 'POTASYUM': '',
    'KLOR': '', 'KALSİYUM': '', 'FOSFOR': '',
    'MAGNEZYUM': '', 'TOTAL PROTEİN': '', 'ALBÜMİN': '',
    'DİREKT BİLİRUBİN': '', 'TOTAL BİLİRUBİN': '',
    'İNDİREKT BİLİRUBİN': '', 'ASPARTAT AMİNOTRANSFERAZ': '',
    'ALANİN AMİNOTRANSFERAZ': '', 'ALKALEN FOSFATAZ': '', 'GAMMA GLUTAMİL TRANSFERAZ': '',
    'LAKTAT DEHİDROGENAZ': '', 'CRP': '', 'PROKALSİTONİN': '',
    'LÖKOSİT': '', 'ERİTROSİT': '', 'TROMBOSİT': '',
    'HEMOGLOBİN': '', 'HEMATOKRIT': '', 'NÖTROFIL SAYISI': '',
    'LENFOSIT SAYISI': '', 'MONOSIT SAYISI': '', 'EOZINOFIL SAYISI': '',
    'BAZOFIL SAYISI': '', 'INR': '', 'APTT': '', 'KREATİN KİNAZ': '', 'CK-MB': '', 'MİYOGLOBİN': '',
    'TROPONİN T': '', 'BNP': '', 'D-DİMER': '', 'FİBRİNOJEN': '', 'FERRİTİN': '',
    'TRİGLİSERİD': '', 'KOLESTEROL VLDL': '', 'HDL KOLESTEROL': '', 'TOTAL KOLESTEROL': '',
    'LDL KOLESTEROL': '', 'NON-HDL KOLESTEROL': '', 'UIBC': '', 'Transferrin Saturasyonu': '',
    'TOTAL DEMİR BAĞLAMA KAPASİTESİ': '', 'SERUM DEMİRİ': '', 'B12 VİTAMİNİ': '',
    'FOLİK ASİT': '', 'TSH': '', 'SERBEST T4': '', 'SERBEST T3': '', 'FOSFOETANOLAMİN': '', 'ASPARTİK ASİT': '',
    'TREONİN': '', 'SERİN': '', 'ASPARAJİN': '', 'GLUTAMİK ASİT': '', 'ALFA-AMİNOADİPİK ASİT': '', 'GLİSİN': '',
    'ALANİN': '', 'SİTRÜLİN': '', 'ALFA- AMİNOBÜTİRİK ASİT': '', 'VALİN': '', 'SİSTİN': '', 'SİSTATİONİN': '',
    'METİONİN': '', 'İZOLÖSİN': '', 'LÖSİN': '', 'TİROZİN': '', 'FENİLALANİN': '', 'GAMA-AMİNOBÜTİRİK ASİT': '',
    'HİSTİDİN': '', '3-METİLHİSTİDİN': '', '1-METİLHİSTİDİN': '', 'TRİPTOFAN': '', 'ANSERİN': '', 'ORNİTİN': '',
    'LİZİN': '', 'ARJİNİN': '', 'HİDROKSİPROLİN': '', 'PROLİN': '', 'İDRARDA  GLUTAMİN': '', 'ALLOİZOLOSİN': '',
    'KREATİNİN-SPOT İDRAR': '', 'İDRARDA PROTEİN SPOT / İDRARDA KREATİNİN': '', 'FOSFOR (P) SPOT İDRAR': '',
    'KALSİYUM-SPOT İDRAR': '', 'PROTEİN KANTİTATİF (İDRARDA)SPOT': '',
    'C0 SERBEST KARNİTİN': '', 'C2 ASETİL KARNİTİN': '', 'C3 PROPİYONİL KARNİTİN': '', 'C4 BÜTİRİL KARNİTİN': '',
    'C4DC METIL MALONIL KARNITIN': '', 'C5 İSOVALERİL KARNİTİN': '', 'C5:1 TİGLİL KARNİTİN': '',
    'C5 OH 3OH İSOVALERİL KARNİTİN': '', 'C5 DC GLUTARİL KARNİTİN': '', 'C6  HEKZANOİL KARNİTİN': '', 'C6DC ADIPIL KARNITIN': '',
    'C8 OKTANOİL KARNİTİN': '', 'C10 DEKANOİL KARNİTİN': '', 'C10:1 DEKENOİL KARNİTİN': '', 'C12 DODECANOİL KARNİTİN': '',
    'C14 MİYRİSTOİL KARNİTİN': '', 'C14:1': '', 'C14:2': '', 'C16 PALMİTOİL KARNİTİN': '', 'C16:1 PALMİTOİL KARNİTİN': '',
    'C18 STERAOİL KARNİTİN': '', 'C18:1 OLEİL KARNİTİN': '', 'C18:1 OH 3OH OLEİL KARNİTİN': '', 'C18:2 LİNOLEİL KARNİTİN': '',
    'C4-OH': '', 'C10:2': '', 'C16-OH': '', 'HOMOSİSTEİN': ''
}

blood_gas = {'PH': '', 'PC02': '', 'PO2': '', 'SO2': ''}

synonyms_dictionary = {
    'SODYUM': 'NA', 'POTASYUM': 'K', 'KALSİYUM': 'Ca', 'KLOR': 'Cl', 'FOSFOR': 'P', 'MAGNEZYUM': 'Mg',
    'ASPARTAT AMİNOTRANSFERAZ': 'AST', 'ALANİN AMİNOTRANSFERAZ': 'ALT', 'ALKALEN FOSFATAZ': 'ALP',
    'GAMMA GLUTAMİL TRANSFERAZ': 'GGT', 'LAKTAT DEHİDROGENAZ': 'LDH', 'LÖKOSİT': 'WBC', 'ERİTROSİT': 'RBC',
    'TROMBOSİT': 'PLT', 'HEMOGLOBİN': 'HB', 'HEMATOKRIT': 'Htc', 'KREATİN KİNAZ': 'CK',
    'NÖTROFIL SAYISI': 'TNS', 'LENFOSIT SAYISI': 'TLS', 'MONOSIT SAYISI': 'Monosit', 'EOZINOFIL SAYISI': 'Eozinofil',
    'BAZOFIL SAYISI': 'Bazofil', 'TOTAL DEMİR BAĞLAMA KAPASİTESİ': 'TDBK',
    'B12 VİTAMİNİ': 'B12', 'SERBEST T4': 'sT4', 'SERBEST T3': 'sT3', 'KOLESTEROL VLDL': 'VLD', 'LDL KOLESTEROL': 'LDL',
    'NON-HDL KOLESTEROL': 'NON-HDL', 'İDRARDA PROTEİN SPOT / İDRARDA KREATİNİN': 'İdrarda Protein Spot/İdrarda Kreatinin Spot'
}
# convert_list means (1000 * result)
convert_list = ['LÖKOSİT', 'TROMBOSİT', 'NÖTROFIL SAYISI', 'LENFOSIT SAYISI']

error_list = ['KAN GAZLARI+PH+NA+K+CA', 'SERUM DEMİRİ VE TOTAL DEMİR', '%SATURASYON (', 'KREATİNİN ÇOCUK (ADOLESAN',
              'PROTEİN/KREATİNİN (SPOT İDRAR)', 'KREATİNİN SPOT İDRAR']

error_dictionary = {
    'KREATİNİN': 'SPOT', 'FOSFOR': 'SPOT', 'KALSİYUM': 'SPOT', 'LÖSİN': 'İZOLÖSİN', 'PROLİN': 'HİDROKSİPROLİN'
    }
error_dictionary2 = {'İDRARDA KANTİTATIF AMINOASIT ANALIZI': '', 'KARNİTİN/AÇİLKARNİTİN ANALİZİ': '', 'BETA-AMİNOBUTİRİK ASİT': '' }



files_path_with_new_file_name = get_pdf_files(folder_path)
for pdf_file, name in files_path_with_new_file_name.items():
    blood_gas_result = {}
    pdf_text, text = extract_all_pdf_text(pdf_file)
    result, control_result, abnormals = extract_search_dictionary_from_text(pdf_text, error_list, search_dictionary,
                                                                            synonyms_dictionary)
    unavailable_tests = get_unavailable_tests(control_result, search_dictionary)
    get_blood_gas(pdf_text, blood_gas)
    x, y, z = multiple_error(text)

    advanced_print(folder_path, name, version, pdf_text, result, blood_gas_result, abnormals, x, y, z)
