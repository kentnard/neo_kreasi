def format_amount(amount):
    """
    Formats "amount" column to show no decimals when integer and to show maximum 2 decimals otherwise
    """
    if float(amount).is_integer():
        # If integer, show without decimal
        return f"{int(amount):,}".replace(",", ".")
    else:
        # If real, but not integer, show 2 decimal places
        return f"{amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")