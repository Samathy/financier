# -*- coding: utf-8 -*-

import csv
import decimal
import json
import pathlib
import shutil

output_fieldnames = [ "date", "description", "in", "out", "balance", ]

temp_path = None 

def no_negatives(i):
    return i * -1


def remove(filename,  symbols):
    with open(filename, "r+") as document:
        data = document.read()
        for symbol in symbols:
            data = data.replace(symbol, "")
        document.seek(0)
        document.write(data)


def join_items(current_row, previous_row, input_data):
    output = ""
    for item in input_data:
        output = f"{output} {current_row[item]}"
    return output


def sum_previous(current, previous_row, input_data):
    if previous_row == None:
        previous_row = {input_data[0]:0}
    return str(decimal.Decimal(current[input_data[0]]) + decimal.Decimal(previous_row[input_data[0]]))

options_preopen = {
        "remove": remove
        }

functions = {
        "sum_previous": sum_previous,
        "join":join_items
        }

operations = {
        }

def headers_match_format(headers, format_json):
    if headers != list(key for key in format_json["fields"].keys() if key != "functions"):
        raise RuntimeError("CSV Headers dont match format")

def run_special(row, previous_row, functions_to_run, format_json):
    output = {}
    for function in functions_to_run:
        callable_f = functions[function["name"]]
        output[function["output"]] = callable_f(row, previous_row, function["input"])
    return output

def main(format_filename, filename, output_filename):

    temp_path = pathlib.Path("/tmp") / filename.name
    shutil.copyfile(filename, temp_path)

    with open(format_filename, "r",errors="ignore") as format_file:
        format_json = json.load(format_file)

    for option in options_preopen.keys():
        if option in format_json.get("options", []):
            options_preopen[option](temp_path,format_json["options"][option])

    functions_to_run = format_json["functions"]

    with open(temp_path, "r",) as document:
        document_csv = csv.DictReader(document)
        headers_match_format(document_csv.fieldnames, format_json)

        with open(output_filename, "w") as output_file:
            output_csv = csv.DictWriter(output_file, fieldnames=output_fieldnames)
            output_csv.writeheader()
            previous_row = None
            for row in document_csv:
                writeable_row = run_special(row, previous_row, functions_to_run, format_json)
                for key, value in row.items():
                    if format_json["fields"][key] in output_fieldnames:
                        writeable_row[format_json["fields"][key]]= value
                output_csv.writerow(writeable_row)
                previous_row = row 
