#!/usr/bin/env python3

"""
VideoProcessor:
Generates output video from pathfinding results
"""

import copy
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import moviepy.editor as mpy
from moviepy.video.io.bindings import mplfig_to_npimage


class VideoProcessor:
    def __init__(
        self, mapData: np.array, tileColors: tuple, vName: str = "pathExplore.mp4"
    ):
        # Colormap Parameters
        self._tileColorData = tileColors
        self._mapDataID = mapData
        self._colorRange = len(tileColors)
        self._createColorMapData()

        # Video Parameters
        self._exploreFPS = 45
        self._pathFPS = 45
        self._fullFPS = 45
        self._videoName = vName

        # Matplotlib Parameters
        self._DPI = 200
        (self._vfig, self._vax) = plt.subplots(dpi=self._DPI)
        self._vfig.tight_layout()
        self._vax.set_axis_off()
        self._videoData = self._vax.imshow(self._mapDataRGB, cmap=self.colormap)

    def animateSearch(self, regionSet: list, regionPath: list):
        exploreVideo = self._createExploreVideo(regionSet)
        pathVideo = self._createPathVideo(regionPath)
        fullVideo = mpy.concatenate_videoclips(
            [exploreVideo, pathVideo], method="compose"
        )

        fullVideo.write_videofile(
            self._videoName,
            fps=self._fullFPS,
            threads=4,
            codec="libx264",
            ffmpeg_params=["-preset", "veryslow", "-crf", "17"],
        )
        fullVideo.close()

    def viewMapData(self):
        self._vax.set_title("Zelda2 Map")
        self._videoData.set_data(self._mapDataRGB)
        plt.show()

    def viewKeyLocations(self, keyLocations: list):
        self._vax.set_title("Zelda2 Key Locations")
        maxCoord = tuple(map(max, zip(*keyLocations)))
        keyMap = np.zeros([maxCoord[0] + 1, maxCoord[1] + 1])
        for coordTup in keyLocations:
            keyMap[coordTup[0], coordTup[1]] = 1
        self._videoData.set_data(keyMap)
        plt.show()

    def _createColorMapData(self):
        normFunc = plt.Normalize(0, self._colorRange)
        self.colormap = matplotlib.colors.ListedColormap(self._tileColorData)
        self.cmapper = matplotlib.cm.ScalarMappable(norm=normFunc, cmap=self.colormap)

        mapDataRGBA = self.cmapper.to_rgba(self._mapDataID, None, True, True)
        self._mapDataRGB = mapDataRGBA[:, :, :-1]
        self._mapDataVideo = copy.copy(self._mapDataRGB)

    def _createExploreVideo(self, exploreList: list):
        self._exploreIterator = iter(exploreList)
        self._numExploreFrames = len(exploreList)

        exploreVideo = mpy.VideoClip(
            self._make_explore_frame,
            duration=(self._numExploreFrames / self._exploreFPS),
        )
        return exploreVideo

    def _createPathVideo(self, pathList: list):
        pathTiles = [tile for path in pathList for tile in path]
        uniquePathTiles = dict.fromkeys(pathTiles)
        self._numPathFrames = len(uniquePathTiles)
        self._pathIterator = iter(uniquePathTiles)

        pathVideo = mpy.VideoClip(
            self._make_path_frame, duration=(self._numPathFrames / self._pathFPS)
        )
        return pathVideo

    def _make_explore_frame(self, t):
        try:
            pathTile = self._exploreIterator.__next__()
        except StopIteration:
            return self._mapDataVideo
        self._mapDataVideo[pathTile] = self.cmapper.to_rgba(16, None, True, True)[:-1]
        self._videoData.set_data(self._mapDataVideo)
        return mplfig_to_npimage(self._vfig)

    def _make_path_frame(self, t):
        try:
            pathTile = self._pathIterator.__next__()
        except StopIteration:
            return self._mapDataVideo
        self._mapDataVideo[pathTile] = self.cmapper.to_rgba(17, None, True, True)[:-1]
        self._videoData.set_data(self._mapDataVideo)
        return mplfig_to_npimage(self._vfig)
