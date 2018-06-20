class Options:

    def __init__(self, csv_dir, csv_file_name, resample_period, rolling_periods,
                 normalisation_method, category_column, vmin, vmax, out_folder):
        self.csv_dir = csv_dir
        self.csv_file_name = csv_file_name
        self.resample_period = resample_period
        self.rolling_periods = rolling_periods
        self.normalisation_method = normalisation_method
        self.category_column = category_column
        self.vmin = vmin
        self.vmax = vmax
        self.out_folder = out_folder
