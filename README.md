# Z2P [Zelda 2 Pathing]

Attempts to find all possible paths to go from the starting location to the ending location
following the game logic

# File Formats & Data 


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
"""



# Sources 
    - [Zelda2MapEdit](https://github.com/matal3a0/Zelda2MapEdit)
        * Author:Johan Björnell
        * Launched off the methods for reading / writing from the rom file
        * Based file format for game graph logic off the maplocations variable

# References
    - ROM FILE
        * [ZeldaIIMapData](https://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:ROM_map#Overworld)
    - Python Visualization
        * [Integer -> Color Mapping](https://stackoverflow.com/questions/36377638/how-to-map-integers-to-colors-in-matplotlib)
        * [Matplotlib Colormap](https://matplotlib.org/3.3.3/tutorials/colors/colormap-manipulation.html#sphx-glr-tutorials-colors-colormap-manipulation-py)
    - Miscellaneous 
        * [String splice](https://stackoverflow.com/questions/9475241/split-string-every-nth-character)



