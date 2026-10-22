import csv


def load_tilemap(tilemap_path):

    with open(tilemap_path, newline='') as csvfile:

        reader = csv.reader(csvfile)

        tilemap = [row for row in reader]

    return tilemap


tilemap = load_tilemap("maps/tilemap.csv")


print("Tile map loaded successfully")
print("Rows:", len(tilemap))
print("Columns:", len(tilemap[0]))