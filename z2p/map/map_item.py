#!/usr/bin/env python3

"""
Class for loading the map item data
"""

import z2p.utility


class MapItemData:
    """
    Wrapper for importing the item data associated with the map
    Item data is specified in data/config/mapitems.dat
    Items are stored in a <item_name>:<value> format with groups of items
    associated together for clarity
        > <item_name>: str
        > <value>: int/float (numeric value)
    This data is associated with specific tiles from the maplogic file so that
    the graph can look up tile costs when traversing the map
    While it is not required, items of higher importance are weighted higher
    than less important / optional items for scoring purposes
    """
    def __init__(self, item_file: str):
        item_data = z2p.utility.load_json_data(item_file)
        self.item_lookup = z2p.utility.unpack_json_data(item_data)
        self.item_lookup["|"] = 0
        self.item_set = set(self.item_lookup.keys())

    def __getitem__(self, item_key: str):
        try:
            item_entry = self.item_lookup[item_key]
            return item_entry
        except KeyError as key_err:
            print(key_err)
            print(
                f"Error indexing the item lookup table with key {item_key}"
            )
            print("Valid keys [{0:s}]".format(*self.item_lookup.keys()))
            return None
