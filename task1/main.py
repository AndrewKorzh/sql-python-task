from db_handler import DBHandler
from db_filler import DBFiller


def print_response(response: list, info):
    if isinstance(info, list):
        for ell in info:
            print(ell)
    else:
        print(info)
    for ell in response:
        print(ell)
    print("\n")


if __name__ == "__main__":
    db_file = "employee.db"
    dbf = DBFiller(db_file=db_file)
    dbh = DBHandler(db_file=db_file)

    dbf.department_gen(amount=3)
    dbf.employee_gen(
        chief_amount=3,
        employee_amount=10,
    )
    dbh.show_db()

    print_response(
        response=dbh.salary_more_than_chief(),
        info=[
            "salary_more_than_chief",
            "employee_id | employee_name | emloyee_sallary | chief_name | chief_sallary",
        ],
    )

    print_response(
        response=dbh.department_max_salary(),
        info=[
            "department_max_salary",
            "employee_id | employee_name | emloyee_sallary | department_max_sal | department_id",
        ],
    )

    employee_amount = 3
    print_response(
        response=dbh.department_employee_not_more_than(amount=employee_amount),
        info=[
            f"department_employee_not_more_than {employee_amount}",
            "department_id |",
        ],
    )

    print_response(
        response=dbh.no_chief_at_same_department(),
        info=[
            "no_chief_at_same_department",
            "employee_id | employee_name | department_id",
        ],
    )

    print_response(
        response=dbh.max_employee_salary_department(),
        info=[
            "max_employee_salary_department",
            "DEPARTMENT_ID | Total_Salary",
        ],
    )
