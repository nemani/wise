import sys
import os.path
from wise.index import InvertedIndex

if __name__ == '__main__':

    wikidump_path = os.path.abspath(sys.argv[1])
    index_dir_path = os.path.abspath(sys.argv[2])

    print("Wiki Dump Path {}".format(wikidump_path))
    print("Index will be saved in {}".format(index_dir_path))

    index = InvertedIndex()
    index.generate_from_dump(wikidump_path)
    index.save_to_file(index_dir_path)
