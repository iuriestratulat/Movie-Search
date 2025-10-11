import sql_connector
import formatter
import log_writer

def run_case2():
    print("\tSearching by years menu")
    while True:
        try:
            menu_case_2 = int(input("""To search by one year choose 1, 
To search by interval choose 2, 
For exit to main menu choose 3
> """))
            if menu_case_2 not in [1, 2, 3]:
                print("Please enter a number between 1 and 3.")
                continue
        except ValueError:
            print("Invalid input. Please enter only numbers 1 to 3.")
            continue

        # --- Case 1: Search by single year ---
        if menu_case_2 == 1:
            min_year = sql_connector.get_min_year()
            max_year = sql_connector.get_max_year()
            if min_year is None or max_year is None:
                print("Could not retrieve available years from database.")
                break

            print(f"You can choose one year from the interval: {min_year} - {max_year}")
            while True:
                year_input = input(f"Enter a year ({min_year}-{max_year}, or press Enter to return): ").strip()
                if year_input == "":
                    break
                try:
                    year = int(year_input)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if year not in range(min_year, max_year + 1):
                    print(f"Year must be between {min_year} and {max_year}.")
                    continue

                offset = 0
                ok, results = sql_connector.get_films_by_year(year, offset)
                results = results or []
                log_writer.log_query("by_year", {"year": year}, len(results) if ok else 0)

                if not ok or not results:
                    print("No films found for the selected year.")
                    continue

                formatter.print_table_results(
                    [(title or '', desc or '', y or '') for _, title, desc, y in results],
                    ["Title", "Description", "Release Year"],
                    "No films found for this year.",
                    start_index=offset + 1
                )

                while True:
                    more = input("Show more results? (y/n): ").lower().strip()
                    if more == "y":
                        offset += 10
                        ok, results = sql_connector.get_films_by_year(year, offset)
                        results = results or []
                        log_writer.log_query("by_year", {"year": year}, len(results) if ok else 0)

                        if not ok or not results:
                            print("No more results.")
                            break

                        formatter.print_table_results(
                            [(title or '', desc or '', y or '') for _, title, desc, y in results],
                            ["Title", "Description", "Release Year"],
                            "No films found for this year.",
                            start_index=offset + 1
                        )
                    elif more == "n":
                        break
                    else:
                        print("Please enter only 'y' or 'n'.")

        # --- Case 2: Search by year interval ---
        elif menu_case_2 == 2:
            min_year = sql_connector.get_min_year()
            max_year = sql_connector.get_max_year()
            if min_year is None or max_year is None:
                print("Could not retrieve years from the database.")
                continue

            print(f"You can choose years from the interval: {min_year} - {max_year}")
            while True:
                first_year_input = input(f"Enter first year ({min_year}-{max_year}, or press Enter to return): ").strip()
                if first_year_input == "":
                    break
                try:
                    first_year = int(first_year_input)
                except ValueError:
                    print("Invalid input. Please enter a valid year.")
                    continue
                if first_year not in range(min_year, max_year + 1):
                    print(f"Year must be between {min_year} and {max_year}.")
                    continue

                second_year_input = input(f"Enter second year ({min_year}-{max_year}, or press Enter to return): ").strip()
                if second_year_input == "":
                    break
                try:
                    second_year = int(second_year_input)
                except ValueError:
                    print("Invalid input. Please enter a valid year.")
                    continue
                if second_year not in range(min_year, max_year + 1):
                    print(f"Year must be between {min_year} and {max_year}.")
                    continue
                if first_year > second_year:
                    print("First year cannot be greater than second year.")
                    continue

                offset = 0
                ok, data = sql_connector.get_films_by_years_interval(first_year, second_year, offset)
                data = data or []
                log_writer.log_query(
                    "years_interval",
                    [{"firstyear": first_year}, {"secondyear": second_year}],
                    len(data) if ok else 0
                )

                if not ok or not data:
                    print("No films found for the chosen year interval.")
                    continue

                formatter.print_table_results(
                    [(title or '', desc or '', y or '') for _, title, desc, y in data],
                    ["Title", "Description", "Release Year"],
                    "No films found for this interval.",
                    start_index=offset + 1
                )

                while True:
                    more = input("Show more results? (y/n): ").lower().strip()
                    if more == "y":
                        offset += 10
                        ok, data = sql_connector.get_films_by_years_interval(first_year, second_year, offset)
                        data = data or []
                        log_writer.log_query(
                            "years_interval",
                            [{"firstyear": first_year}, {"secondyear": second_year}],
                            len(data) if ok else 0
                        )

                        if not ok or not data:
                            print("No more results.")
                            break

                        formatter.print_table_results(
                            [(title or '', desc or '', y or '') for _, title, desc, y in data],
                            ["Title", "Description", "Release Year"],
                            "No films found for this interval.",
                            start_index=offset + 1
                        )
                    elif more == "n":
                        break
                    else:
                        print("Please enter only 'y' or 'n'.")

        # --- Exit back to main menu ---
        elif menu_case_2 == 3:
            break

    print("\tMain menu choose one option")
