def create_table(row_data):
    if not row_data or not all(isinstance(row, (list, tuple)) for row in row_data):
        return "Invalid input: row_data should be a non-empty list of lists or tuples."

    # Extract column headers
    header = [str(i) for i in range(len(row_data[0]))]

    # Determine column widths
    col_widths = [max(len(header[i]), max(len(str(row[i])) for row in row_data)) + 2 for i in range(len(header))]

    # Build the table
    table = "+{}+".format("+".join("-" * width for width in col_widths))
    lines = ["| {} |".format(" | ".join(str(row[i]).ljust(col_widths[i] - 1) for i in range(len(header)))) for row in row_data]

    # Combine everything into the final table
    return "{}\n{}\n{}".format(table, "\n".join([table] + lines + [table]), table)
