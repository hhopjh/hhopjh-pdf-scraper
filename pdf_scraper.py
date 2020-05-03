#!/usr/bin/env python3
import PyPDF2
import re
import os
import csv
from pprint import pprint
import multiprocessing as mp

inputdir = './input/'
inputfile = './in.txt'
outputfile = './out.csv'
outputfile_failed = './out_failed.csv'


def worker(filename):
    l = []
    if re.search(r'\.pdf$', filename):
        # print(f'Scanning {file_number}/{file_total}: {filename}')

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
            # result = re.search(regex_pattern, text)
            # if result:
            if regex_pattern in text:
                # print(f'{regex_pattern}\t{filename}')
                # l = d.get(regex_pattern)
                # if filename not in l:
                #     l.append(filename)
                # d[regex_pattern] = l
                l.append(regex_pattern)
    return (filename, l)


def main():
    global invoice_list
    # txt file with invoice ids
    with open(inputfile, 'r') as f:
        invoice_list = f.read().splitlines()

    # empty list for fail files:
    fail_files = []

    # build empty dict for success matches
    d = {}
    for regex_pattern in invoice_list:
        d[regex_pattern] = []

    file_total = len(os.listdir(inputdir))
    file_number = 0

    p = mp.Pool()
    for file, result in p.imap_unordered(worker, os.listdir(inputdir)):
        file_number += 1
        print(f'Scanning {file_number}/{file_total} ', end='')
        print(f'{file}: {result}')
        if result:
            for e in result:
                d[e].append(file)
        else:
            fail_files.append(file)

    if d:
        pprint(d)
        f_write_to_csv(d)
        f_write_fail_to_csv(fail_files)

        input('Success!')


def f_write_to_csv(d):
    with open(outputfile, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['sep=,'])
        writer.writerow(['Invoice', 'Filename'])

        for invoice in d:
            l = [invoice]
            l.extend(d[invoice])
            writer.writerow(l)


def f_write_fail_to_csv(l):
    with open(outputfile_failed, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(['sep=,'])
        writer.writerow(['Failed'])
        for file in l:
            writer.writerow([file])


if __name__ == '__main__':
    main()
