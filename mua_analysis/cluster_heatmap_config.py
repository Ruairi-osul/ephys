from cluster_heatmap.logic import main
from cluster_heatmap.classes import Options


ops = Options(csv_dir=r'G:\Rawdata\SERT\csvs',
              csv_file_name='all_neurons_ts_with_clusters',
              out_folder=r'G:\Rawdata\SERT\figures\cluster_heat_maps',
              resample_period='5sec',
              category_column='category',
              rolling_periods=120,
              normalisation_method='zscore',
              vmin=-2.5,
              vmax=2.5)

if __name__ == '__main__':
    main(ops)
