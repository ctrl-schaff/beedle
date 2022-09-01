#!/usr/bin/env python3

import pathlib 

import pytest


@pytest.fixture()
def z2_map_data():
    '''
    Constructs the map data from the zelda 2 map
    '''

    SUB_MAP_SIZE_X = 75
    SUB_MAP_SIZE_Y = 65
    MAP_SIZE_X = 2 * SUB_MAP_SIZE_X
    MAP_SIZE_Y = 2 * SUB_MAP_SIZE_Y

    map_boundary = {
        "WEST_HYRULE": (int("506C", 16), int("538C", 16)),
        "DEATH_MOUNTAIN": (int("665C", 16), int("6942", 16)),
        "EAST_HYRULE": (int("9056", 16), int("936F", 16)),
        "MAZE_ISLAND": (int("A65C", 16), int("A942", 16)),
    }

    sub_map_data = []

    map_data = np.zeros(
        [2 * SUB_MAP_SIZE_X, 2 * SUB_MAP_SIZE_Y], dtype=int
    )

    rompath_env = get_env_vars()
    rompath = pathlib.Path(rompath_env).resolve()
    assert rompath.exists()
    
    with open(romdata, "rb+") as romfile:
        for mapbound in map_boundary.values():
            romfile.seek(mapbound[0])
            num_map_bytes = (mapbound[1] - mapbound[0]) + 1
            map_byte_chunk = romfile.read(num_map_bytes).hex()

            sub_map = []

            # Collect data into fixed-length chunks or blocks
            # def chunker(iterable, n, fillvalue=None):
            #     args = [iter(iterable)] * n
            #     return itertools.zip_longest(*args, fillvalue=fillvalue)
            for byte in z2p.utility.chunker(
                    map_byte_chunk, 2, fillvalue="0"
            ):
                sub_map += (int(byte[0], 16) + 1) * [int(byte[1], 16)]

            ._form_water_barrier(sub_map)

            .sub_map_data.append(
                np.resize(
                    np.array(sub_map),
                    (.SUB_MAP_SIZE_X, .SUB_MAP_SIZE_Y)
                )
            )

    """
    Vertical water barrier to separate sub maps
    """
    for index in range(.SUB_MAP_SIZE_Y,
                       len(sub_map),
                       .SUB_MAP_SIZE_Y
                       ):
        sub_map.insert(index - 1, 12)

    # Cleanup the Death Mountain and Maze Island Segments
    .sub_map_data[1][:, 28:] = 12
    .sub_map_data[1][60:, :] = 12
    .sub_map_data[3][:, :28] = 12
    .sub_map_data[3][59:, :] = 12

    # Form total map
    .map_data[:, :] = np.hstack(
        (
            np.vstack((.sub_map_data[0], .sub_map_data[1])),
            np.vstack((.sub_map_data[2], .sub_map_data[3])),
        )
    )

    # Transpose the map to ensure you can index with
    # (X, Y) rather than (Y, X)
    .map_data = .map_data.T
    (.MAP_SIZE_X, .MAP_SIZE_Y) = .map_data.shape
