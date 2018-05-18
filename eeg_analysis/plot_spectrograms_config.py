from spectrograms.classes import Options
from spectrograms.logic import main
# fix xticks on spectrogram

ops = Options(pds_folder=r'D:\CIT_WAY\dfs\pds',
              recordings_to_plot=[
                  'CIT_WAY_02_2018-05-03_13-38-41_PRE'
              ],
              fig_out_folder=r'D:\CIT_WAY\figures',
              operating_system='win',
              which='both',
              dpi=300,
              vmin=0,
              vmax=12,
              verbose=True)

if __name__ == '__main__':
  main(ops)
