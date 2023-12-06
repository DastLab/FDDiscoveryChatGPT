import sys
import argparse
import os


def readRows(file):
    rows = []
    with open(file, 'r') as text:
        for line in text:
            rows.append(line.strip())
    return rows


def splitRow(row, ssSeparator, alsSeparator):
    lhs, rhs = row.split(ssSeparator)
    rhs = rhs.strip()
    lhs = lhs.split(alsSeparator)
    lhs = list(filter(None, lhs))
    lhs = list(map(str.strip, lhs))
    return {"lhs": lhs, "rhs": rhs}


def splitRows(rows, ssSeparator, alsSeparator):
    result = []
    for row in rows:
        result.append(splitRow(row, ssSeparator, alsSeparator))
    return result


def generateStringFromFD(fd):
    return ", ".join(fd["lhs"]) + " -> " + fd["rhs"]


def generateStringFromFDs(fds):
    toret = ""
    for x in fds:
        toret += generateStringFromFD(x) + "\n"
    return toret


def generateStringFromSuperSubSet(fds):
    toret = ""
    for x in fds:
        toret += (generateStringFromFD(x["firstFile"]) + " | " + generateStringFromFD(x["secondFile"]) + "\n")
    return toret


def writeOutput(nameFile1, nameFile2, outfile, nfds1, nfds2, commonFds, fds1, fds2, splus, smins, errorset):
    writeString = 'Differenze ' + nameFile1 + ' - ' + nameFile2 + '\n'
    writeString += 'Righe ' + nameFile1 + ': ' + str(nfds1) + '\n'
    writeString += 'Righe ' + nameFile2 + ': ' + str(nfds2) + '\n'
    writeString += '---------------- FDs COMUNI: ' + str(len(commonFds)) + ' -------------------\n'
    writeString += generateStringFromFDs(commonFds)
    writeString += '---------------- FDs RESTANTI ' + nameFile1 + ': ' + str(len(fds1)) + ' -------------------\n'
    writeString += generateStringFromFDs(fds1)
    writeString += '---------------- FDs RESTANTI ' + nameFile2 + ': ' + str(len(fds2)) + ' -------------------\n'
    writeString += generateStringFromFDs(fds2)
    writeString += '---------------- LHS IN ' + nameFile1 + ' SOTTOINSIEME DI LHS IN ' + nameFile2 + ': ' + str(
        len(smins)) + ' -------------------\n'
    writeString += generateStringFromSuperSubSet(smins)
    writeString += '---------------- LHS IN ' + nameFile1 + ' SOVRAINSIEME DI LHS IN ' + nameFile2 + ': ' + str(
        len(splus)) + ' -------------------\n'
    writeString += generateStringFromSuperSubSet(splus)
    writeString += '---------------- ERRATE IN ' + nameFile2 + ': ' + str(
        len(errorset)) + ' -------------------\n'
    writeString += generateStringFromFDs(errorset)
    with open(outfile, "w") as json_file_out:
        json_file_out.write(writeString)


parser = argparse.ArgumentParser(description='Processa due file contenenti dipendenze funzionali.')
parser.add_argument('folder1', help="Cartella file dipendenze 1 *.txt")
parser.add_argument('folder2', help="Cartella file dipendenze 2 *.txt")
parser.add_argument('output', help="Cartella output")

# Assumo che le dipendenze in tutti i file hanno la seguente configurazione A, B, C -> D
lhsAttrsSeparator = ", "
sideSeparator = " -> "
args = parser.parse_args()

folder_input_main = args.folder1
folder_input_test = args.folder2

if not os.path.isdir(folder_input_main):
    print("Cartella main non esistente")

if not os.path.isdir(folder_input_test):
    print("Cartella test non esistente")

folder_output = args.output
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)

file_result_path = os.path.join(folder_output, "hyfd_" + os.path.basename(folder_input_test))
if not os.path.isdir(file_result_path):
    os.mkdir(file_result_path)

txt_main_files = [filename for filename in os.listdir(folder_input_main) if filename.endswith('.txt')]
for txt_file in txt_main_files:

    file_test_path = os.path.join(folder_input_test, txt_file)
    if not os.path.exists(file_test_path):
        print("Il file " + file_test_path + " non esiste")
        continue
    file_main_path = os.path.join(folder_input_main, txt_file)

    print(file_main_path, "\t", file_test_path)
    rowsFile1 = readRows(file_main_path)
    rowsFile2 = readRows(file_test_path)
    fdsFile1 = (splitRows(rowsFile1, sideSeparator, lhsAttrsSeparator))
    fdsFile2 = (splitRows(rowsFile2, sideSeparator, lhsAttrsSeparator))

    # 2 liste perchè il lhs potrebbe avere ordinamento diverso e non funzionerebbe il remove
    commonFds1 = []
    commonFds2 = []
    subsets = []
    superset = []
    numberFdsFile1 = len(fdsFile1)
    numberFdsFile2 = len(fdsFile2)

    for fdF1 in fdsFile1:
        rhsCommon = (filter(lambda fd: fd["rhs"] == fdF1["rhs"], fdsFile2))
        for fdF2 in rhsCommon:
            checkF1inF2 = all(item in fdF1["lhs"] for item in fdF2["lhs"])
            checkF2inF1 = all(item in fdF2["lhs"] for item in fdF1["lhs"])
            if checkF1inF2 is True and checkF2inF1 is True:
                commonFds1.append(fdF1)
                commonFds2.append(fdF2)
            elif checkF1inF2 is True and checkF2inF1 is False:
                superset.append({
                    "firstFile": fdF1,
                    "secondFile": fdF2
                })
            elif checkF1inF2 is False and checkF2inF1 is True:
                subsets.append({
                    "firstFile": fdF1,
                    "secondFile": fdF2
                })

    for fd in commonFds1:
        if fd in fdsFile1:
            fdsFile1.remove(fd)

    for fd in commonFds2:
        if fd in fdsFile2:
            fdsFile2.remove(fd)

    errorset = []
    tempsubset = list(map(lambda fd: fd["secondFile"], subsets))
    tempsuperset = list(map(lambda fd: fd["secondFile"], superset))
    for fd in fdsFile2:
        if fd not in tempsubset and fd not in tempsuperset:
            errorset.append(fd)

    result_file = os.path.join(file_result_path, txt_file)

    writeOutput(file_main_path, file_test_path, result_file, numberFdsFile1, numberFdsFile2, commonFds1, fdsFile1,
                fdsFile2,
                superset, subsets, errorset)
