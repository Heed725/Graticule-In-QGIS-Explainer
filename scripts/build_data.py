from __future__ import annotations

import io
import os
import shutil
import urllib.request
import zipfile

import shapefile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

NE_URL = "https://www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip"


def download_natural_earth() -> None:
    print(f"Downloading Natural Earth countries from: {NE_URL}")
    req = urllib.request.Request(NE_URL, headers={"User-Agent": "QGIS-Graticule-Tutorial/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        payload = response.read()

    with zipfile.ZipFile(io.BytesIO(payload)) as zf:
        wanted = {
            "ne_110m_admin_0_countries.shp",
            "ne_110m_admin_0_countries.shx",
            "ne_110m_admin_0_countries.dbf",
            "ne_110m_admin_0_countries.prj",
            "ne_110m_admin_0_countries.cpg",
        }
        names = set(zf.namelist())
        missing = wanted - names
        if missing:
            raise RuntimeError(f"Natural Earth archive is missing expected files: {sorted(missing)}")
        for name in wanted:
            target = os.path.join(DATA, name)
            with zf.open(name) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
            print(f"Wrote {target}")


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

    # Meridians: every 20° from 180°W to 180°E.
    for lon in range(-180, 181, 20):
        points = [[lon, lat] for lat in range(-80, 81, 2)]
        writer.line([points])
        writer.record("longitude", lon, format_lon(lon))

    # Parallels: every 20° from 80°S to 80°N.
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
