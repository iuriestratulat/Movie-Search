import sql_connector
import formatter
import log_writer

def run_case1():
    print ("\tKey word searching menu")
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
