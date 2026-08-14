from __future__ import annotations

import os
import urllib.request

import shapefile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

# Natural Earth's maintained vector repository on GitHub. Pull the individual
# 1:110m Admin 0 Countries shapefile components so this workflow stays small
# and reproducible.
NE_RAW_BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/110m_cultural"
NE_FILES = [
    "ne_110m_admin_0_countries.shp",
    "ne_110m_admin_0_countries.shx",
    "ne_110m_admin_0_countries.dbf",
    "ne_110m_admin_0_countries.prj",
    "ne_110m_admin_0_countries.cpg",
]


def download_file(url: str, target: str) -> None:
    print(f"Downloading {url}")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Graticule-In-QGIS-Explainer/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = response.read()
    if not payload:
        raise RuntimeError(f"Downloaded file was empty: {url}")
    with open(target, "wb") as f:
        f.write(payload)
    print(f"Wrote {target} ({len(payload):,} bytes)")


def download_natural_earth() -> None:
    for name in NE_FILES:
        download_file(f"{NE_RAW_BASE}/{name}", os.path.join(DATA, name))


def format_lon(value: int) -> str:
    if value < 0:
        return f"{abs(value)}°W"
    if value > 0:
        return f"{value}°E"
    return "0°"


def format_lat(value: int) -> str:
    if value < 0:
        return f"{abs(value)}°S"
    if value > 0:
        return f"{value}°N"
    return "0°"


def build_graticule() -> None:
    base = os.path.join(DATA, "graticule_20deg")
    writer = shapefile.Writer(base, shapeType=shapefile.POLYLINE)
    writer.field("type", "C", size=10)
    writer.field("value", "N", size=6, decimal=1)
    writer.field("label", "C", size=20)

    # Meridians every 20 degrees from 180 W to 180 E.
    for lon in range(-180, 181, 20):
        points = [[lon, lat] for lat in range(-80, 81, 2)]
        writer.line([points])
        writer.record("longitude", lon, format_lon(lon))

    # Parallels every 20 degrees from 80 S to 80 N.
    for lat in range(-80, 81, 20):
        points = [[lon, lat] for lon in range(-180, 181, 2)]
        writer.line([points])
        writer.record("latitude", lat, format_lat(lat))

    writer.close()

    prj = (
        'GEOGCS["WGS 84",DATUM["WGS_1984",'
        'SPHEROID["WGS 84",6378137,298.257223563]],'
        'PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],'
        'AUTHORITY["EPSG","4326"]]'
    )
    with open(base + ".prj", "w", encoding="utf-8") as f:
        f.write(prj)
    with open(base + ".cpg", "w", encoding="utf-8") as f:
        f.write("UTF-8")

    print("Generated 20-degree EPSG:4326 graticule shapefile")


if __name__ == "__main__":
    download_natural_earth()
    build_graticule()
