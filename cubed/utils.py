# Standard library imports

import json
from pathlib import Path
from datetime import datetime
import multiprocessing as mp
from typing import Dict, Any, Union
import time

# Third party imports
import pandas as pd
import geopandas as gpd
from osgeo import gdal
import xarray as xr
import rioxarray
from shapely.geometry import mapping


try:
    from rich import print
except ImportError:
    pass


def parse_bandmap(
    sat, path: Path = Path("./bandmap.json")
) -> Union[Dict[str, str], None]:
    """TODO: Docstring for parse_bandmap.

    Parameters
    ----------
    path : TODO

    Returns
    -------
    TODO

    """
    if not isinstance(path, Path):
        try:
            path = Path(path)
        except TypeError:
            print("Invalid path type")

    with open(path.resolve(), "r") as fp:
        band_map = json.load(fp)
    try:
        sat_map = band_map.get(sat)
        return sat_map
    except ValueError:
        print(f"{sat} not in available band map")
        return None


def inv_bandmap(band_map: Dict[str, str]) -> Dict[str, str]:
    """Generate inverted band, common name dictonary

    Parameters
    ----------
    band_map : dict
        Band map for data product

    Returns
    -------
    dict
        Band map with inverted band name and common name key, value pair

    Example
    -------
        bmap =  {"HLSS30.v2.0": {
                "B01": "aerosal"}}
        inv_bandmap(bmap)

    """
    inv_dict = {}
    collections = list(band_map.keys())
    for c in collections:
        inv_dict[c] = {v: k for k, v in band_map.get(c).items()}
    return inv_dict
