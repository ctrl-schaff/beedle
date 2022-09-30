"""
LocationMap:
Creates a frozen lookup table from the configuration dictionary given
a coordinate pair and returns a dictionary of location specific map data
Maps (xcoord, ycoord) -> dict

Example location dictionary structure
    {
      "description": "",
      "entrance": [<int>, <int>],
      "exit": [<int>, <int>],
      "traversal_cost": [],
      "reward_cost": [],
      "reward": []
    }
"""

from collections import UserDict
from typing import Any, List, Tuple

from loguru import logger


class LocationMap(UserDict):
    """
    Creates a custom dictionary for passing in coordinate pairs in
    the forms of tuples to the dictionary to access dictionary values
    that represent location specific data from the map data
    """

    def __init__(self, location_data: List[dict]):
        _location_map = self._form_location_map(location_data)
        super().__init__()
        for key, value in _location_map.items():
            super().__setitem__(key, value)

    def __repr__(self) -> str:
        location_map_repr = "LocationMap(\n" "\tlocation_data\n"
        return location_map_repr

    def __str__(self) -> str:
        location_map_str = f"LocationMap Instance {id(self)}"
        return location_map_str

    def _form_location_map(self, location_data: List[dict]) -> dict:
        """
        Iterates over the locations dictionary transforming
        (X, Y) -> dict of location specific data
        """
        location_map = {}
        for location_entry in location_data:
            location_coord = tuple(location_entry["entrance"])
            location_map[location_coord] = location_entry
            logger.debug(f"Added entry to {self}@{location_coord}")
        return location_map

    def __set_item__(self, key: Any, value: Any):
        frozen_location_msg = (
            f"{self} object is immutable "
            "Unable to modify stored data\n"
            f"Passed arguments {key}:{value}"
        )
        logger.error(frozen_location_msg)
        raise AttributeError(frozen_location_msg)

    def __del_item__(self, key: Any, value: Any):
        frozen_location_msg = (
            f"{self} object is immutable "
            "Unable to modify stored data\n"
            f"Passed arguments {key}:{value}"
        )
        logger.error(frozen_location_msg)
        raise AttributeError(frozen_location_msg)

    @property
    def location_coordinates(self) -> Tuple[int, int]:
        """
        Extracts the location entrance from the specified locations
        and transforms it into a set of coordinate locations
        key_view -> set[tuple]
        """
        location_properties = self.data.keys()
        location_coordinates = {
            tuple(location.entrance) for location in location_properties
        }
        return location_coordinates

    @property
    def location_rewards(self) -> List[str]:
        """
        Extracts the location entrance from the specified locations
        and transforms it into a set of coordinate locations
        key_view -> set[tuple]
        """
        location_properties = self.data.keys()
        location_rewards = {
            tuple(location.reward) for location in location_properties
        }
        return location_coordinates
