import sql_connector
import formatter
import log_writer

def run_case3():
    print("\tSearching by geners menu")
    genres = sql_connector.get_genres() or []
    if not genres:
        print("No genres found in the database.")
        return

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
