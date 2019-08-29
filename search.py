import sys
from wise.index import InvertedIndex

if __name__ == '__main__':

    index_path = sys.argv[1]
    query_path = sys.argv[2]
    out_path = sys.argv[3]

    print("Index will be loaded from {}".format(index_path))

    index = InvertedIndex()
    index.load_from_file(index_path)

    qf = open(query_path, 'r')
    out = open(out_path, 'w')

    for query in qf.readlines():
        titles = index.search(query)
        out.write("\n".join(titles))
        out.write("\n\n")

