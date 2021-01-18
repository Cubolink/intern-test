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


def open_rasters(initial_date: date = None, final_date: date = None):
    """
    Gets the raster data from one date to other.

    :param initial_date: the initial date to consider when getting the data. Default None means from the oldest times.
    :param final_date: the final date to consider when getting the data. Default None means to the most recent times.
    :return: a list with the inforomation over time. Each element is a list with all the potreros at the same date.
    """
    if initial_date is None:
        initial_date = date(1, 1, 1)
    if final_date is None:
        final_date = date(5000, 12, 1)
    rasters_stats = []

    for name in os.listdir(RASTER_DIR):
        if name[-4:] == '.tif':  # we open only .tif files
            raster_date = get_date_from_filename(name)
            if initial_date <= raster_date <= final_date:  # dates are between the initial and final date we want
                rasters_stats.append(open_raster(name))

    # calculate stats over this period of time
    potreros = {}

    def combined_mean(x1, n1, x2, n2):
        return (x1 * n1 + x2 * n2) / (n1 + n2)

    for p in range(len(rasters_stats[0])):
        for t in range(len(rasters_stats)):  # for each potrero, iterate over the time dictionaries
            name = rasters_stats[t][p]['properties']['Name']
            if name not in potreros.keys():
                potreros[name] = {}
                potreros[name]['count'] = 0
                potreros[name]['mean'] = 0

            if rasters_stats[t][p]['properties']['mean'] is not None:
                potreros[name]['mean'] = combined_mean(potreros[name]['mean'], potreros[name]['count'],
                                                       rasters_stats[t][p]['properties']['mean'],
                                                       rasters_stats[t][p]['properties']['count'])
                potreros[name]['count'] += rasters_stats[t][p]['properties']['count']
            else:
                print(f"'None' mean value in {t}, {p}")

    # then return

    return potreros


def get_potreros_info(names: [str] = None, initial_date: date = None, final_date: date = None):
    """
    Gets the information of an specific potrero or list of potreros.

    :param names: the names of the selected potrero. Default None means all potreros.
    :param initial_date: the initial date to consider. Default None means from the oldest times.
    :param final_date: the final date to consider. Default None means to the most recent times.

    :return: a list with the information through time. Each element is a list with the potreros information.
    """

    # look for the files
    raster_stats = open_rasters(initial_date, final_date)
    if names is not None:
        # select info
        for i_date in range(len(raster_stats)):
            # option 1, coparing times resulted in this option being twice faster
            raster_stats[i_date] = [
                potrero for potrero in raster_stats[i_date]
                if potrero['properties']['Name'] in names
            ]

            '''
            # option 2
            raster_stats[i_date] = list(filter(lambda potrero: potrero['properties']['Name'] in names,
                                               raster_stats[i_date]))
            '''

    return raster_stats


if __name__ == "__main__":
    # vector_visualization()
    print(get_potreros_info())

