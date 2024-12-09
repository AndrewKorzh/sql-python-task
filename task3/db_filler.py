import random
import string
import json

from db_handler import DBHandler
from config import DB_PATH


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return f"#{r:02x}{g:02x}{b:02x}"


# Важно - отдельные функции для генерации, отдельные для вставки
class DBFiller:
    def __init__(self, db_file):
        self.db_handler = DBHandler(db_file=db_file)

    def add_random_collors(self, amount=5):
        colors = [{"id": i, "hex": generate_random_color()} for i in range(amount)]

        self.db_handler.create_table_whith_data(
            "colors",
            colors,
            primary_key="id",
            column_types={
                "id": "INTEGER",
            },
        )

    def gen_field(
        self,
        figures_amount=12,
        scale_min=1,
        scale_max=10,
        x_start_min=-5,
        x_start_max=5,
        y_start_min=-5,
        y_start_max=5,
    ):
        figures = []

        color_ids = self.db_handler.get_column_values(
            table_name="colors",
            column_name="id",
        )

        figures_ids = self.db_handler.get_column_values(
            table_name="figures",
            column_name="id",
        )

        for f_index in range(figures_amount):
            figures.append(
                {
                    "id": f_index,
                    "figure_id": random.choice(figures_ids),
                    "color_id": random.choice(color_ids),
                    "scale": random.uniform(scale_min, scale_max),
                    "x_start": random.uniform(x_start_min, x_start_max),
                    "y_start": random.uniform(y_start_min, y_start_max),
                }
            )

        self.db_handler.create_table_whith_data(
            "field",
            figures,
            primary_key="id",
            foreign_keys=[
                {"column": "figure_id", "ref_table": "figures", "ref_column": "id"},
                {"column": "color_id", "ref_table": "colors", "ref_column": "id"},
            ],
            column_types={
                "id": "INTEGER",
                "figure_id": "INTEGER",
                "color_id": "INTEGER",
                "x_start": "REAL",
                "y_start": "REAL",
                "scale": "REAL",
            },
        )

    # Тут фигуры не те что на поле а как некий класс
    # фигура - набор значений от 0 до 1
    def add_random_figures(
        self,
        figures_amount=5,
        vertices_amount=5,
    ):

        figures = []
        vertices = []

        vert_count = 0

        for f_index in range(figures_amount):
            for vert in range(vertices_amount):
                if vert == 0:
                    x, y = 0, 0
                else:
                    x, y = random.uniform(0, 1), random.uniform(0, 1)

                point = {
                    "id": vert_count,
                    "x": x,
                    "y": y,
                    "figure_id": f_index,
                    "vert_order": vert,
                }
                vertices.append(point)
                vert_count += 1

            figures.append(
                {
                    "id": f_index,
                    "figure_name": "".join(random.choices(string.ascii_letters, k=5)),
                }
            )

        self.db_handler.create_table_whith_data(
            "figures",
            figures,
            primary_key="id",
            column_types={
                "id": "INTEGER",
            },
        )
        self.db_handler.create_table_whith_data(
            "vertices",
            vertices,
            primary_key="id",
            foreign_keys=[
                {
                    "column": "figure_id",
                    "ref_table": "figures",
                    "ref_column": "id",
                }
            ],
            column_types={
                "id": "INTEGER",
                "x": "REAL",
                "y": "REAL",
                "figure_id": "INTEGER",
                "vert_order": "INTEGER",
            },
        )


if __name__ == "__main__":
    dbf = DBFiller(db_file=DB_PATH)
    dbf.add_random_collors()

    dbf.add_random_figures()

    dbf.gen_field()
