#_*_coding=utf-8_*_
import pymongo as mg
import argparse
import os
import glob
import read_tables

parser = argparse.ArgumentParser(
    description='Update impact factor from IF form.',
    fromfile_prefix_chars="@",
)
parser.add_argument(
    '-u',
    '--user',
    type=str,
    help='which user to login mongodb, e.g. "publication_manager"',
)
parser.add_argument(
    '-p',
    '--passwd',
    type=str,
    help='password of the user',
)
parser.add_argument(
    '--ip',
    type=str,
    default="59.72.115.44:27017",
    help='host and port to connect, default "59.72.115.44:27017"',
)
parser.add_argument(
    '-c',
    '--collection',
    type=str,
    help='which collection to use, e.g. "iccms"',
)
parser.add_argument(
    '--partition',
    type=str,
    help='which journal partition to update, istic or cas',
    choices=['istic', 'cas'],
)
args = parser.parse_args()

istic = read_tables.istic


def update_partition():
    host = 'mongodb://' + args.user + ':' + args.passwd + '@' + args.ip
    #* connect to database and collection
    col = mg.MongoClient(host).publication[args.collection]
    print('Using collection: ', args.collection)

    print('Updating all documents in collection: ', args.collection)
    query = {}
    projection = {
        '_id': 1,
        'JF': 1,
    }
    for doc in col.find(query, projection):
        key = 'C1.' + args.partition
        col.update_one(
            {'_id': doc['_id']},
            {
                '$set': {
                    key:
                    istic['partition'].loc[istic[istic['periodical'] ==
                                                 doc['JF']].index.values[0]]
                },
            },
        )
    print('Updated.')


if __name__ == '__main__':
    update_partition()