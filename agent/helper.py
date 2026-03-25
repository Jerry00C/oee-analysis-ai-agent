def print_result(result, headers=None):
    """
    Pretty-print a list of tuples (SQL query result) in a table format to the terminal.

    Args:
        result (list[tuple]): Query result, each tuple is a row.
        headers (list[str], optional): List of column names to print as header. If None, header is omitted.
    """
    if not result and not headers:
        print("(No results)")
        return

    # Determine number of columns
    if headers:
        ncols = len(headers)
    elif result and len(result) > 0:
        ncols = len(result[0])
    else:
        ncols = 0

    # Prepare columns to calculate width
    col_widths = [0] * ncols
    rows = []
    if headers:
        for i, h in enumerate(headers):
            col_widths[i] = max(col_widths[i], len(str(h)))
    for row in result:
        srow = []
        for i, cell in enumerate(row):
            scell = str(cell)
            srow.append(scell)
            col_widths[i] = max(col_widths[i], len(scell))
        rows.append(srow)
    # Print header
    if headers:
        header_row = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
        print(header_row)
        print("-+-".join("-" * col_widths[i] for i in range(ncols)))
    # Print rows
    for srow in rows:
        print(" | ".join(srow[i].ljust(col_widths[i]) for i in range(ncols)))