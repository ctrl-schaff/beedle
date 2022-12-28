"""
Command line tool for converting the map data stored within the zelda2 rom
to a plain-text file with integers representing the overworld map tiles

This tool is how the map data is generated for testing purposes within the
beedle library

We process the rom map data in quadrants. Each quadrant has a starting and
ending address for where the map data is run length encoded
"""

import argparse
import itertools
from pathlib import Path
from typing import Any, Iterable, Union

import numpy as np


def chunker(
    iterable: Iterable, length: int, fillvalue: Any = None
) -> Iterable:
    """
    Collect data into fixed-length chunks or blocks
    """
    iter_collection = [iter(iterable)] * length
    return itertools.zip_longest(*iter_collection, fillvalue=fillvalue)


def extract_map_data(romfile: Path) -> np.array:
    """
    Extracts the map data from the zelda 2 rom.

    Important Reference:
    https://datacrystal.romhacking.net/wiki/Zelda_II:_The_Adventure_of_Link:ROM_map#Overworld_Map_Data

    Using these addresses:
    506C - 538C - West Hyrule
    665C - 6942 - Death Mountain
    9056 - 936F - East Hyrule
    A65C - A942 - Maze Island
    We can construct the map using integer values for the tile representation

    For additional clarity purposes we also introduce a barriers between
    the four quadrants for traversal representation purposes
    """

    half_map_size_x_dimension = 75
    half_map_size_y_dimension = 65
    map_data = np.zeros(
        [2 * half_map_size_x_dimension, 2 * half_map_size_y_dimension],
        dtype=int,
    )

    map_boundary = {
        "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
        "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
        "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
        "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
    }

    map_quadrants = []
    with open(romfile, "rb+") as romdata:
        for mapbound in map_boundary.values():
            romdata.seek(mapbound[0])
            num_map_bytes = (mapbound[1] - mapbound[0]) + 1
            map_byte_chunk = romdata.read(num_map_bytes).hex()

            quadrant = []
            for byte in chunker(map_byte_chunk, 2, fillvalue="0"):
                quadrant += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

            # Vertical water barrier to separate sub maps
            water_range = range(
                half_map_size_y_dimension,
                len(quadrant),
                half_map_size_y_dimension,
            )
            for index in water_range:
                quadrant.insert(index - 1, 12)

            map_quadrants.append(
                np.resize(
                    np.array(quadrant),
                    (half_map_size_x_dimension, half_map_size_y_dimension),
                )
            )

    # Cleanup the Death Mountain and Maze Island Segments
    map_quadrants[1][:, 28:] = 12
    map_quadrants[1][60:, :] = 12
    map_quadrants[3][:, :28] = 12
    map_quadrants[3][59:, :] = 12

    # Form total map
    map_data[:, :] = np.hstack(
        (
            np.vstack((map_quadrants[0], map_quadrants[1])),
            np.vstack((map_quadrants[2], map_quadrants[3])),
        )
    )

    # Transpose the map to ensure you can index with
    # (X, Y) rather than (Y, X)
    # map_data = map_data.T
    return map_data


def write_map_data(map_data: np.array, output_file: Union[str, Path]) -> None:
    """
    Write the numpy 2D array to a text file for
    consumption within the beedle tests
    """
    text_separator = " "
    text_format = "%1.0u"
    line_break = "\n"
    np.savetxt(
        fname=output_file,
        X=map_data,
        fmt=text_format,
        delimiter=text_separator,
        newline=line_break,
    )


if __name__ == "__main__":
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument(
        "-r",
        "--romfile",
        dest="romfile",
        type=str,
        required=True,
        help="Input file path for the zelda 2 rom file",
    )
    parser_obj.add_argument(
        "-o",
        "--outpath",
        dest="outpath",
        type=str,
        required=True,
        help="Output file path for the extracted map data",
    )

    args = parser_obj.parse_args()
    mapfile_path = Path(args.romfile).absolute().resolve()
    outputfile_path = Path(args.outpath).absolute().resolve()

    extracted_map_data = extract_map_data(mapfile_path)
    write_map_data(extracted_map_data, outputfile_path)
