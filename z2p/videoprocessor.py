#!/usr/bin/env python3

"""
VideoProcessor:
Generates output video from pathfinding results
"""


import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage


class VideoProcessor:
    _EXPLORE_TILE = 16
    _PATH_TILE = 17

    def __init__(
        self,
        map_data: np.array,
        tile_data,
        num_out_path: int = 10,
    ):
        tile_colors = tile_data.get_tile_property_collection("COLOR")

        # Colormap Parameters
        self._tile_color_data = tile_colors
        self._map_data_id = map_data
        self._create_color_map_data()

        # Video Parameters
        self._num_out_path = num_out_path
        self._video_fps = 60
        self._video_buffer_size = 60
        self._buffer_tile = (-1, -1)
        self._clip_data = []
        self._time_data = []

        # Matplotlib Parameters
        self._dpi = 200

        (self._vfig, self._vax) = plt.subplots(dpi=self._dpi)
        self._vfig.tight_layout()

        self._vax.set_axis_off()
        self._video_data = self._vax.imshow(self._map_data_rgb,
                                            cmap=self.colormap
                                            )

        self._path_iterator = None
        self._explore_iterator = None

    def animate_explore(self, region_set: list, video_name: str) -> None:
        """
        Animate the region exploration only
        """
        self.create_explore_video(region_set)

        full_video = mpy.concatenate_videoclips(self._clip_data,
                                                method="compose"
                                                )
        full_video.write_videofile(
            video_name,
            fps=self._video_fps,
            threads=4,
            ffmpeg_params=["-preset", "ultrafast", "-crf", "17"],
            codec="libx264",
        )
        full_video.close()

    def animate_search(self,
                       region_set: list,
                       region_path: list,
                       video_name: str
                       ):
        """
        Animate the combination of region exploration and path generation
        associated with exploring key locations based on map logic
        """
        self.create_explore_video(region_set)
        self.create_path_video(region_path)

        full_video = mpy.concatenate_videoclips(self._clip_data,
                                                method="compose"
                                                )
        full_video.write_videofile(
            video_name,
            fps=self._video_fps,
            threads=4,
            ffmpeg_params=["-preset", "ultrafast", "-crf", "17"],
            codec="libx264",
        )
        full_video.close()

    def view_map_data(self):
        """
        Basic method for plotting the map data
        """
        self._vax.set_title("Zelda2 Map")
        self._video_data.set_data(self._map_data_rgb)
        plt.show()

    def view_key_locations(self, key_locations: list):
        """
        Basic plotting method with an extra argument
        for identifying key locations on the map
        """
        self._vax.set_title("Zelda2 Key Locations")
        max_coord = tuple(map(max, zip(*key_locations)))
        key_map = np.zeros([max_coord[0] + 1, max_coord[1] + 1])
        for coord in key_locations:
            key_map[coord[0], coord[1]] = 1
        self._video_data.set_data(key_map)
        plt.show()

    def _create_color_map_data(self):
        """
        Takes the tile color data and forms an appropiate map
        between the integer values and the string hex color values
        https://matplotlib.org/stable/api/collections_api.html
        """
        norm_func = plt.Normalize(0, len(self._tile_color_data))
        self.colormap = mpl.colors.ListedColormap(self._tile_color_data)
        self.cmapper = mpl.cm.ScalarMappable(norm=norm_func,
                                             cmap=self.colormap
                                             )

        map_data_rgba = self.cmapper.to_rgba(self._map_data_id,
                                             alpha=None,
                                             norm=True,
                                             bytes=True
                                             )
        self._map_data_rgb = map_data_rgba[:, :, :-1]
        self._map_data_video = np.copy(self._map_data_rgb)

    def create_explore_video(self, explore_list: list):
        """
        Creates the frames associated with the flood fill algorithm
        """
        self._explore_iterator = iter(
            explore_list + [self._buffer_tile] * self._video_buffer_size
        )
        num_explore_frames = len(explore_list) + self._video_buffer_size

        explore_video = mpy.VideoClip(
            self._make_explore_frame,
            duration=(num_explore_frames / self._video_fps),
        )
        self._background = np.copy(self._map_data_video)
        self._clip_data.append(explore_video)

    def create_path_video(self, path_list: list):
        """
        Creates the frames associated with the pathfinding algorithm
        """
        all_path_tiles = []
        for tpath in path_list[0:self._num_out_path]:
            all_path_tiles.extend(tpath.collection)
            all_path_tiles.extend(
                [self._buffer_tile] * self._video_buffer_size
            )
        self._path_iterator = iter(all_path_tiles)

        for tpath in path_list[0:self._num_out_path]:
            num_path_frames = tpath.rank[1] + self._video_buffer_size
            path_video = mpy.VideoClip(
                self._make_path_frame,
                duration=(num_path_frames / self._video_fps)
            )
            self._clip_data.append(path_video)

    def _make_explore_frame(self, t):
        self._time_data.append(t)
        try:
            path_tile = self._explore_iterator.__next__()
        except StopIteration:
            return mplfig_to_npimage(self._vfig)

        self._frameupdate(path_tile, self._EXPLORE_TILE)
        return mplfig_to_npimage(self._vfig)

    def _make_path_frame(self, t):
        self._time_data.append(t)
        try:
            path_tile = self._path_iterator.__next__()
        except StopIteration:
            return mplfig_to_npimage(self._vfig)

        self._frameupdate(path_tile, self._PATH_TILE)
        return mplfig_to_npimage(self._vfig)

    def _frameupdate(self, path_tile: tuple, path_value: int):
        if path_tile == self._buffer_tile:
            self._map_data_video = np.copy(self._background)
        else:
            self._map_data_video[path_tile] = self.cmapper.to_rgba(
                path_value, None, True, True
            )[:-1]
        self._video_data.set_data(self._map_data_video)
