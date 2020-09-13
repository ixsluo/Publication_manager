#_*_coding=utf-8_*_
import pymongo as mg
import argparse
import os
import glob
from inout import parse_document
import impact

def insert():
    parser = argparse.ArgumentParser(description='Insert documents from file')
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        help='which user to login mongodb, e.g. "publication_manager"',
        metavar='',
    )
    parser.add_argument(
        '-p',
        '--passwd',
        type=str,
        help='password of the user',
        metavar='',
    )
    parser.add_argument(
        '--ip',
        type=str,
        default="59.72.115.44:27017",
        help='host and port to connect, default "59.72.115.44:27017"',
        metavar='',
    )
    parser.add_argument(
        '-c',
        '--collection',
        type=str,
        help='which collection to use, e.g. "iccms"',
        metavar='',

    )
    parser.add_argument(
        '-f',
        '--file',
        type=str,
        help='file name or file name mode to insert, e.g. "data/*"',
        metavar='',
    )
    args = parser.parse_args()


    host = 'mongodb://' + args.user + ':' + args.passwd + '@' + args.ip
    # * connect to database and collection
    iccms = mg.MongoClient(host).publication[args.collection]

    f_list = glob.glob(args.file)

    print('Using collecton: ', args.collection)

    for file in f_list:
        print('parsing ', file)
        document, exitcode = parse_document(file)
        if exitcode == 0:
            pass
        elif exitcode == 1:
            print('Wrong periodical. Pass to the next document.')
            continue
        elif exitcode == 2:
            print('Impact factor not exist, please update impact_df.xlsx. Pass to \
    the next document.')
            continue
        else:
            pass


        # ? exist or not
        query = {
            "$or":[
                {"title": document['title']},
                {"doi": document['doi']}
            ]
        }

        if iccms.count_documents(query) != 0:
            print('same title or doi already exist, please check again or use \
    update instead of insert')
        else:
            print('New document')
            #iccms.insert_one(document)


if __name__ == '__main__':
    insert()