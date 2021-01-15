import os
from datetime import date

import geopandas as gpd
from matplotlib import pyplot as plt

from RasterData import open_raster, get_date_from_filename

BASE_DIR = "../"
RASTER_DIR = BASE_DIR+"raster/"
SHAPE_DIR = BASE_DIR+"shape/"


def vector_visualization():
    file_dir = ""
    for name in os.listdir(SHAPE_DIR):
        if name[-8:] == '.geojson':
            file_dir = SHAPE_DIR+name
            break

    a = gpd.read_file(file_dir)
    a.plot()
    plt.savefig('temp.jpg')  # doesn't work because we haven't use plt


def add_raster_date_to_rasterstats(raster_stats: [], date_str: str):
    for i in range(len(raster_stats)):
        raster_stats[i]['date'] = date_str


def open_rasters(initial_date: date = date(1, 1, 1), final_date: date = date(5000, 12, 1)):
    rasters_stats = []

    for name in os.listdir(RASTER_DIR):
        if name[-4:] == '.tif':  # we open only .tif files
            raster_date = get_date_from_filename(name)
            if initial_date <= raster_date <= final_date:  # dates are between the initial and final date we want
                rasters_stats.append(open_raster(name))

    print(rasters_stats)
    return rasters_stats


def get_potrero_info(name):
    """
    Gets the information of an specific potrero.

    :param name: the name of the potrero
    :return: a dictionary with that information.
    """

    # look for the files

    #

    return 0


if __name__ == "__main__":
    # vector_visualization()
    open_rasters()

