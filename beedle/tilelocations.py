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

New transformed location dictionary structure
    {
      "description": str
      "entrance": Tuple[int, int],
      "exit": Tuple[int, int]
      "traversal_cost": Set,
      "reward_cost": Set,
      "reward": Set
    }
"""

from collections import UserDict
from typing import Any, List, Set, Tuple

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

        self.__entrance_locations = None

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
            location_entry["entrance"] = tuple(location_entry["entrance"])
            location_entry["exit"] = tuple(location_entry["exit"])

            location_entry["traversal_cost"] = set(
                location_entry["traversal_cost"]
            )
            location_entry["reward_cost"] = set(location_entry["reward_cost"])
            location_entry["reward"] = set(location_entry["reward"])

            location_coordinates = location_entry["entrance"]
            location_map[location_coordinates] = location_entry

            logger.debug(f"Added entry [{location_coordinates}] to {self}")
        return location_map

    def __missing__(self, key: Any) -> dict:
        """
        Handles the cases where we attempt to access
        additional location properties for tiles
        with no additional information

        Defaults to returning an empty dict
        """
        default_resp = {}
        missing_msg = f"Unable to find key {key}"
        logger.debug(missing_msg)
        return default_resp

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
    def entrance_locations(self) -> Set[Tuple[int, int]]:
        """
        Extracts the location entrance from the specified locations
        and transforms it into a set of coordinate locations
        key_view -> set[tuple]
        """
        if self.__entrance_locations is None:
            logger.debug("Populating __entrance_locations property")
            location_properties = self.data.values()
            self.__entrance_locations = {
                location["entrance"] for location in location_properties
            }
        return self.__entrance_locations

    def location_search(self, item: str) -> List[Tuple[int, int]]:
        """
        Given an item value to search with in the LocationMap dictionary,
        will iterate over all stored locations and return list collection
        of coordinates that match having the specified item as a
            > {reward, reward_cost, traversal_cost}

        Specific to the reward property, this should be unique to one specific
        location as multiple of the same reward cannot exist within the logic
        of the map configuration, so this method always returns a single value
        """
        origin_locations = self.location_cost_search(item)
        origin_locations.append(self.location_reward_search(item))
        return origin_locations

    def location_cost_search(self, item: str) -> List[Tuple[int, int]]:
        """
        Given an item value to search with in the LocationMap dictionary,
        will iterate over all stored locations and return list collection
        of coordinates that match having the specified item as a
            > {reward_cost, traversal_cost}
        """
        cost_origin_locations = self.location_reward_cost_search(item)
        cost_origin_locations.extend(self.location_traversal_cost_search(item))
        return cost_origin_locations

    def location_reward_search(self, item: str) -> Tuple[int, int]:
        """
        Given an item value to search with in the LocationMap dictionary,
        will iterate over all stored locations and return list collection
        of coordinates that match having the specified item as a
            > {reward}

        Specific to the reward property, this should be unique to one specific
        location as multiple of the same reward cannot exist within the logic
        of the map configuration, so this method always returns a single value
        """
        reward_origin_locations = self.__property_search("reward", item)
        if reward_origin_locations:
            reward_origin_locations = reward_origin_locations[0]
        return reward_origin_locations

    def location_reward_cost_search(self, item: str) -> List[Tuple[int, int]]:
        """
        Given an item value to search with in the LocationMap dictionary,
        will iterate over all stored locations and return list collection
        of coordinates that match having the specified item as a
            > {reward_cost}
        """
        reward_cost_origin_locations = self.__property_search(
            "reward_cost", item
        )
        return reward_cost_origin_locations

    def location_traversal_cost_search(
        self, item: str
    ) -> List[Tuple[int, int]]:
        """
        Given an item value to search within the LocationMap dictionary,
        will iterate over all stored locations and return a list collection
        of coordinates that match having the specified item as a
            > {traversal_cost}
        """
        traversal_cost_origin_locations = self.__property_search(
            "traversal_cost", item
        )
        return traversal_cost_origin_locations

    def __property_search(
        self, property_name: str, item: str
    ) -> List[Tuple[int, int]]:
        """
        Base method for searching through the location properties stored
        as keys to the LocationMap underlying dict

        Returns all coordinates that matched in a list collection
        """
        found_locations = []
        for location_coordinates, location_properties in self.data.items():
            if item in location_properties.get(property_name, []):
                found_locations.append(location_coordinates)
        return found_locations
