#_*_coding=utf-8_*_
import pymongo as mg
import argparse
import os
import glob
import impact

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
    '-y',
    '--year',
    type=str,
    help='update impact factor of which year',
)
args = parser.parse_args()

df = impact.df


def update_if():
    host = 'mongodb://' + args.user + ':' + args.passwd + '@' + args.ip
    #* connect to database and collection
    col = mg.MongoClient(host).publication[args.collection]
    print('Using collection: ', args.collection)

    if args.year not in df.columns:
        raise ValueError(
            'No impact factor for given year, please check impact_df.xlsx for useable year.'
        )
    else:
        print('Updating all documents of year: ', args.year)
        query = {
            'PY': args.year,
        }
        projection = {
            '_id': 1,
            'JF': 1,
        }
        for doc in col.find(query, projection):
            col.update_one(
                {'_id': doc['_id']},
                {
                    '$set': {
                        'C2':
                        df[args.year].loc[df[df['periodical'] ==
                                             doc['JF']].index.values[0]]
                    },
                },
            )
        print('Updated.')


if __name__ == '__main__':
    update_if()