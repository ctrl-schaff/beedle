"""
Module for all custom exceptions within the z2p module
"""

from __future__ import annotations

from typing import Any

# from .tilemap import TileMap


class TileMapIndexError(KeyError):
    """
    Index error specifically for TileMap objects
    If a Tuple[int, int] is passed in that is beyond
    the bounds of the map / isn't an instance of type
    Tuple[int, int], then this exception is raised
    """

    def __init__(self, tilemap: "TileMap", key: Any, value: Any):
        message = self._format_message(tilemap, key, value)
        super().__init__(message)

    def _format_message(self, tilemap: "TileMap", key: Any, value: Any) -> str:
        """
        Formats the KeyError message based off the size of tilemap
        and the provided key-value pair provided
        """
        message = (
            f"{{key:{key}, value:{value}}}\n"
            f"Unable to access TileMap instance {tilemap}\n"
            f"Expected key type: Tuple[int, int]\n"
            f"Expected value type: TileNode\n"
        )
        return message
