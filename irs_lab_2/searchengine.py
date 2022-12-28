import re
import os
import argparse
import bbc_feeds

stories = bbc_feeds.news().all(limit=20)

bbc_news_collection = {}
for story in stories:
    if story.title not in bbc_news_collection.keys():
        bbc_news_collection[story.title] = story.summary


class Storage:
    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, self_id):
        return self.db.get(self_id, None)

    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)


def get_files_list(dir):
    files_array = []

    for file in os.listdir('{dir}/'.format(dir=dir)):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'data/{file}'.format(file=file))
        files_array.append(file_name)
        # files_array.append(file)

    return files_array


def get_bbc_titles():
    titles_array = []
    for title in bbc_news_collection:
        titles_array.append(title)
    return titles_array


def get_files_text(dir):
    inc = 1
    doc = {}
    for file in os.listdir('{dir}/'.format(dir=dir)):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, '{dir}/{file}'.format(file=file, dir=dir))
        file_handle = open(file_name)
        content = file_handle.read()
        clean_content = re.sub(r'[^\w\s]', '', content)
        if '\n' in clean_content:
            text = clean_content.split('\n')[0]
        elif '.' in clean_content:
            text = clean_content.split('.')[0]
        else:
            text = clean_content
        file_handle.close()
        if file_name not in doc.keys():
            doc[file_name] = text
        inc += 1
    return doc


def index_title_from_dir():
    list_of = get_files_text('data')
    res_dict = {}
    truncate_num = 50

    for key in list_of.keys():
        if key not in res_dict.keys():
            if len(list_of[key]) >= truncate_num:
                new_str = list_of[key][0:truncate_num]
                res_dict[key] = new_str + '…'
            else:
                res_dict[key] = list_of[key]
    return res_dict


def format_output_from_dir(obj):
    title = index_title_from_dir()
    inc = 1

    formatted_obj = {}
    for item in obj.keys():
        for value in obj[item]:
            if value in title.keys():
                formatted_obj[title[value]] = value

    for el in formatted_obj:
        print(str(inc) + '. Title: ' + el + ', File: ' + formatted_obj[el])
        inc += 1


def format_output_from_bbc(obj):
    inc = 1
    formatted_obj = {}
    for title in obj:
        if title not in formatted_obj.keys():
            formatted_obj[title] = bbc_news_collection[title]

    test = []
    for el in formatted_obj:
        # TODO {1. Title: 'title', File: 'file'}
        # print(str(inc) + '. Title: ' + el + ', Content: ' + formatted_obj[el])
        # TODO [{1. Title: 'title', File: 'file'}]
        test.append({str(inc): '. Title: ' + el + ', Content: ' + formatted_obj[el]})
        # TODO [{title: 'title'}]
        # test.append({'title': el})
        inc += 1

    return test


class InvertedIndex:
    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        clean_text = re.sub(r'[^\w\s]', '', document['text']).lower()
        terms = clean_text.replace('\n', ' ').split(' ')
        appearances_dict = dict()

        for term in terms:
            appearances_dict[term] = get_files_list('data')[int(document['id']) - 1]

        # Update index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }

        self.index.update(update_dict)
        # print(update_dict)

        # Add into the database
        self.db.add(document)
        return document

    def index_bbc_news(self, document):
        clean_text = re.sub(r'[^\w\s]', '', document['text']).lower()
        terms = clean_text.replace('\n', ' ').split(' ')
        appearances_dict = dict()

        for term in terms:
            appearances_dict[term] = get_bbc_titles()[int(document['id']) - 1]

        # Update index
        update_dict = {
            key: [appearance]
            if key not in self.index
            else self.index[key] + [appearance]
            for (key, appearance) in appearances_dict.items()
        }

        self.index.update(update_dict)
        # print(update_dict)

        # Add into the database
        self.db.add(document)
        return document

    def lookup_query_from_dir(self, query):
        if query == '':
            return []
        clean_text = re.sub(r'd+[^\w\s]', '', query).lower().strip()
        indexed_obj = {term: self.index[term] for term in clean_text.split(' ') if term in self.index}

        if not bool(indexed_obj):
            return "\033[1;32;40m {term} not found \033[0;0m".format(term=query)
            # return []
        return indexed_obj

    def lookup_query_from_bbc(self, query):
        if query == '':
            return []
        clean_text = re.sub(r'd+[^\w\s]', '', query).lower().strip()
        indexed_obj = {term: self.index[term] for term in clean_text.split(' ') if term in self.index}
        if not bool(indexed_obj):
            # return "\033[1;32;40m {term} not found \033[0;0m".format(term=query)
            return []
        return indexed_obj[query]


def index_file_from_dir(index):
    inc = 1
    for x in os.listdir('data/'):
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, 'data/{file}'.format(file=x))
        file_handle = open(file_name)
        tst = file_handle.read()
        file_handle.close()

        doc = {'id': str(inc), 'text': tst}
        index.index_document(doc)
        inc += 1


def index_file_from_bbc(index):
    inc = 1
    for title in bbc_news_collection:
        doc = {'id': str(inc), 'text': bbc_news_collection[title]}
        index.index_bbc_news(doc)
        inc += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--index_files',
        nargs='?',
        type=str,
        help='search from dir files'
    )
    parser.add_argument(
        '--search_bbc',
        nargs='?',
        type=str,
        help='search from bbc news'
    )
    args = parser.parse_args()

    if not args.index_files and not args.search_bbc:
        print('please, specify a command to complete. for information see --help.')
        return
    if args.index_files:
        db = Storage()
        index = InvertedIndex(db)
        index_file_from_dir(index)
        if args.index_files == '':
            print('please, specify a query to index/search from dir files')
            return
        index_res = index.lookup_query_from_dir(args.index_files)
        print('Results for query "{term}":'.format(term=args.index_files))
        format_output_from_dir(index_res)
    if args.search_bbc:
        db = Storage()
        index = InvertedIndex(db)
        index_file_from_bbc(index)

        index_res = index.lookup_query_from_bbc(args.search_bbc)
        # print('Results for query "{term}":'.format(term=args.search_bbc))
        return print(format_output_from_bbc(index_res))


if __name__ == "__main__":
    main()
