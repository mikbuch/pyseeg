'''
    csv module for reading csv file to the 2D list

    Default mode is 'rb'
    Default delimiter is ',' and the quotechar '|'
    # # #

    arguments:
        csv_file - read csv file name
        coma - if True replaces all the comas with dots in the particular cells
        header - specify how many lines (from the begining) are to be removed
    # # #

    example use:

        import read_csv

        some_list = read_csv.read(example.csv)
        other_list = read_csv.read(example.csv, header=5)

'''

import csv


def read(
        csv_file,
        comas=True,
        delimiter=',',
        header=None,
        mode='rb',
        quotechar='|'
        ):

    data = []

    print('init')
    if len(delimiter) > 1:
        data = advanced(
            csv_file,
            comas=comas,
            data=data,
            delimiter=delimiter,
            mode=mode)
    else:
        data = basic(
            csv_file=csv_file,
            comas=comas,
            data=data,
            delimiter=delimiter,
            mode=mode,
            quotechar=quotechar
            )
    if header is not None:
        data = data[header:]
    return data


def basic(
        csv_file,
        data,
        comas=False,
        delimiter=',',
        mode='rb',
        quotechar='|'
        ):
    with open(csv_file, mode) as csv_file:
        csv_reader = csv.reader(
            csv_file,
            delimiter=delimiter,
            quotechar=quotechar
            )
        for row_list in csv_reader:
            if comas:
                # change comas to dots
                row_list = [i.replace(',', '.') for i in row_list]
            data.append(row_list)
    return data


def advanced(
        csv_file,
        data,
        delimiter=', ',
        comas=True,
        mode='rb'
        ):

    with open(csv_file, mode) as f:
        for line in f:
            # remove new line character
            line = line.rstrip('\n')
            # split to cells accordingly to the double delimiter
            line = line.split(delimiter)
            if comas:
                # change comas to dots
                line = [i.replace(',', '.') for i in line]
            data.append(line)
    return data
