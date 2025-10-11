import sql_connector
import log_writer
import formatter
import log_stats

from menu_case1 import run_case1
from menu_case2 import run_case2
from menu_case3 import run_case3
from menu_case4 import run_case4

def main():
    print("\tMain menu choose one option")
    while True:
        try:
            menu = int(input(
                """To search by keyword choose 1, 
To search by year of production choose 2, 
To search by genre choose 3, 
If you want to see statistics choose 4 
For exit choose 5
> """))
            if menu not in [1, 2, 3, 4, 5]:
                print("Please enter a number between 1 and 5.")
                continue
        except ValueError:
            print("Invalid input. Please enter only numbers 1 to 5.")
            continue

        if menu == 1:
            run_case1()
        elif menu == 2:
            run_case2()
        elif menu == 3:
            run_case3()
        elif menu == 4:
            run_case4()
        elif menu == 5:
            log_writer.close_mongo()
            print("Connections closed. Goodbye!")
            break

if __name__ == "__main__":
    main()
