import geopandas as gpd
import matplotlib.colors
import matplotlib.pyplot as plt
import rioxarray as rxr
from rasterio.crs import CRS
from shapely.geometry import mapping

params = {
    "lines.linewidth": 3,
    "font.size": 16,
    "savefig.dpi": 150,
}
plt.rcParams.update(params)

elevation_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    "", ["#4a9c0f", "#fffa68", "#ffb326", "#92641e", "#ffffff"]
)


def clip(
    raster="eu_dem_v11_E50N10/eu_dem_v11_E50N10.TIF",
    shapefile="shapefiles/city/EL003L1_PATRA_UA2012_Boundary.shp",
):
    elevation_gr = rxr.open_rasterio(raster, masked=True).squeeze()
    patras_shp = gpd.read_file(shapefile)
    patras_shp = patras_shp.set_crs("epsg:4285")
    elevation_clipped = elevation_gr.rio.clip(
        patras_shp.geometry.apply(mapping)
    )
    elevation_clipped.rio.to_raster("clipped.tif")


elevation = rxr.open_rasterio("clipped.tif", masked=True).squeeze()
crs_wgs84 = CRS.from_string("EPSG:4326")
elevation_wgs84 = elevation.rio.reproject(crs_wgs84)
coords_shp = gpd.read_file("shapefiles/coords/cam_coords.shp")

fig, ax = plt.subplots(figsize=(8, 5))
elevation_wgs84.plot(
    ax=ax,
    cmap=elevation_cmap,
    vmin=elevation.min().item(),
    vmax=elevation.max().item(),
    cbar_kwargs={"label": "$Elevation  \ (m)$"},
)
coords_shp.plot(ax=ax, color="red", edgecolor="black")
plt.title(None)
plt.tight_layout()
plt.savefig("elevation_map.png")
# plt.show()
