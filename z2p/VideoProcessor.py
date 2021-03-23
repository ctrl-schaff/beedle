#!/usr/bin/env python3

"""
VideoProcessor:
Generates output video from pathfinding results
"""

import sys

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
import moviepy.editor as mpy
from moviepy.video import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

from z2p.Tile import TilePath


class VideoProcessor:
    def __init__(
        self,
        mapData: np.array,
        tileColors: tuple,
        vName: str = "pathExplore.mp4",
        numOutPath: int = 10,
    ):
        # Colormap Parameters
        self._tileColorData = tileColors
        self._mapDataID = mapData
        self._colorRange = len(tileColors)
        self._createColorMapData()
        self._EXPLORE_TILE = 16
        self._PATH_TILE = 17

        # Video Parameters
        self._numOutPath = numOutPath
        self._videoFPS = 60
        self._videoBufferSize = 60
        self._bufferTile = (-1, -1)
        self._videoName = vName
        self._clipData = []
        self._timeData = []

        # Matplotlib Parameters
        self._DPI = 200
        (self._vfig, self._vax) = plt.subplots(dpi=self._DPI)
        self._vfig.tight_layout()
        self._vax.set_axis_off()
        self._videoData = self._vax.imshow(self._mapDataRGB, cmap=self.colormap)

    def animateSearch(self, regionSet: list, regionPath: list):
        self._createExploreVideo(regionSet)
        self._createPathVideo(regionPath)

        fullVideo = mpy.concatenate_videoclips(self._clipData, method="compose")
        fullVideo.write_videofile(
            self._videoName,
            fps=self._videoFPS,
            threads=4,
            ffmpeg_params=["-preset", "ultrafast", "-crf", "17"],
            codec="libx264",
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
        self.colormap = mpl.colors.ListedColormap(self._tileColorData)
        self.cmapper = mpl.cm.ScalarMappable(norm=normFunc, cmap=self.colormap)

        mapDataRGBA = self.cmapper.to_rgba(self._mapDataID, None, True, True)
        self._mapDataRGB = mapDataRGBA[:, :, :-1]
        self._mapDataVideo = np.copy(self._mapDataRGB)

    def _createExploreVideo(self, exploreList: list):
        self._exploreIterator = iter(
            exploreList + [self._bufferTile] * self._videoBufferSize
        )
        numExploreFrames = len(exploreList) + self._videoBufferSize

        exploreVideo = mpy.VideoClip(
            self._make_explore_frame,
            duration=(numExploreFrames / self._videoFPS),
        )
        self._background = np.copy(self._mapDataVideo)
        self._clipData.append(exploreVideo)

    def _createPathVideo(self, pathList: list):
        allPathTiles = []
        for tpath in pathList[0 : self._numOutPath]:
            allPathTiles.extend(tpath.collection)
            allPathTiles.extend([self._bufferTile] * self._videoBufferSize)
        self._pathIterator = iter(allPathTiles)

        for tpath in pathList[0 : self._numOutPath]:
            numPathFrames = tpath.rank[1] + self._videoBufferSize
            pathVideo = mpy.VideoClip(
                self._make_path_frame, duration=(numPathFrames / self._videoFPS)
            )
            self._clipData.append(pathVideo)

    def _make_explore_frame(self, t):
        self._timeData.append(t)
        try:
            pathTile = self._exploreIterator.__next__()
        except StopIteration:
            return mplfig_to_npimage(self._vfig)

        self._frameupdate(pathTile, self._EXPLORE_TILE)
        return mplfig_to_npimage(self._vfig)

    def _make_path_frame(self, t):
        self._timeData.append(t)
        try:
            pathTile = self._pathIterator.__next__()
        except StopIteration:
            return mplfig_to_npimage(self._vfig)

        self._frameupdate(pathTile, self._PATH_TILE)
        return mplfig_to_npimage(self._vfig)

    def _frameupdate(self, pathTile: tuple, pathValue: int):
        if pathTile == self._bufferTile:
            self._mapDataVideo = np.copy(self._background)
        else:
            self._mapDataVideo[pathTile] = self.cmapper.to_rgba(
                pathValue, None, True, True
            )[:-1]
        self._videoData.set_data(self._mapDataVideo)
