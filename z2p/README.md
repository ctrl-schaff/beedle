[maplogic]
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

