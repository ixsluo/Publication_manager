#_*_coding:utf-8_*_
import glob
import os
import re
import read_tables

impact = read_tables.impact
istic = read_tables.istic

#cas = read_tables.cas


#& parse ris file
class Ris:
    #~ ris structure
    def __init__(self, file=None):
        self.records = []
        self.parse(file)
        #& Check doi and periodical full name
        for doc in self.records[:]:
            if len(doc['DO']) == 0:
                print('DOI must be given, please check ', doc)
                print('Pass to next document.')
                self.records.remove(doc)
            elif doc['JF'] not in impact['periodical'].values:
                print('Wrong periodical full name!!!    ', doc['JF'])
                print('Pass to next document.')
                self.records.remove(doc)
        #& Update impact factor and journal partition
        for doc in self.records:
            #! Add journal partition
            #~ istic partition
            doc['C1']['istic'] = istic['partition'].loc[istic[
                istic['periodical'] == doc['JF']].index.values[0]]
            #~ cas partition
            '''
            doc['C1']['cas'] = cas['partition'].loc[cas[
                cas['periodical'] == doc['JF']].index.values[0]]
            '''

            #! Add impact factor
            if doc['PY'] in impact.columns:
                #~ IF of the current year exist.
                if_year = doc['PY']
            elif str(int(doc['PY']) - 1) in impact.columns:
                #~ IF of the current year not exist, use IF of the last year.
                if_year = str(int(doc['PY']) - 1)
            else:
                #~ IF of the last year not exist, do not do anything.
                continue
            doc['C2'] = float(impact[if_year].loc[impact[
                impact['periodical'] == doc['JF']].index.values[0]])

    def parse(self, file):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if (len(line) == 0) or (line[0] in ['#', '!', '"', "'"]):
                    continue
                #~ find the index of split symbol
                split_index = re.search('[  -]', line).span()[0]
                key, value = line[:split_index], line[split_index + 3:]
                key, value = key.strip(), value.strip()
                self.parse_field(key, value)
                #print(key, value)

    def parse_field(self, key, value):
        if key == 'TY':
            # * initialize
            self.document = {
                'TY': '',
                'TI': '',  #~ Title
                'T1': '',  #~ Title in html format
                'AU': [],
                'A1': [],  #~ Primary authors
                'A0': [],  #~ Custom 1, corresponding author
                'JF': '',  #! Journal/Periodical name: full name
                'C1': {},  #~ Custom 1, journal partition
                'C2':
                '',  #~ Custom 2, impact factor. Not recommended to specify manually
                'JA': '',  #~ Journal standard abbreviation
                'PR': '',  #~ Pre-publish or not
                'PY': '',  #~ Publication year
                'MO': '',  #~ Month
                'DA': '',  #~ Date
                'Y1': '',  #~ Primary date
                'Y2': '',  #~ Access date
                'VL': '',  #~ Volume
                'IS': '',  #~ Issue
                'SP': '',  #~ Start page
                'EP': '',  #~ End page
                'DO': '',  #~ DOI
                'UR': '',  #~ URL
                'SN': '',  #~ ISBN/ISSN
                'AB': '',  #~ Abstract
                'N1': '',  #~ Notes
                'N2': '',  #~ Abstract
                'ID': '',  #~ Reference ID
            }
            self.document[key] = value
        elif key == 'TI':
            self.document[key] = value
        elif key == 'T1':
            self.document[key] = value
        elif key == 'AU':
            self.document[key].append(value)
        elif key == 'A1':
            self.document[key].append(value)
        elif key == 'A0':
            self.document[key].append(value)
        elif key == 'JF':
            self.document[key] = value.lower()
        elif key == 'C2':
            self.document[key] = value
        elif key == 'JA':
            self.document[key] = value
        elif key == 'PR':
            self.document[key] = value
        elif key == 'PY':
            self.document[key] = value
        elif key == 'MO':
            self.document[key] = value
        elif key == 'DA':
            self.document[key] = value
        elif key == 'Y1':
            self.document[key] = value
        elif key == 'Y2':
            self.document[key] = value
        elif key == 'VL':
            self.document[key] = value
        elif key == 'IS':
            self.document[key] = value
        elif key == 'SP':
            self.document[key] = value
        elif key == 'EP':
            self.document[key] = value
        elif key == 'DO':
            self.document[key] = value
        elif key == 'UR':
            self.document[key] = value
        elif key == 'SN':
            self.document[key] = value
        elif key == 'AB':
            pass
            #self.document[key] = value
        elif key == 'N1':
            self.document[key] = value
        elif key == 'N2':
            pass
            #self.document[key] = value
        elif key == 'ID':
            self.document[key] = value
        elif key == 'ER':
            self.records.append(self.document)
        else:
            print('Unknown field, ignore: ', key, value)


if __name__ == '__main__':
    file_list = glob.glob(os.path.join('.', 'data', '*.ris'))
    print(file_list)
    for file in file_list:
        documents = Ris(file).records
        for doc in documents:
            print(doc)