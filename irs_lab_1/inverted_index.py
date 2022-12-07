import argparse

import toolset

DATABASE_PATH = '.tmp/inverted_index.json'

def index(indexed_file_loc, db_file_loc):
    text = toolset.read_txt(indexed_file_loc)
    tokens = toolset.tokenize(text)
    db = toolset.read_db(db_file_loc)
    for token in tokens:
        if token not in db:
            db[token] = []
        if indexed_file_loc not in db[token]:
            db[token].append(indexed_file_loc)
    toolset.write_db(file_loc=db_file_loc, data=db)
    print("indexed successfully!")

def search(query, db_file_loc):
    query = toolset.tokenize(query)
    db = toolset.read_db(db_file_loc)
    result = {}
    for token in query:
        if token in db:
            result[token] = db[token]
        else:
            result[token] = []
        
    return result

def print_search_result(result):
    for token in result:
        if len(result[token]) == 0:
            print(f'"{token}": not found')
            continue
        print(f'"{token}": {result[token]}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--index',
        nargs='?',
        type=str,
        help='file to index'
    )
    parser.add_argument(
        '--search',
        nargs='?',
        type=str,
        help='search string'
    )
    parser.add_argument(
        '--db',
        nargs='?',
        type=str,
        default=DATABASE_PATH,
        help='database file'
    )
    args = parser.parse_args()

    if not args.index and not args.search:
        print('please, specify a command to complete. for information see --help.')
        return
    if args.index:
        index(args.index, args.db)
    if args.search:
        result = search(args.search, args.db)
        print_search_result(result)


if __name__ == "__main__":
    main()