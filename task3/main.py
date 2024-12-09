import json

from config import DB_PATH
from db_handler import DBHandler
from polygon_visualizer import PolygonVisualizer


# dbh = DBHandler(db_file=DB_PATH)
# dbh.show_db()
# field_data = [
#     {"id": 1, "figure": "triangle", "size": 5},
#     {"id": 6, "figure": "sqere", "size": 10},
# ]
# dbh.create_table_whith_data(table_name="figures", data=field_data)
# dbh.show_db()


if __name__ == "__main__":

    polygons = [
        {"points": [(0, 0.4), (1, 0), (1, 1), (0, 1)], "color": "#ff5733"},
        {"points": [(2, 2), (3, 2), (2.5, 3.5)], "color": "#33ff57"},
        {
            "points": [(5, 5), (6, 5), (5, 6), (6, 6), (4.5, 5.5)],
            "color": "#3357ff",
        },
    ]
    visualizer = PolygonVisualizer()
    visualizer.display(polygons)
