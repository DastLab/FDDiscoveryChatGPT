import sys
import argparse
import os
import pandas as pd
import numpy as np


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


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


def resultFile(file1, file2, rowFile1, rowFile2, uniqueFile2, supersets, subsets, err, err2, uniquesuperset,
               uniquesubset, tp,
               fp, fn, acc,
               prec, rec, f1score):
    result = ""
    result += file1 + "\t" + str(rowFile1) + "\n"
    result += file2 + "\t" + str(rowFile2) + " - (Unique: " + str(uniqueFile2) + ")\n"
    result += "Generalizzazioni\t" + str(subsets) + "\n"
    result += "Generalizzazioni (unique)\t" + str(uniquesubset) + "\n"
    result += "Specializzazioni\t" + str(supersets) + "\n"
    result += "Specializzazioni (unique)\t" + str(uniquesuperset) + "\n"
    result += "Errate (no gen/spec/comuni)\t" + str(err) + "\n"
    result += "Errate(no spec/comuni)\t" + str(err2) + "\n"
    result += "\n"
    result += "TP: " + str(tp) + "\n"
    result += "FP: " + str(fp) + "\n"
    result += "FN: " + str(fn) + "\n"
    result += "Accuracy: " + str(acc) + "\n"
    result += "Precision: " + str(prec) + "\n"
    result += "Recall: " + str(rec) + "\n"
    result += "F1 SCORE: " + str(f1score) + "\n"
    result += "----------------------------------------------------------\n"
    return result


def Average(lst):
    return sum(lst) / len(lst)


def format_number(val):
    return '{:.4f}'.format(val)


def completeOutput(file_vuoti, file_tot, accs, precs, recs, f1s):
    result = ""
    result += "File vuoti: " + str(file_vuoti) + "\n"
    result += "File con dipendenze: " + str(file_tot - file_vuoti) + "\n"
    result += "File totali: " + str(file_tot) + "\n"
    result += "Avg accuracy: " + str(Average(accs)) + "\n"
    result += "Avg precision: " + str(Average(precs)) + "\n"
    result += "Avg recall: " + str(Average(recs)) + "\n"
    result += "Avg F1 score: " + str(Average(f1s)) + "\n"
    return result


parser = argparse.ArgumentParser(description='Processa due file contenenti dipendenze funzionali.')
parser.add_argument('folder1', help="Cartella file dipendenze 1 *.txt")
parser.add_argument('folder2', help="Cartella file dipendenze 2 *.txt")
parser.add_argument('output', help="Cartella output")
parser.add_argument('--csv', dest="csv", help="Esporta csv (default false)", default=True, type=bool)

# Assumo che le dipendenze in tutti i file hanno la seguente configurazione A, B, C -> D
lhsAttrsSeparator = ", "
sideSeparator = " -> "
args = parser.parse_args()

folder_input_main = args.folder1
folder_input_test = args.folder2
csvprint = args.csv

if not os.path.isdir(folder_input_main):
    print("Cartella main non esistente")

if not os.path.isdir(folder_input_test):
    print("Cartella test non esistente")

folder_output = args.output
if not os.path.isdir(folder_output):
    os.mkdir(folder_output)

file_result_path = os.path.join(folder_output, "hyfd_" + os.path.basename(folder_input_test) + ".txt")

txt_main_files = [filename for filename in os.listdir(folder_input_main) if filename.endswith('.txt')]
file_count = 0
flie_vuoti = 0
accs = []
precs = []
recs = []
f1s = []

accsv = []
precsv = []
recsv = []
f1sv = []
result_file = ""
csvdata = []
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

    commonFds1 = []
    commonFds2 = []
    generalizzazioni = []
    specializzazioni = []
    numberFdsFile1 = len(fdsFile1)
    numberFdsFile2 = len(fdsFile2)


    fdsFile2 = unique(fdsFile2)
    uniquegptfd = len(fdsFile2)

    for fdF1 in fdsFile1:
        rhsCommon = (filter(lambda fd: fd["rhs"] == fdF1["rhs"], fdsFile2))
        for fdF2 in rhsCommon:
            checkF1inF2 = all(np.in1d(fdF1["lhs"], fdF2["lhs"]))
            checkF2inF1 = all(np.in1d(fdF2["lhs"], fdF1["lhs"]))

            if checkF1inF2 is True and checkF2inF1 is True:
                commonFds1.append(fdF1)
                commonFds2.append(fdF2)

    for fd in commonFds1:
        if fd in fdsFile1:
            fdsFile1.remove(fd)
    for fd in commonFds2:
        if fd in fdsFile2:
            fdsFile2.remove(fd)



    for fdF1 in fdsFile1:
        rhsCommon = (filter(lambda fd: fd["rhs"] == fdF1["rhs"], fdsFile2))
        for fdF2 in rhsCommon:
            checkF1inF2 = all(np.in1d(fdF1["lhs"], fdF2["lhs"]))
            checkF2inF1 = all(np.in1d(fdF2["lhs"], fdF1["lhs"]))
            if checkF1inF2 is True and checkF2inF1 is False:
                specializzazioni.append({
                    "firstFile": fdF1,
                    "secondFile": fdF2
                })
            elif checkF1inF2 is False and checkF2inF1 is True:
                generalizzazioni.append({
                    "firstFile": fdF1,
                    "secondFile": fdF2
                })



    errorset = []
    errorset2 = []
    tempsubset = list(map(lambda fd: fd["secondFile"], generalizzazioni))
    tempsuperset = list(map(lambda fd: fd["secondFile"], specializzazioni))
    for fd in fdsFile2:
        if fd not in tempsubset and fd not in tempsuperset:
            errorset.append(fd)
        if fd not in tempsuperset:
            errorset2.append(fd)

    coperte_spec = list(map(lambda fd: fd["firstFile"], specializzazioni))
    coperte_spec = unique(coperte_spec)

    uniquesuperset = unique(tempsuperset)
    uniquesubset = unique(tempsubset)
    errorset = unique(errorset)
    errorset2 = unique(errorset2)
    commonFds1 = unique(commonFds1)


    file_count += 1
    if numberFdsFile2 == 0:
        flie_vuoti += 1

    tp = len(commonFds1)
    fn = len(fdsFile1)
    fp = len(fdsFile2)
    if tp > 0:
        acc = tp / (tp + fn + fp)
        prec = tp / (tp + fp)
        rec = tp / (tp + fn)
        f1score = (2 * prec * rec) / (prec + rec)
    else:
        acc = 0
        prec = 0
        rec = 0
        f1score = 0

    accs.append(acc)
    precs.append(prec)
    recs.append(rec)
    f1s.append(f1score)

    tpv = tp + len(coperte_spec)
    fpv = len(errorset) + len(uniquesubset)
    fnv = numberFdsFile1 - tpv
    if tpv > 0:
        accv = tpv / (tpv + fnv + fpv)
        precv = tpv / (tpv + fpv)
        recv = tpv / (tpv + fnv)
        f1scorev = (2 * precv * recv) / (precv + recv)
    else:
        accv = 0
        precv = 0
        recv = 0
        f1scorev = 0

    accsv.append(accv)
    precsv.append(precv)
    recsv.append(recv)
    f1sv.append(f1scorev)

    csvdata.append({
        "alg": os.path.basename(folder_input_test).replace("result_", ""),
        "file": txt_file.replace(".txt", ""),
        "hyfd_fd": numberFdsFile1,
        "gpt_fd": numberFdsFile2,
        "gpt_fd(unique)": uniquegptfd,
        "generalizzazioni": len(generalizzazioni),
        "generalizzazioni(unique)": len(uniquesubset),
        "specializzazioni": len(specializzazioni),
        "specializzazioni(unique)": len(uniquesuperset),
        "hyfd_coperte_spec": len(coperte_spec),
        "errate(no coumuni/spec/gen)": len(errorset),
        "errate(no comuni/spec)": len(errorset2),
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "accuracy(min)": format_number(acc),
        "precision(min)": format_number(prec),
        "recall(min)": format_number(rec),
        "f1score(min)": format_number(f1score),
        "TP(valide)": tpv,
        "FP(valide)": fpv,
        "FN(valide)": fnv,
        "accuracy(valide)": format_number(accv),
        "precision(valide)": format_number(precv),
        "recall(valide)": format_number(recv),
        "f1score(valide)": format_number(f1scorev),
    })
    result_file += resultFile(
        file_main_path,
        file_test_path,
        numberFdsFile1,
        numberFdsFile2,
        uniquegptfd,
        len(specializzazioni),
        len(generalizzazioni),
        len(errorset),
        len(errorset2),
        len(uniquesuperset),
        len(uniquesubset),
        tp,
        fp, fn, acc, prec,
        rec, f1score)

result_file += completeOutput(flie_vuoti, file_count, accs, precs, recs, f1s)

with open(file_result_path, "w") as json_file_out:
    json_file_out.write(result_file)

if csvprint:
    csvFile = os.path.join(folder_output, "result.csv")
    df = pd.json_normalize(csvdata)
    df.to_csv(csvFile, index=False, mode="a", header=not os.path.exists(csvFile))
