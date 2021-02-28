import csv
import argparse
import json
import pathlib

output_fieldnames = [ "date", "description", "in", "out", "balance", ]

def headers_match_format(headers, format_json):
    print(headers)
    if headers != list(format_json["fields"].keys()):
        raise RuntimeError("CSV Headers dont match format")

def main(format_filename, filename, output_filename):

    with open(format_filename, "r") as format_file:
        format_json = json.loads(format_file.read())

    with open(filename, "r") as document:
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", required=True, nargs=1, action="store")
    parser.add_argument("--filename", required=True, nargs=1, action="store")
    parser.add_argument("--output", required=False, nargs=1, action="store", default="output.csv")


    args = parser.parse_args()
    
    format_filename = pathlib.Path("./formats") / f"{args.format[0]}.json"
    filename = args.filename[0]
    output_filename = args.output[0]

    main(format_filename, filename, output_filename)
