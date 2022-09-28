"""
Module for all custom exceptions within the 
z2p module
"""

from __future__ import annotations

from typing import Any

from .tilemap import TileMap


class TileMapIndexError(KeyError):
    def __init__(self, tilemap: TileMap, key: Any, value: Any):
        message = self._format_message(tilemap, key, value)
        super().__init__(message)

    def _format_message(self, tilemap: TileMap, key: Any, value: Any) -> str:
        """
        Formats the KeyError message based off the size of tilemap
        and the provided key-value pair provided
        """
        message = (
            f"Unable to update TileMap instance {tilemap} "
            f"with key {key} + value {value} pair\n"
            "Expected tuple key value representing coordinates "
            "and TileNode object value"
        )
        return message
