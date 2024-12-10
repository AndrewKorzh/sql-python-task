import random
import string
import math

from db_handler import DBHandler


class DBFiller:
    def __init__(self, db_file):
        self.db_handler = DBHandler(db_file=db_file)

    def department_gen(self, amount=5):
        departments = [
            {"id": i + 1, "name": f"department_{i+1}"} for i in range(amount)
        ]

        self.db_handler.create_table_whith_data(
            "department",
            departments,
            primary_key="id",
            column_types={
                "id": "INTEGER",
            },
        )

    def employee_gen(
        self,
        employee_amount=20,
        chief_amount=5,
        salary_min=70000,
        salary_max=300000,
    ):
        employee_ids = [i for i in range(employee_amount)]
        chief_ids = random.sample(employee_ids, chief_amount)

        departments_ids = self.db_handler.get_column_values(
            table_name="department",
            column_name="id",
        )

        employee = []

        for employee_id in employee_ids:
            chief_id = None
            if not employee_id in chief_ids:
                chief_id = random.choice(chief_ids)
            employee.append(
                {
                    "id": employee_id,
                    "department_id": random.choice(departments_ids),
                    "chief_id": chief_id,
                    "name": f"employee_{employee_id}",
                    "salary": random.randint(salary_min, salary_max),
                }
            )

        self.db_handler.create_table_whith_data(
            "employee",
            employee,
            primary_key="id",
            column_types={
                "id": "INTEGER",
                "department_id": "INTEGER",
                "chief_id": "INTEGER",
                "salary": "INTEGER",
            },
            foreign_keys=[
                {"column": "chief_id", "ref_table": "employee", "ref_column": "id"},
                {
                    "column": "department_id",
                    "ref_table": "department",
                    "ref_column": "id",
                },
            ],
        )
