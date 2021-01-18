import rasterio
from rasterstats import zonal_stats
from potrerosshape import get_potreros_shape
from datetime import datetime

RASTER_DIR = "../raster/"


class __RasterStats:
    """
    A class in charge of getting the information of determined raster files.
    """

    def __init__(self):
        self.raster_stats = {}

    @staticmethod
    def __find_nodata_val(src_readed):
        """
        Given a raster already readed, find the value used as nodata.

        :param src_readed: The data to find the nodata value
        :return: the nodata value found
        """
        # normally, src.nodatavals[0] would do it, but it seems that the actual value used in src does not match
        for i in range(len(src_readed)):
            for j in range(len(src_readed[i])):
                if src_readed[i][j] < 0:
                    return src_readed[i][j]

    def read_raster_stats(self, filename: str):
        """
        Reads a raster file, gets stats of the file and stores them into a dictionary

        :param filename: the raster to read
        :return: a dictionary with the stats information of the raster.
        """

        # check if the filename is already loaded and processed
        if filename not in self.raster_stats:
            # read the file and calculate basic stats
            src = rasterio.open(RASTER_DIR + filename)
            src_readed = src.read(1)

            stats = zonal_stats(get_potreros_shape(), src_readed,
                                affine=src.transform, nodata=self.__find_nodata_val(src_readed),
                                stats="count min mean std max median",
                                geojson_out=True)

            # add the date to the raster stats
            raster_date = get_date_from_filename(filename)
            for i in range(len(stats)):
                stats[i]['date'] = raster_date.strftime("%Y-%m-%d")

            # add the data to the dictionary of loaded and processed files
            self.raster_stats[filename] = stats

        # return the data
        return self.raster_stats[filename]


# instantiate the private class __RasterStats
rasterStats = __RasterStats()


def get_date_from_filename(filename: str):
    """
    Given a raster filename, gets the date represented by that file
    :param filename: the name of the raster file
    :return: the date
    """
    datestr = filename.replace('agrospace_piloto_', '').replace('.tif', '')
    dateobj = datetime.strptime(datestr, "%Y-%m-%d").date()
    return dateobj


def open_raster(filename: str):
    """
    Gets the information of a raster file

    :param filename: the raster file from which to get the information
    :return: a dictionary with the information.
    """
    return rasterStats.read_raster_stats(filename)
