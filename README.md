### beedle 
Python3 library for translating a 2D map into a graph object
Provides methods for analyzing bottlenecks and topologically
sorting the graph for solving map traversal given predefined
logical constraints

Primary motivation for development was to analyze the map for
zelda2 for the NES and expanded to a general purpose library
for analyzing any defined 2D map

### Installation
Installation from pypi: `pip install beedle`

### Configuration
There are two main things required in order to work with beedle:

    1. map data
    2. map constraints

The map data is represented as a 2D array of integer values. These
are stored in a numpy.array object. Each value of a tile represents
the tile within the map that indicates what the properties of the 
map tile

The map constraints are slightly more specific. In order to determine
how to traverse / progress through the map, there are certain pre-defined
constraints that are defined in a separate json configuration file. The configuration
has two main sections, the tile properties and the location properties. In order
for the integer values associated with the map data to mean something, we must map
the integer value to some tile properties data. This is defined within the `"tiles"`
field. This field is represents a collection of map objects that has the following
structure:

```
{
    "tiles": {
        "0": {
            "TYPE": <str>,
            "SYMBOL": <str>,
            "BASE_COST": <collection<str>>,
            "WALKABLE": <bool>,
            "COLOR": <str>
        },

        ...

        "N": {
            "TYPE": <str>,
            "SYMBOL": <str>,
            "BASE_COST": <collection<str>>,
            "WALKABLE": <bool>,
            "COLOR": <str>
        }
    }
}
```

The tiles dictionary is a map of string represented integers as keys with
tile properties maps representing import core properties of the map tile.

- TYPE: string value representing the tile environment used primarily for
identification purposes. Serves no purpose other than giving additional information
- SYMBOL: string value representing the tile symbol in a text environment used primarily for
identification purposes. Serves no purpose other than giving additional information. Previously
used when visually representing the map in a terminal window
- BASE_COST: collection of string values that are any items required to access 
- WALKABLE: flag value to indicate if the tile is able to be traversed. This is slighly different
from `BASE_COST` because it only indicates if at some point the tile is meant to be traversal at
some point within the map. Effectively any walls that cannot be traversed would have a value of 
false for the `WALKABLE` property
- COLOR: string value representing the tile color in a visual environment used primarily for
identification purposes. Serves no purpose other than giving additional information. Previously
used when visually representing the map in a graphical window


The location properties are specific tiles within the map data that represent unique areas.
Potential resasons for adding a location to the `"locations"` field within the configuration:

- Any area where import rewards can be acquired for continued traversal of the map 
- Any area where non-adjacent entrances / exits exist to add as an edge to the tile
- Any area with specific rewards accessable within the tile

The following format defines how the `"locations"` field is structured within the configuration

```
{
    "locations": [
        {
            "description": <str>,
            "entrance": [<int>, <int>],
            "exit": [<int>, <int>],
            "traversal_cost": <collection<str>>,
            "reward_cost": <collection<str>>,
            "reward": <collection<str>>
        },

        ...

        {
            "description": <str>,
            "entrance": [<int>, <int>],
            "exit": [<int>, <int>],
            "traversal_cost": <collection<str>>,
            "reward_cost": <collection<str>>,
            "reward": <collection<str>>
        }
    ]
}
```

- description: string providing a short label for what the location is. Optional within the logic of
the library as it's used only for debugging purposes
- entrance: tuple of two integer values representing the (x,y) position of the access point to the
location on the map. Currently only support one value for this field
- exit: tuple of two integer values representing the (x,y) position of the exit point to the
location on the map. For values that aren't equal to the entrance, these locations represent exits
that aren't equal to the entrance and may potentially be non-adjacent the location on the map.
Currently only support one value for this field
- traversal_cost: collection of strings representing the items required to traverse / access the
entrance of the location. In order to meet this requirement, all items within the traversal_cost
field must be present. If empty, then the location can be accessed regardless of the inventory
status
- reward_cost: collection of strings representing the items required to access the rewards stored at
the location. In order to meet this requirement, all items within the reward_cost
field must be present. If empty, then the reward can be attained regardless of the inventory
status
- reward: collection of items that can be obtained at the specified location. If empty then nothing
can be added to modify the inventory after visiting this location


### Example [Zelda 2]
A lot of the map data extraction information came from 
https://datacrystal.romhacking.net

Specifically the info related to the overworld map and how
to extract that data from the ROM can be found there through the
following [link](https://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:ROM_map#Overworld)

The data discovered from the above links allows us to build the following table with tile properties
specific to our map

---
###### Tile Properties
ID     | SYMBOL | BACKGROUND | COLOR (HEX) |
------ | ------ | ---------- | ----------- |
00     | T      | Town       | #747474     |
01     | C      | Cave       | #000000     |
02     | P      | Palace     | #efefe1     |
03     | B      | Bridge     | #f0bc3c     |
04     | D      | Desert     | #fabcb1     |
05     | G      | Grassland  | #80D011     |
06     | F      | Forest     | #009401     |
07     | S      | Swamp      | #386131     |
08     | Y      | Graveyard  | #fcfcf1     |
09     | R      | Road       | #ffbc31     |
10     | V      | Volcanic   | #c84c01     |
11     | M      | Mountain   | #634530     |
12     | W      | Water      | #3cbcf0     |
13     | W      | Water(Walk)| #85d5f2     |
14     | O      | Boulder    | #dc7e43     |
15     | A      | Monster    | #03daf4     |
---

Using this data we can then define the `"tiles"` field
with this information along with the '`locations"` field 
for our configuration. We can then load the map directly
from the rom and import it directly into a numpy.array.

With these two items we can build our graph

```
# map_data (2D np.array)
# configuration (json loaded dictionary)

from beedle import TileGraph, LocationMap, TileMap

# Build the LocationMap object 
location_data = configuration.get('locations', None)
location_map = LocationMap(location_data)

# Build the TileMap object
tile_data = configuration.get('tiles', None)
tile_map = TileMap(map_data, location_map, tile_data)

# Build the TileGraph object
graph_start = (23, 22)
graph_end = (69, 43)
graph_obj = TileGraph(graph_start, graph_end, tile_map, location_map)

# Sort the Graph 
topological_order, topological_graph = graph_obj.topological_sort(tile_map, location_map)
```

# References 
* [Zelda2MapEdit](https://github.com/matal3a0/Zelda2MapEdit)
    * Author: Johan Björnell
    * Launched off the methods for reading / writing from the rom file
    * Based file format for game graph logic off the maplocations variable
* [NesZeldaMapData](https://github.com/asweigart/nes_zelda_map_data)
    * Author: 
    * Used the overmap data for constructing the configuration for the zelda 1 map
