# -*- coding: utf-8 -*-
import csv
import json
import pathlib
import shutil

output_fieldnames = [ "date", "description", "in", "out", "balance", ]

temp_path = None 

def remove(filename,  symbols):
    with open(filename, "r+") as document:
        data = document.read()
        for symbol in symbols:
            data = data.replace(symbol, "")
        document.seek(0)
        document.write(data)


options_preopen = {
        "remove": remove
        }


def headers_match_format(headers, format_json):
    if headers != list(format_json["fields"].keys()):
        raise RuntimeError("CSV Headers dont match format")

def main(format_filename, filename, output_filename):

    temp_path = pathlib.Path("/tmp") / filename.name
    shutil.copyfile(filename, temp_path)

    with open(format_filename, "r",errors="ignore") as format_file:
        format_json = json.load(format_file)

    for option in options_preopen.keys():
        if option in format_json["options"]:
            options_preopen[option](temp_path,format_json["options"][option])

    with open(temp_path, "r",) as document:
        document_csv = csv.DictReader(document)

        headers_match_format(document_csv.fieldnames, format_json)

        with open(output_filename, "w") as output_file:
            output_csv = csv.DictWriter(output_file, fieldnames=output_fieldnames)
            output_csv.writeheader()
            for row in document_csv:
                writeable_row = {}
                for key, value in row.items():
                    if format_json["fields"][key] in output_fieldnames:
                        writeable_row[format_json["fields"][key]]= value
                output_csv.writerow(writeable_row)
