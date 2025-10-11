def print_table_results(results, columns, empty_message, start_index=1):
    """
    Professional table printer with auto column width and artificial numbering.
    
    :param results: list of tuples - data to print
    :param columns: list of str - column headers (excluding numbering column)
    :param empty_message: str - shown if no results
    :param start_index: int - starting number for artificial numbering
    """
    if not results:
        print(empty_message)
        return

    # Add artificial numbering
    numbered_results = [(i, *row) for i, row in enumerate(results, start=start_index)]

    # Add numbering header
    columns_with_num = ["#"] + columns

    # Compute max width for each column
    col_widths = []
    for col_idx, col_name in enumerate(columns_with_num):
        max_data_len = max(len(str(row[col_idx])) for row in numbered_results)
        col_widths.append(max(max_data_len, len(col_name)))

    # Print header
    header = " | ".join(col_name.ljust(col_widths[i]) for i, col_name in enumerate(columns_with_num))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(columns_with_num)))

    print(header)
    print(separator)

    # Print each row
    for row in numbered_results:
        line = " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(columns_with_num)))
        print(line)



def print_statistic_results(results, stat_type):
    """
    Print formatted statistics based on the given stat_type.
    Supported types: 'keyword', 'year', 'genre', 'interval'.
    """
    if not results:
        print("No data found for this statistic.")
        return

    titles = {
        'keyword': "Top 5 keywords by search frequency",
        'year': "Top 5 years by search frequency",
        'genre': "Top 5 genres by search frequency",
        'interval': "Top 5 year intervals by search frequency"
    }

    print(f"\n{titles.get(stat_type, 'Top 5 results')}:")
    print("-" * len(titles.get(stat_type, 'Top 5 results') + ":"))

    for i, entry in enumerate(results, start=1):
        if stat_type == 'keyword':
            print(f"{i}. {entry['word']} — {entry['search_frequency']} searches")
        elif stat_type == 'year':
            print(f"{i}. {entry['year']} — {entry['search_frequency']} searches")
        elif stat_type == 'genre':
            print(f"{i}. {entry['genre_name']} — {entry['search_frequency']} searches")
        elif stat_type == 'interval':
            print(f"{i}. {entry['decade_range']} — {entry['search_frequency']} searches")
        else:
            print(f"{i}. {entry} (unknown statistic type)")
