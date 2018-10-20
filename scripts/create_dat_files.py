import argparse
import sys
import os
sys.path.append('/home/ruairi/repos')  # path to parent folder to ephys

from ephys.package._classes.options import options_from_args
from preprocess import pack_2


def get_options():
  parser = argparse.ArgumentParser(
      description='''Packs concurrently recorded continuous
                    files to one flat binary .dat file.''')
  parser.add_argument('-c', '--config_file', required=True,
                      help='path to options configuration [.json] file')
  parser.add_argument('-r', '--recordings', required=True,
                      help='''recordings to pack. give a single recording
                        or a comma-separated list of recordings (no spaces)''')
  parser.add_argument('-f', '--reference_method',
                      help='''reference method desired. defaults to "ave"
                         for common average reference''', default='ave')

  args = parser.parse_args()
  ops = options_from_args(args)
  return ops


def pack_recordings(ops):
  for recording in ops.recordings:
    if not os.path.exists(os.path.join(ops.parent_dir, 'dat_files', recording)):
      os.mkdir(os.path.join(ops.parent_dir,
                            'dat_files', recording))
    pack_2(folderpath=os.path.join(ops.continuous_dir, recording),
           filename=os.path.join(
               ops.parent_dir, 'dat_files', recording, recording) + '.dat',
           channels=ops.chan_map,
           chprefix='CH',
           dref=ops.reference_method,
           session='0',
           source='100')


if __name__ == '__main__':
  ops = get_options()
  pack_recordings(ops)
