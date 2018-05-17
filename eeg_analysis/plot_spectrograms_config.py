from spectrograms.classes import Options
from spectrograms.logic import main
# fix xticks on spectrogram

ops = Options(pds_folder=r'D:\SERT_DREADD\dfs\pds',
              recordings_to_plot=[
                  '371a_2018-04-11_17-09-39_NO_CNO',
                  '371a_2018-04-11_17-48-20_NO_CNO_2',
                  '371a_2018-04-11_18-15-03_CNO',
                  '401a_2018-04-18_16-34-20_NO_CNO',
                  '401a_2018-04-18_17-40-36_CNO',
                  '401b_2018-04-16_14-25-14_NO_CNO',
                  '401b_2018-04-16_15-26-37_CNO',
                  '401c_2018-04-17_13-35-07_NO_CNO',
                  '401c_2018-04-17_14-38-53_CNO',
                  'unknown_2018-04-12_14-00-40_NO_CNO',
                  'unknown_2018-04-12_15-01-27_CNO'
              ],
              fig_out_folder=r'D:\SERT_DREADD\figures',
              operating_system='win',
              which='both',
              dpi=300,
              vmin=0,
              vmax=12,
              verbose=True)

if __name__ == '__main__':
    main(ops)
