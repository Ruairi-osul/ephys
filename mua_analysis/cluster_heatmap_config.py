from cluster_heatmap.logic import main
from cluster_heatmap.classes import Options


ops = Options(csv_dir=r'E:\SERT_DREADD\csvs',
              csv_file_name='all_neurons_ts_with_clusters',
              out_folder=r'E:\SERT_DREADD\figures\cluster_heat_maps',
              resample_period='120sec',
              category_column='category',
              rolling_periods=240,
              normalisation_method='percent',
              vmin=0,
              vmax=200)

if __name__ == '__main__':
    main(ops)
