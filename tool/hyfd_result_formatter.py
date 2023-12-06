import os
import argparse
import json

parser = argparse.ArgumentParser(description='Formatta i file json risultanti da hyfd.py')
parser.add_argument('input_folder', help="Folder input")
parser.add_argument('output_folder', help="Folder output")

args = parser.parse_args()
folder_input = args.input_folder
folder_output = args.output_folder
if not os.path.isdir(folder_input):
    print("Input folder non esiste")

if not os.path.isdir(folder_output):
    os.mkdir(folder_output)

json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.json')]
for json_file_name in json_file_names:
    old = os.path.join(folder_input, json_file_name)
    new = os.path.join(folder_input, json_file_name.split('-')[0]+".json")
    os.rename(old, new)

json_file_names = [filename for filename in os.listdir(folder_input) if filename.endswith('.json')]
for json_file_name in json_file_names:
    with open(os.path.join(folder_input, json_file_name)) as json_file:
        json_text = json.load(json_file)
        toFlush = ""
        for fd in json_text:
            for rhs in fd[1]:
                toFlush += (", ".join(map(str, fd[0])) + " -> " + str(rhs) + "\n")
        with open(os.path.join(folder_output, json_file_name.replace("json", "txt")), "w") as json_file_out:
            json_file_out.write(toFlush)
