import random
import string
import math

from db_handler import DBHandler

ROUND_DIGITS = 2


def generate_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return f"#{r:02x}{g:02x}{b:02x}"


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
        figures_amount=10,
        scale_min=1,
        scale_max=10,
        x_offset_min=-5,
        x_offset_max=5,
        y_offset_min=-5,
        y_offset_max=5,
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
                    "scale": round(random.uniform(scale_min, scale_max), ROUND_DIGITS),
                    "x_offset": round(
                        random.uniform(x_offset_min, x_offset_max), ROUND_DIGITS
                    ),
                    "y_offset": round(
                        random.uniform(y_offset_min, y_offset_max), ROUND_DIGITS
                    ),
                }
            )

        self.db_handler.create_table_whith_data(
            "figures_on_field",
            figures,
            primary_key="id",
            foreign_keys=[
                {"column": "figure_id", "ref_table": "figures", "ref_column": "id"},
                {"column": "figure_id", "ref_table": "vertices", "ref_column": "id"},
                {"column": "color_id", "ref_table": "colors", "ref_column": "id"},
            ],
            column_types={
                "id": "INTEGER",
                "figure_id": "INTEGER",
                "color_id": "INTEGER",
                "x_offset": "REAL",
                "y_offset": "REAL",
                "scale": "REAL",
            },
        )

    # Тут фигуры не те что на поле а как некий класс
    # фигура - набор значений от 0 до 1
    def add_random_figures(
        self,
        figures_amount=5,
    ):

        figures = []
        vertices = []

        vert_count = 0

        for f_index in range(figures_amount):
            sides = f_index + 3
            radius = 0.5
            for vert in range(sides):
                angle = 360 / sides * vert
                x = radius * math.cos(math.radians(angle))
                y = radius * math.sin(math.radians(angle))

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
                    "name": "".join(random.choices(string.ascii_letters, k=5)),
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
