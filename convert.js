import fs from "fs";
import proj4 from "proj4";

// SIRGAS 2000 / UTM 23S (EPSG:31983)
proj4.defs("EPSG:31983",
  "+proj=utm +zone=23 +south +datum=SIRGAS2000 +units=m +no_defs"
);

const src = "EPSG:31983";
const dst = "WGS84";

const csvText = fs.readFileSync("input.csv", "utf8").trim().split(/\r?\n/);

let coordinates = "";

for (let i = 1; i < csvText.length; i++) {
  const cols = csvText[i].split(",");
  const north = parseFloat(cols[1]);
  const east = parseFloat(cols[2]);
  const [lng, lat] = proj4(src, dst, [east, north]);
  
  coordinates += `${lng},${lat},0 `;
}

let kml = `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Polygon</name>
    <Placemark>
      <name>Area</name>
      <Polygon>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
              ${coordinates.trim()}
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>`;

fs.writeFileSync("output.kml", kml, "utf8");
console.log("Done: output.kml");