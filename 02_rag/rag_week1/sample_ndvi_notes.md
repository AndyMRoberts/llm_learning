# Starter notes (replace with real papers!)

## NDVI
The Normalized Difference Vegetation Index is NDVI = (NIR - Red) / (NIR + Red).
Values range from -1 to 1. Dense healthy vegetation typically gives high positive values,
bare soil gives values near zero, and water is negative. NDVI saturates in dense canopies.

## NDRE
NDRE = (NIR - RedEdge) / (NIR + RedEdge). Red-edge reflectance penetrates deeper into the
canopy, so NDRE is often more sensitive than NDVI to chlorophyll content in mid/late-season crops.

## SAVI
SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L), where L is a soil brightness correction
factor, commonly 0.5. It reduces soil background effects in sparse canopies.
