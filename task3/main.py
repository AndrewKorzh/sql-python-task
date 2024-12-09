import json

from config import DB_PATH
from db_handler import DBHandler
from db_filler import DBFiller
from polygon_visualizer import PolygonVisualizer


if __name__ == "__main__":
    dbf = DBFiller(db_file=DB_PATH)
    dbh = DBHandler(db_file=DB_PATH)

    dbf.add_random_collors(amount=10)
    dbf.add_random_figures(figures_amount=10)
    dbf.gen_field(
        figures_amount=20,
        scale_min=1,
        scale_max=3,
    )

    polygons = dbh.get_all_field_polygons()
    visualizer = PolygonVisualizer()
    visualizer.display(polygons)
