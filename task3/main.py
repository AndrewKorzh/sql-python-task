from db_handler import DBHandler
from db_filler import DBFiller
from polygon_visualizer import PolygonVisualizer


if __name__ == "__main__":
    db_file = "figures.db"
    dbf = DBFiller(db_file=db_file)
    dbh = DBHandler(db_file=db_file)

    dbf.add_random_collors(
        amount=4,
    )
    dbf.add_random_figures(
        figures_amount=4,
    )
    dbf.gen_field(
        figures_amount=10,
        scale_min=1,
        scale_max=3,
    )

    polygons = dbh.get_all_field_polygons()
    visualizer = PolygonVisualizer()
    visualizer.display(polygons)
