import formatter
import log_stats

def run_case4():
    print("\tStatistics menu")
    while True:
        try:
            menu_case_4 = int(input("""To find top 5 queries by keyword choose 1, 
To find top 5 queries by year of production choose 2, 
To find top 5 queries by interval years of production choose 3, 
To find top 5 queries by genres choose 4, 
For exit choose 5
> """))
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
