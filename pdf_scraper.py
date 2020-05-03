#!/usr/bin/env python3
import PyPDF2
import re
import os
import csv
from pprint import pprint

inputdir = './input/'
inputfile = './in.txt'
outputfile = './out.csv'


def main():
    # txt file with invoice ids
    with open(inputfile, 'r') as f:
        invoice_list = f.read().splitlines()

    # build empty dict
    d = {}
    for regex_pattern in invoice_list:
        d[regex_pattern] = []

    file_total = len(os.listdir(inputdir))
    file_number = 1
    for filename in os.listdir(inputdir):
        if re.search(r'\.pdf$', filename):
            file_number += 1
            print(f'Scanning {file_number}/{file_total}: {filename}')

            # open the pdf file
            object = PyPDF2.PdfFileReader(inputdir + filename)

            # get number of pages
            NumPages = object.getNumPages()

            for regex_pattern in invoice_list:
                # extract text and do the search
                text = ''
                for i in range(0, NumPages):
                    PageObj = object.getPage(i)
                    # print("this is page " + str(i))
                    text += PageObj.extractText()
                    # print(text)
                result = re.search(regex_pattern, text)
                if result:
                    # print(f'{regex_pattern}\t{filename}')
                    l = d.get(regex_pattern)
                    if filename not in l:
                        l.append(filename)
                    d[regex_pattern] = l
    if d:
        pprint(d)
        f_write_to_csv(d)


def f_write_to_csv(d):
    with open(outputfile, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['Invoice', 'Filename'])
        for invoice in d:
            filename_str = ''
            for filename in d[invoice]:
                filename_str += filename + ' '
            filename_str.rstrip()

            writer.writerow([invoice, filename_str])


if __name__ == '__main__':
    main()
