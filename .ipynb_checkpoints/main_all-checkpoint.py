import sql_connector
import formatter
import log_writer
import log_stats

# ------------------------------- Main menu loop ------------------------------- #
while True:
    try:
        menu = int(input(
            """To search by keyword choose 1, 
To search by year of production choose 2, 
To search by genre choose 3, 
If you want to see statistics choose 4 
For exit choose 5
> """
        ))
        if menu not in [1, 2, 3, 4, 5]:
            print("Please enter a number between 1 and 5.")
            continue
    except ValueError:
        print("Invalid input. Please enter only numbers 1 to 5.")
        continue

    match menu:
        # ------------------------------- Case 1: search by keyword ------------------------------- #
        case 1:
            while True:
                offset = 0
                key_word = input("Enter keyword (or press Enter to return to main menu): ").strip()
                if key_word == "":
                    break

                result = sql_connector.find_by_key_word(key_word, offset) or []
                log_writer.log_query("keyword", {"key_word": key_word}, len(result))

                if not result:
                    print("No films found with your keyword.")
                    continue

                formatter.print_table_results(
                    [(title or '', desc or '', year or '') for _, title, desc, year in result],
                    ["Title", "Description", "Release Year"],
                    "No films found with your keyword.",
                    start_index=offset + 1
                )

                if len(result) < 10:
                    continue

                while True:
                    more = input("Show more results? (y/n): ").lower().strip()
                    if more == "y":
                        offset += 10
                        result = sql_connector.find_by_key_word(key_word, offset) or []
                        log_writer.log_query("keyword", {"key_word": key_word}, len(result))

                        if result:
                            formatter.print_table_results(
                                [(title or '', desc or '', year or '') for _, title, desc, year in result],
                                ["Title", "Description", "Release Year"],
                                "No films found with your keyword.",
                                start_index=offset + 1
                            )
                            if len(result) < 10:
                                print("No more results.")
                                break
                        else:
                            print("No more results.")
                            break
                    elif more == "n":
                        break
                    else:
                        print("Please enter only 'y' or 'n'.")

            print("\tMain menu choose one option")

        # ------------------------------- Case 2: search by year or interval ------------------------------- #
        case 2:
            while True:
                try:
                    menu_case_2 = int(input(
                        """To search by one year choose 1, 
To search by interval choose 2, 
For exit to main menu choose 3
> """
                    ))
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
                        year_input = input(
                            f"Enter a year ({min_year}-{max_year}, or press Enter to return): "
                        ).strip()
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
                        first_year_input = input(
                            f"Enter first year ({min_year}-{max_year}, or press Enter to return): "
                        ).strip()
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

                        second_year_input = input(
                            f"Enter second year ({min_year}-{max_year}, or press Enter to return): "
                        ).strip()
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
                                ok, data = sql_connector.get_films_by_years_interval(
                                    first_year, second_year, offset
                                )
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

                elif menu_case_2 == 3:
                    break

            print("\tMain menu choose one option")

        # ------------------------------- Case 3: search by genre ------------------------------- #
        case 3:
            genres = sql_connector.get_genres() or []
            if not genres:
                print("No genres found in the database.")
                break

            print("Available genres:")
            for genre_id, name in genres:
                print(f"{genre_id}: {name}")

            while True:
                genre_input = input("Enter the genre ID (or press Enter to return): ").strip()
                if genre_input == "":
                    break

                try:
                    genre_id = int(genre_input)
                except ValueError:
                    print("Invalid input. Please enter only numbers.")
                    continue

                valid_ids = [g[0] for g in genres]
                if genre_id not in valid_ids:
                    print(f"Please enter a number between {min(valid_ids)} and {max(valid_ids)}.")
                    continue

                offset = 0
                ok, films = sql_connector.find_films_by_genres(genre_id, offset)
                films = films or []
                log_writer.log_query("genre", {"genre_id": genre_id}, len(films) if ok else 0)

                if not ok or not films:
                    print("No results found for the selected genre.")
                    continue

                formatter.print_table_results(
                    [(title or '', desc or '', year or '') for title, desc, year in films],
                    ["Title", "Description", "Release Year"],
                    "No films found for this genre.",
                    start_index=offset + 1
                )

                while True:
                    if len(films) < 10:
                        print("No more results.")
                        genres = sql_connector.get_genres() or []
                        for genre_id, name in genres:
                            print(f"{genre_id}: {name}")
                        break

                    more = input("Show more results? (y/n): ").lower().strip()
                    if more not in ("y", "n"):
                        print("Please enter only 'y' or 'n'.")
                        continue

                    if more == "y":
                        offset += 10
                        ok, films = sql_connector.find_films_by_genres(genre_id, offset)
                        films = films or []
                        log_writer.log_query("genre", {"genre_id": genre_id}, len(films) if ok else 0)

                        if not ok or not films:
                            print("No more results.")
                            genres = sql_connector.get_genres() or []
                            for genre_id, name in genres:
                                print(f"{genre_id}: {name}")
                            break

                        formatter.print_table_results(
                            [(title or '', desc or '', year or '') for title, desc, year in films],
                            ["Title", "Description", "Release Year"],
                            "No films found for this genre.",
                            start_index=offset + 1
                        )
                    else:
                        genres = sql_connector.get_genres() or []
                        for genre_id, name in genres:
                            print(f"{genre_id}: {name}")
                        break

            print("\tMain menu choose one option")

        # ------------------------------- Case 4: statistics ------------------------------- #
        case 4:
            while True:
                try:
                    menu_case_4 = int(input(
                        """To find top 5 queries by keyword choose 1, 
To find top 5 queries by year of production choose 2, 
To find top 5 queries by interval years of production choose 3, 
To find top 5 queries by genres choose 4, 
For exit choose 5
> """
                    ))
                    if menu_case_4 not in [1, 2, 3, 4, 5]:
                        print("Please enter a number between 1 and 5.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter only numbers 1 to 5.")
                    continue

                if menu_case_4 == 5:
                    break

                if menu_case_4 == 1:
                    stats = log_stats.search_frequency_key_word() or []
                    stat_type = 'keyword'
                elif menu_case_4 == 2:
                    stats = log_stats.search_frequency_year() or []
                    stat_type = 'year'
                elif menu_case_4 == 3:
                    stats = log_stats.search_frequency_interval() or []
                    stat_type = 'interval'
                elif menu_case_4 == 4:
                    stats = log_stats.search_frequency_genre() or []
                    stat_type = 'genre'
                else:
                    continue

                if not stats:
                    print("No statistics found.")
                    continue

                formatter.print_statistic_results(stats, stat_type)

            print("\tMain menu choose one option")

        # ------------------------------- Exit ------------------------------- #
        case 5:
            log_writer.close_mongo()
            print("Connections closed. Goodbye!")
            break
