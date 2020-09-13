#_*_coding:utf-8_*_
import glob
import os
import re
import impact

df = impact.df

# & parse documents
def parse_document(filename):
    exitcode = 0  # ^ exit code
    document = {
        'title': '',
        'all_author': [],
        'first_author': [],
        'commun_author': [],
        'periodical': '',
        'if': '',
        'publish_year': '',
        'date': '',
        'accept_year': '',
        'volume': '',
        'issue': '',
        'doi': '',
        'url': '',
    }
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            # ~ jump comment line or blank line
            if (len(line) == 0) or (line[0] in ['#', '!', '"', "'"]):
                continue
            # ~ split by any blank but at least one \t
            key, value = re.split(r'\s*\t\s*', line)
            key = key.strip(':').lower()  # remove ':'
            if key == 'title':
                document['title'] = value
            elif key == 'all_author':
                document['all_author'].append(value)
            elif key == 'first_author':
                document['first_author'].append(value)
            elif key == 'commun_author':
                document['commun_author'].append(value)
            elif key == 'periodical':
                document['periodical'] = value.lower()
            elif key == 'if':
                document['if'] = value
            elif key == 'publish_year':
                document['publish_year'] = value
            elif key == 'date':
                document['date'] = value
            elif key == 'accept_year':
                document['accept_year'] = value
            elif key == 'volume':
                document['volume'] = value
            elif key == 'issue':
                document['issue'] = value
            elif key == 'doi':
                document['doi'] = value
            elif key == 'url':
                document['url'] = value
            else:
                print('Unknown field, ignore: ', line)

        if document['periodical'] not in df['periodical'].values:
            # ! Wrong periodical, pass to next document
            exitcode = 1
        else:
            # ~ IF of the current year exist
            if document['publish_year'] in df.columns:  
                if_year = document['publish_year']
            # ~ IF of the current year not exist, use IF of the last year
            elif str(int(document['publish_year']) - 1) in df.columns:
                if_year = str(int(document['publish_year']) - 1)
            # ~ IF of the last year not exist
            else:
                exitcode = 2
                return document, exitcode

            document['if'] = df[if_year].loc[
                df[df['periodical'] == document['periodical']].index.values[0]
            ]

    return document, exitcode


if __name__ == '__main__':
    doc_list = glob.glob('./data/1.txt')
    print(doc_list)
    for doc in doc_list:
        document = parse_document(doc)
        print(document)