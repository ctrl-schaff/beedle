## beedle 
Python3 library for translating a 2D map into a bidirectional graph
while also topologically sorting based off the 2D map configuration logic


## Example [Zelda 2]
## File Formats & Data 
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

# Sources 
* [Zelda2MapEdit](https://github.com/matal3a0/Zelda2MapEdit)
    * Author:Johan Björnell
    * Launched off the methods for reading / writing from the rom file
    * Based file format for game graph logic off the maplocations variable

# References
* ROM FILE
    * [ZeldaIIMapData](https://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:ROM_map#Overworld)
* Python Visualization
    * [Integer -> Color Mapping](https://stackoverflow.com/questions/36377638/how-to-map-integers-to-colors-in-matplotlib)
    * [Matplotlib Colormap](https://matplotlib.org/3.3.3/tutorials/colors/colormap-manipulation.html#sphx-glr-tutorials-colors-colormap-manipulation-py)
    * [Matplotlib ScalarMappable](https://matplotlib.org/3.3.4/api/cm_api.html#matplotlib.cm.ScalarMappable)
    * [Matplotlib Colormap decode](https://stackoverflow.com/questions/45177154/how-to-decode-color-mapping-in-matplotlibs-colormap/45178154#45178154)
* Miscellaneous 
    * [String splice](https://stackoverflow.com/questions/9475241/split-string-every-nth-character)
    * [Unique List | Maintain Order](https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order)
    * [NamedTuple defaults](https://stackoverflow.com/questions/11351032/named-tuple-and-default-values-for-optional-keyword-arguments)
    * [List tuple index](https://stackoverflow.com/questions/30341008/is-it-possible-to-index-nested-lists-using-tuples-in-python)
* Moviepy
    * [Moviepy demo](https://zulko.github.io/blog/2014/11/29/data-animations-with-python-and-moviepy/)
* Pathfinding
    * [redblobgames](https://www.redblobgames.com/pathfinding/a-star/introduction.html)

### maplogic
Class for containing the logic related to the map data. Logic in this case refers to specific things
about map that cannot be obtained from a simple (X,Y) coordinate static map. Also not every tile on
a map requires additional logic for understanding how to parse the node, so the logic file only
contains those tiles which require additional information to process appropriately. 
    > Traversal Cost
        Required cost in order to actually walk on the tile. At the moment, this only uses items as
        requirements as the item special effect is likely required in order to connect to a specific
        edge that this tile connects with
    > Reward Cost
        Required cost in order to receive a reward on this tile. At the moment, this only uses items
        as requirements as the item special effect is likely required in order to obtain the reward 
    > Reward
        Item list received if the reward cost is met
    > Entrace & Exit Coordinatesa
        If a tile connects to a non-adjecent node, then this entrance & exit coordinates specify
        this non-obvious connection

