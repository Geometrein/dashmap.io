# This file can be used to preview the datum.json
# on a map with its traces.
import os
import sys
from dashmap import map_graphs

dirname = os.path.dirname(__file__)
dirname = dirname.replace('data/datum', '')
sys.path.insert(0, dirname)


def main():
    """
    """
    df1, df2, df3 = map_graphs.load_datum()
    choropleth = map_graphs.init_choropleth(df1, df3)
    choropleth = map_graphs.update_layout_and_traces(choropleth)
    choropleth.show()


if __name__ == '__main__':
    main()
