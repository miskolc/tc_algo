class ApiKey:
    daily = 'daily'
    weekly = "weekly"
    monthly = 'monthly'
    quarterly = 'quaterly'
    annual = 'annual'
    quandl_intervals = [daily, weekly, monthly, quarterly, annual]

    row_diff = 'diff'
    row_perc_change = 'rdiff'
    latest_value_perc_increment = 'rdiff_from'
    cumulative_sum = 'cmul'
    normalize = 'normalize'
    quandl_transform = [row_diff, row_perc_change, latest_value_perc_increment, cumulative_sum, normalize]


class ExitCode:
    max_attempts = 21
    api_error = 22
    token_error = 23
    symbol_not_found = 24
