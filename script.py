import json
import numpy as np
from PIL import Image

# ---------- 1) Load JSON ----------
with open("elevation.json", "r") as f:
    data = json.load(f)

results = data["results"]

rows = len(results)
cols = len(results[0])

# ---------- 2) Build elevation array ----------
elev = np.array([[pt["elevation"] for pt in row] for row in results],
                dtype=float)

# ---------- 3) Normalize to 0–255 ----------
emin = float(elev.min())
emax = float(elev.max())

norm = (elev - emin) / (emax - emin + 1e-9)   # avoid divide-by-zero
img_array = (norm * 255).astype(np.uint8)

# Optional: flip vertically so north is up
img_array = np.flipud(img_array)

# ---------- 4) Save grayscale image ----------
img = Image.fromarray(img_array, mode="L")
png_name = "elevation_heightmap.png"
img.save(png_name)
print(f"Saved PNG: {png_name}")

# ---------- 5) Compute geographic bounds ----------
# assuming grid is regular (each cell has lat/lon)
all_lats = [pt["latitude"] for row in results for pt in row]
all_lons = [pt["longitude"] for row in results for pt in row]

south = min(all_lats)
north = max(all_lats)
west  = min(all_lons)
east  = max(all_lons)

print("Bounds:")
print("  north:", north)
print("  south:", south)
print("  west :", west)
print("  east :", east)

# ---------- 6) Write KML GroundOverlay ----------
kml_name = "elevation_overlay.kml"

kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Elevation Overlay</name>
    <GroundOverlay>
      <name>Elevation Heightmap</name>
      <Icon>
        <href>{png_name}</href>
      </Icon>
      <LatLonBox>
        <north>{north}</north>
        <south>{south}</south>
        <east>{east}</east>
        <west>{west}</west>
        <rotation>0</rotation>
      </LatLonBox>
    </GroundOverlay>
  </Document>
</kml>
"""

with open(kml_name, "w", encoding="utf-8") as f:
    f.write(kml_content)

print(f"Saved KML: {kml_name}")
