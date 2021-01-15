import geopandas as gpd


class __PotrerosShape:
    """
    A 'class' to store the read shape of the potreros from a geojson.
    """
    _instance = None
    SHAPE_DIR = "../" + "shape/"
    shape = gpd.read_file(SHAPE_DIR+"agrospace_piloto.geojson")


potrerosShape = __PotrerosShape()


def get_potreros_shape():
    """
    :return: the shape of the potreros.
    """
    return potrerosShape.shape
