#_*_coding=utf-8_*_
import pymongo as mg
import argparse
import os
import glob
from inout import Ris
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
    #* connect to database and collection
    col = mg.MongoClient(host).publication[args.collection]

    file_list = glob.glob(args.file)

    print('Using collection: ', args.collection)

    for file in file_list:
        print('parsing ', file)
        documents = Ris(file).records
        for doc in documents:
            #? exist or not
            query = {
                "$or":[
                    {"TI": doc['TI']},
                    {"DO": doc['DO']},
                ]
            }

            if col.count_documents(query) != 0:
                print('same title or doi already exist, please check again or use update instead of insert, doi: ', doc['DO'])
            else:
                print('New document')
                col.insert_one(doc)


if __name__ == '__main__':
    insert()