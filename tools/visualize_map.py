"""
Tool for visualizing map provided a custom colormap to translate the
2D map data into an image via the specified color mapping

The input configuration for the color definitions uses the following:
{
    "MAP_TILE_DESCRIPTION": {
        "index": <integer>,
        "color": <string>
    },
    ...
}
- The "MAP_TILE_DESCRIPTION" isn't used but is useful for human readability
  for ensuring that the color mapping corresponds to the intended tile
- The index is the actual value of the tile on the map. This doesn't have to
  necessarily be an integer but float doesn't seem a likely alternative
- The color is the string hex value of the color to map to the index value
"""

import argparse
import json
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

ColorMap = mpl.colors.ListedColormap
Mapper = mpl.cm.ScalarMappable


def load_map_data(filename: Union[str, Path]) -> np.array:
    """
    Loads the map data into a 2D numpy array

    Expected map data file format:
    <int> <int> ... <int>\n
    <int> <int> ... <int>\n
    ...
    <int> <int> ... <int>
    """
    with open(filename, "r", encoding="utf-8") as file_handle:
        return np.array(
            [
                list(map(int, map_row.strip("\n").split()))
                for map_row in file_handle.readlines()
            ]
        )


def load_color_definitions(filename: Union[str, Path]) -> dict:
    """
    Loads the color definitions file as a json object
    """
    with open(filename, "r", encoding="utf-8") as file_handle:
        try:
            color_definitions = json.load(file_handle)
        except json.JSONDecodeError as json_decode_err:
            raise json_decode_err
        return color_definitions


def __parse_color_definitions(color_definitions: dict) -> List[str]:
    """
    Provided the dictionary of color definitions extract the
    hex format color strings for colormap generation
    """
    hex_colors = [
        tile_value["color"] for tile_value in color_definitions.values()
    ]
    return hex_colors


def create_colormap(color_definitions: dict) -> Tuple[ColorMap, Mapper]:
    """
    Given the scalar map data and color definitions, create
    a colormap for usage within matplotlib for visualizing
    the map data

    References:
    <ScalarMappable>
    https://matplotlib.org/stable/api/cm_api.html#matplotlib.cm.ScalarMappable
    <ListedColormap>
    https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.ListedColormap
    """
    color_values = __parse_color_definitions(color_definitions)
    normalize_function = plt.Normalize(0, len(color_values))
    colormap_instance = mpl.colors.ListedColormap(color_values)

    mapper_instance = mpl.cm.ScalarMappable(
        norm=normalize_function, cmap=colormap_instance
    )
    return colormap_instance, mapper_instance


def translate_colormap(data: np.array, cmapper: Mapper) -> np.array:
    """
    Wrapper around mpl.cm.ScalarMappable.to_rgba to encode the provided
    numpy array with RGBA color values for visualization purposes
    """
    map_color = cmapper.to_rgba(data, alpha=None, bytes=True, norm=True)
    map_color = map_color[:, :, :-1]
    return map_color


if __name__ == "__main__":
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument(
        "-m",
        "--mapdata",
        dest="mapdata",
        type=str,
        required=True,
        help="Input file path for the map data",
    )
    parser_obj.add_argument(
        "-c",
        "--colordef",
        dest="color_definitions",
        type=str,
        required=True,
        help="Input file path for the color definitions",
    )
    parser_obj.add_argument(
        "-o",
        "--outimage",
        dest="outimage",
        type=str,
        required=False,
        default="./map_colors.png",
        help="Output file path for the map image",
    )

    args = parser_obj.parse_args()
    map_data = load_map_data(args.mapdata)
    color_definitions = load_color_definitions(args.color_definitions)

    colormap, mapper = create_colormap(color_definitions)
    color_map_data = translate_colormap(map_data, mapper)

    DPI = 1000
    (vfig, vax) = plt.subplots(dpi=DPI)
    vfig.tight_layout()
    map_figure = vax.imshow(color_map_data, cmap=colormap)
    plt.savefig(args.outimage, format="png")
