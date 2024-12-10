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
    def get_column_values(self, cursor: Cursor, table_name: str, column_name: str):
        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        values = cursor.fetchall()
        return [value[0] for value in values]

    @with_db_connection
    def salary_more_then_chief(self, cursor: Cursor):
        query = """
            SELECT 
                e1.ID AS Employee_ID,
                e1.NAME AS Employee_Name,
                e1.SALARY AS Employee_Salary,
                e2.NAME AS Chief_Name,
                e2.SALARY AS Chief_Salary
            FROM 
                EMPLOYEE e1
            JOIN 
                EMPLOYEE e2
            ON 
                e1.CHIEF_ID = e2.ID
            WHERE 
                e1.SALARY > e2.SALARY;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        return values

    @with_db_connection
    def department_max_salary(self, cursor: Cursor):
        query = """
            WITH DepartmentMaxSalary AS (
                SELECT 
                    DEPARTMENT_ID,
                    MAX(SALARY) AS Max_Salary
                FROM 
                    EMPLOYEE
                GROUP BY 
                    DEPARTMENT_ID
            )
            SELECT 
                e.ID AS Employee_ID,
                e.NAME AS Employee_Name,
                e.SALARY AS Employee_Salary,
                d.Max_Salary,
                e.DEPARTMENT_ID
            FROM 
                EMPLOYEE e
            JOIN 
                DepartmentMaxSalary d
            ON 
                e.DEPARTMENT_ID = d.DEPARTMENT_ID
            AND 
                e.SALARY = d.Max_Salary;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        return values

    @with_db_connection
    def department_employee_not_more_then(self, cursor: Cursor, amount):
        query = f"""
            SELECT 
                DEPARTMENT_ID
            FROM 
                EMPLOYEE
            GROUP BY 
                DEPARTMENT_ID
            HAVING 
                COUNT(*) <= {amount};
        """
        cursor.execute(query)
        values = cursor.fetchall()
        return values

    @with_db_connection
    def no_chief_at_same_department(self, cursor: Cursor):
        query = f"""
            SELECT 
                e.ID AS Employee_ID,
                e.NAME AS Employee_Name,
                e.DEPARTMENT_ID
            FROM 
                EMPLOYEE e
            LEFT JOIN 
                EMPLOYEE chief
            ON 
                e.CHIEF_ID = chief.ID
            AND 
                e.DEPARTMENT_ID = chief.DEPARTMENT_ID
            WHERE 
                chief.ID IS NULL;
        """
        cursor.execute(query)
        values = cursor.fetchall()
        return values

    @with_db_connection
    def max_employee_salary_department(self, cursor: Cursor):
        query = f"""
            WITH DepartmentSalary AS (
                SELECT 
                    DEPARTMENT_ID,
                    SUM(SALARY) AS Total_Salary
                FROM 
                    EMPLOYEE
                GROUP BY 
                    DEPARTMENT_ID
            )
            SELECT 
                DEPARTMENT_ID,
                Total_Salary
            FROM 
                DepartmentSalary
            WHERE 
                Total_Salary = (SELECT MAX(Total_Salary) FROM DepartmentSalary);
        """
        cursor.execute(query)
        values = cursor.fetchall()
        return values

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
