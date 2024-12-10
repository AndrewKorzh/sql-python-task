from functools import wraps
import sqlite3
from sqlite3 import Cursor


def with_db_connection(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        result = func(self, cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return wrapper


class DBHandler:
    def __init__(self, db_file):
        self.db_file = db_file

    @with_db_connection
    def show_db(self, cursor: Cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(self.db_file)
        for table_name in tables:
            print(f"\tТаблица: {table_name[0]}")
            cursor.execute(f"PRAGMA table_info({table_name[0]});")
            columns = cursor.fetchall()
            print("\t\tСтолбцы:")
            for column in columns:
                column_name = column[1]
                column_type = column[2]
                print(f"\t\t\t- {column_name} ({column_type})")
            print("\n")

    @with_db_connection
    def create_table_whith_data(
        self,
        cursor: Cursor,
        table_name,
        data,
        primary_key=None,
        foreign_keys=None,
        column_types={},
    ):
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
            (table_name,),
        )
        if cursor.fetchone():
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        if not isinstance(data, list):
            return

        columns = data[0].keys()
        column_defs = []

        for col in columns:
            col_type = column_types.get(col, "TEXT")
            if col == primary_key:
                column_defs.append(f"{col} {col_type} PRIMARY KEY")
            else:
                column_defs.append(f"{col} {col_type}")

        if foreign_keys:
            for fk in foreign_keys:
                column_defs.append(
                    f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['ref_table']}({fk['ref_column']})"
                )

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_defs)});"
        cursor.execute(create_table_query)

        for row in data:
            placeholders = ", ".join("?" for _ in row)
            insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row.values()))

    @with_db_connection
    def clear_db(self, cursor: Cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            if table_name[0] == "sqlite_sequence":
                continue
            cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
            print(f"Таблица {table_name[0]} была удалена.")

    @with_db_connection
    def get_column_values(self, cursor: Cursor, table_name: str, column_name: str):
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        values = cursor.fetchall()
        return [value[0] for value in values]

    @with_db_connection
    def get_all_field_polygons(self, cursor: Cursor):
        query = """
            SELECT 
                fof.scale,
                fof.x_offset,
                fof.y_offset,
                c.hex AS color,
                GROUP_CONCAT('(' || v.x || ',' || v.y || ')' ORDER BY v.vert_order) AS points
            FROM 
                figures_on_field fof
            JOIN 
                colors c ON fof.color_id = c.id
            JOIN 
                vertices v ON fof.figure_id = v.figure_id
            GROUP BY 
                fof.scale, fof.x_offset, fof.y_offset, c.hex;
            """

        cursor.execute(query)
        rows = cursor.fetchall()

        polygons = []
        for row in rows:
            scale, x_offset, y_offset, color, points = row

            points_list = [
                tuple(map(float, point.strip("()").split(",")))
                for point in points.split("),(")
            ]

            polygons.append(
                {
                    "scale": scale,
                    "x_offset": x_offset,
                    "y_offset": y_offset,
                    "color": color,
                    "points": points_list,
                }
            )

        return polygons
