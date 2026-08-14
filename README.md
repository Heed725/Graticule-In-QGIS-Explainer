# Graticule in QGIS Explainer

A practical, beginner-friendly guide to **graticules, latitude/longitude labels, label positioning, frames, coordinate formats, and Natural Earth data in QGIS**.

This repository includes:

- a compact Natural Earth world countries shapefile (`data/ne_110m_admin_0_countries.*`)
- a generated 20-degree latitude/longitude graticule shapefile (`data/graticule_20deg.*`)
- an example QGIS project (`project/Graticule_In_QGIS_Example.qgs`)
- this complete step-by-step tutorial

> The main lesson: in a geographic graticule, **X = longitude** and **Y = latitude**. For a conventional rectangular map, put longitude labels on the **top/bottom** and latitude labels on the **left/right**.

## 1. What is a graticule?

A graticule is the network of geographic coordinate lines drawn over a map.

- **Meridians** are lines of longitude and generally run north-south.
- **Parallels** are lines of latitude and generally run east-west.

Typical labels are:

- Longitude: `30°W`, `0°`, `30°E`
- Latitude: `20°S`, `0°`, `20°N`

For a simple rectangular geographic map:

```text
                  LONGITUDE
            20°W    0°    20°E
                   TOP
        ┌───────────────────────┐
  20°N  │                       │ 20°N
        │                       │
LATITUDE│          MAP          │LATITUDE
        │                       │
  20°S  │                       │ 20°S
        └───────────────────────┘
                  BOTTOM
            20°W    0°    20°E
```

A clean convention is therefore:

| Map side | Coordinate component |
|---|---|
| Top | Longitude / X |
| Bottom | Longitude / X |
| Left | Latitude / Y |
| Right | Latitude / Y |

For a minimalist report map, use only **bottom = longitude** and **left = latitude**.

## 2. Repository structure

```text
Graticule-In-QGIS-Explainer/
├── README.md
├── data/
│   ├── ne_110m_admin_0_countries.shp
│   ├── ne_110m_admin_0_countries.shx
│   ├── ne_110m_admin_0_countries.dbf
│   ├── ne_110m_admin_0_countries.prj
│   ├── graticule_20deg.shp
│   ├── graticule_20deg.shx
│   ├── graticule_20deg.dbf
│   └── graticule_20deg.prj
└── project/
    └── Graticule_In_QGIS_Example.qgs
```

## 3. Natural Earth data

Natural Earth provides public-domain cultural and physical vector data at approximately **1:10m, 1:50m and 1:110m** scales. This example uses a compact low-resolution world countries dataset derived from Natural Earth, which is ideal for learning world-map graticules.

For a new project, you can also download current Natural Earth layers such as:

- Admin 0 Countries
- Coastline
- Land
- Ocean
- Lakes
- Rivers and lake centerlines

For global teaching maps, **1:110m** is usually enough. Use 1:50m or 1:10m when you need more detail.

## 4. Open the example project

1. Clone or download this repository.
2. Open QGIS.
3. Choose **Project → Open**.
4. Open:

```text
project/Graticule_In_QGIS_Example.qgs
```

The project uses relative paths, so keep the `data` and `project` folders together.

The project contains:

- Natural Earth world countries
- a 20° vector graticule layer

The vector graticule is useful for understanding the geometry, but for polished map output you should normally create the final graticule in the **QGIS Print Layout**, because Layout gives much better annotation control.

## 5. Create a Print Layout

Go to:

```text
Project → New Print Layout
```

Give it a name, for example:

```text
Natural Earth Graticule Tutorial
```

Then:

```text
Add Item → Add Map
```

Draw a map rectangle on the page.

Select the map item. The right-side **Item Properties** panel contains the controls for extent, scale, CRS, frames and grids.

## 6. Add a graticule in the Layout

With the Layout map selected:

```text
Item Properties → Grids → +
```

Rename the grid to something useful, for example:

```text
Latitude Longitude Graticule
```

Enable:

```text
Draw grid
```

## 7. Set the grid CRS to EPSG:4326

For latitude/longitude annotations, set the grid CRS to:

```text
EPSG:4326 — WGS 84
```

This is important even if the **map itself uses another projection** such as Equal Earth, Robinson, Mercator or a national projected CRS.

Think of them separately:

```text
MAP CRS  → controls how the map is projected
GRID CRS → controls what coordinates the grid represents
```

A projected map can therefore still have latitude/longitude labels such as `10°S` and `35°E`.

## 8. Understand X and Y intervals

For an EPSG:4326 grid:

```text
X = Longitude
Y = Latitude
```

Therefore:

- **X interval** = spacing between meridians
- **Y interval** = spacing between parallels

Example:

```text
X interval = 20
Y interval = 20
```

This creates longitude lines every 20 degrees and latitude lines every 20 degrees.

The included `graticule_20deg.shp` demonstrates this concept as a normal vector layer.

## 9. Choose an interval appropriate to the map scale

Do not use the same interval for every map.

Suggested starting points:

| Map extent | Starting interval |
|---|---:|
| World | 20°–30° |
| Continent | 5°–10° |
| Country | 1°–5° |
| Region | 0.25°–1° |
| District/local area | 0.05°–0.5° |

For a world Natural Earth map, try:

```text
X interval = 30°
Y interval = 20°
```

Too many lines make the map look like graph paper.

## 10. Turn on coordinate annotations

In the grid settings, enable:

```text
Draw coordinates
```

The map will now show coordinate values around the frame.

The goal is usually not to show every coordinate type on every side. Filter the sides so the reader immediately understands what each number represents.

## 11. Correct label positioning

For a conventional rectangular map:

```text
TOP    = Longitude / X only
BOTTOM = Longitude / X only
LEFT   = Latitude / Y only
RIGHT  = Latitude / Y only
```

Why?

A longitude meridian intersects the top and bottom edges, while a latitude parallel intersects the left and right edges.

### Full four-sided configuration

Use this for atlas-style or formal cartographic maps:

| Side | Setting |
|---|---|
| Top | Longitude / X only |
| Bottom | Longitude / X only |
| Left | Latitude / Y only |
| Right | Latitude / Y only |

### Minimal publication configuration

For reports, theses and papers, this is often cleaner:

| Side | Setting |
|---|---|
| Top | Disabled |
| Right | Disabled |
| Bottom | Longitude / X only |
| Left | Latitude / Y only |

That avoids duplicated coordinate information.

## 12. Coordinate format

For most general-purpose cartography, use a format that displays directional suffixes.

Instead of:

```text
-20
0
20
```

prefer:

```text
20°W
0°
20°E
```

For latitude:

```text
20°S
0°
20°N
```

Directional suffixes are immediately understandable and avoid forcing the reader to remember that negative longitude means west and negative latitude means south.

## 13. Precision

For a world map, use zero decimal places unless there is a special reason not to.

Good:

```text
20°E
6°S
```

Usually unnecessary:

```text
20.000000°E
6.000000°S
```

For detailed maps you may need decimal degrees or degrees/minutes/seconds.

## 14. Inside versus outside labels

For publication maps, **outside the frame** is usually the cleanest choice.

Outside annotations:

- do not cover geographic features
- give a strong visual frame
- are easier to scan

Inside annotations can be useful when page space is tight, but they may collide with map content.

## 15. Annotation distance

If labels sit directly against the map border, increase the annotation distance.

A useful starting range is:

```text
1.5 mm to 3 mm
```

Then adjust visually according to font size and final page dimensions.

## 16. Label orientation

For most modern maps:

- top/bottom longitude labels → horizontal
- left/right latitude labels → horizontal

Rotated labels can save space, but horizontal labels are generally easier to read.

## 17. Frame, grid and annotation are different things

These three components can be controlled separately:

```text
FRAME       = border around the map
GRID        = lines crossing the map
ANNOTATIONS = coordinate text around the frame
```

Possible designs include:

- Frame + Grid + Annotations
- Grid + Annotations
- Frame + Annotations but no interior grid lines
- Minimal ticks + Annotations

A frame with coordinate labels but no full internal lines is often excellent for thematic maps because it provides location reference without covering the data.

## 18. Graticule versus projected coordinate grid

Do not confuse a geographic graticule with a measured/projected grid.

### Geographic graticule

Uses:

- longitude
- latitude
- degrees

Examples:

```text
35°E
6°S
```

Typically created with grid CRS `EPSG:4326`.

### Projected coordinate grid

Uses coordinate units such as metres:

```text
500000 E
9200000 N
```

This is common for UTM and national projected CRSs.

## 19. Projected world maps

If your map uses a curved global projection, the geographic graticule may also curve. That is correct.

Conceptually:

```text
EPSG:4326 latitude/longitude grid
                 ↓
          transformed to
                 ↓
          the map projection
```

So on Equal Earth, Robinson, Winkel Tripel and similar projections, meridians and parallels do not necessarily appear as straight vertical/horizontal lines.

## 20. Tanzania example

A Tanzania map is approximately within longitudes around 29°E–41°E and latitudes around 1°S–12°S.

A useful first grid interval is:

```text
2° × 2°
```

Longitude labels might be:

```text
30°E  32°E  34°E  36°E  38°E  40°E
```

Latitude labels might be:

```text
2°S  4°S  6°S  8°S  10°S  12°S
```

For a Tanzania layout, a clean configuration is:

```text
LEFT   = Latitude / Y
BOTTOM = Longitude / X
TOP    = Off
RIGHT  = Off
```

Natural Earth is good for regional and international context. For detailed Tanzania regions, districts or wards, combine it with a more detailed Tanzania administrative boundary dataset.

## 21. Equator, Prime Meridian and Date Line

Important reference lines are:

```text
Equator        = latitude 0°
Prime Meridian = longitude 0°
Date Line      ≈ longitude ±180°
```

A normal QGIS Layout grid applies the same style to all grid lines. If you want the Equator or Prime Meridian to be visually stronger, use a separate vector layer or duplicate styling approach.

Near ±180°, inspect labels manually because map projections and wraparound can make edge annotations visually awkward.

## 22. Common mistakes

### Mistake 1: Latitude and longitude mixed on all four sides

Fix the side filters:

```text
Top/Bottom → X / longitude
Left/Right → Y / latitude
```

### Mistake 2: Too many grid lines

Increase the X/Y interval.

### Mistake 3: Too much precision

Use whole degrees for world and continental maps unless precision is genuinely needed.

### Mistake 4: Grid lines are visually stronger than the actual map

Use thin, subtle lines. The graticule is supporting information, not usually the main subject.

### Mistake 5: Corner labels overlap

Try one or more of:

- disable top labels
- disable right labels
- increase annotation distance
- reduce font size slightly
- increase grid interval
- increase page margin

### Mistake 6: Using projected metres when you intended degrees

Set the **grid CRS** to EPSG:4326.

## 23. Suggested styling

A good starting hierarchy for a Natural Earth map is:

```text
Country/coastline geometry → most visible
Thematic information      → strongly visible
Labels                    → clear
Graticule                  → subtle
```

Suggested starting values:

| Element | Suggested starting point |
|---|---|
| Graticule line | 0.10–0.20 mm |
| Coordinate labels | 7–9 pt |
| Map frame | 0.30–0.50 mm |
| Annotation distance | 1.5–3 mm |

Always judge styling at the **final export size**.

## 24. Recommended Natural Earth world-map configuration

For a clean global map:

```text
Grid CRS: EPSG:4326
X interval: 30°
Y interval: 20°
Draw grid: On
Draw coordinates: On
Coordinate format: Decimal with directional suffix
Precision: 0
```

### Full-frame labels

```text
LEFT   = Latitude / Y only
RIGHT  = Latitude / Y only
TOP    = Longitude / X only
BOTTOM = Longitude / X only
```

### Minimal labels

```text
LEFT   = Latitude / Y only
BOTTOM = Longitude / X only
TOP    = Off
RIGHT  = Off
```

## 25. Vector graticule included in this repository

The file:

```text
data/graticule_20deg.shp
```

contains:

- longitude lines every 20° from 180°W to 180°E
- latitude lines every 20° from 80°S to 80°N
- attributes identifying whether each feature is latitude or longitude
- a ready-to-use text label such as `40°W`, `20°S`, `0°`, `60°E`

Open its attribute table to see:

```text
type
value
label
```

This layer is useful for learning, analysis or custom styling. For normal layout coordinate labels, prefer QGIS Layout's built-in grid system.

## 26. Optional: label the vector graticule itself

To practice labeling a vector graticule:

1. Select `graticule_20deg`.
2. Open **Layer Properties → Labels**.
3. Choose **Single Labels**.
4. Label using the `label` field.
5. Use placement rules carefully; labeling every grid line over the full world often becomes cluttered.

This is fundamentally different from **Layout coordinate annotations**, which are placed against the map frame and are normally cleaner for final cartography.

## 27. Exporting

From the Layout, export as:

- PDF for reports and printing
- SVG for vector editing
- PNG/TIFF for images

Before exporting, check:

- label collisions at corners
- ±180° labels
- page margins
- font readability
- grid line weight
- whether the chosen interval still looks good at final size

## 28. Quick checklist

- [ ] Natural Earth layer loaded
- [ ] Correct map CRS chosen
- [ ] Layout map created
- [ ] Grid added
- [ ] Grid CRS = EPSG:4326 for latitude/longitude
- [ ] X interval chosen for longitude
- [ ] Y interval chosen for latitude
- [ ] Draw coordinates enabled
- [ ] Longitude restricted to top/bottom where appropriate
- [ ] Latitude restricted to left/right where appropriate
- [ ] Directional suffix format selected
- [ ] Unnecessary decimal places removed
- [ ] Annotation distance checked
- [ ] Corner overlaps checked
- [ ] Grid lines kept visually subtle
- [ ] Final PDF/PNG inspected at intended size

## Data source and attribution

Natural Earth is a public-domain map dataset created and maintained by the Natural Earth community with support from NACIS. The compact world-country sample in this repository is derived from Natural Earth data and is included for education and demonstration.

Natural Earth: https://www.naturalearthdata.com/

QGIS documentation: https://docs.qgis.org/

## License

The tutorial text and generated graticule may be reused and adapted. Natural Earth data is public domain under Natural Earth's terms of use. See the upstream sources for the most current data and documentation.
