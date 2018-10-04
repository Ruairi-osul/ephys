import argparse
import os
from collections import namedtuple


def _get_options():
    '''Specifies command line arguments

    call:
        'python py_kilosort.py -h'

    for details...
    '''
    parser = argparse.ArgumentParser(
        description='''Call kilosort from python ;)

    Given a path to a .dat file, updates kilosort config files
    and calls it as subprocess
    ''')

    parser.add_argument('-r', '--recording', required=True,
                        help='''Path to .dat file to be spike sorted
                        ''')
    parser.add_argument('-m', '--master', required=True,
                        help='''Path to kilosort master.m script
                        ''')
    parser.add_argument('-c', '--config', required=True,
                        help='''Path to kilosort sandard_cofig.m script
                        ''')
    return parser.parse_args()


def update_kilosort_config(recording, config, tempfile, root):
    '''Updates kilosort Standard config file.
    New file saved as temp.m in current working direcory [maybe change this?]


    Arguments:
        recording: path to .dat file to do
        config: path to StandardConfig.m
        tempfile: path to temperary file created during kilosort spike sorting
        root: parent directory of .dat file to do
    '''

    def _get_line_indexes(config):
        settings = ['ops.fbinary', 'ops.fproc', 'ops.root']
        temp = []
        with open(config, 'r') as file:
            lines = file.readlines()
            for setting in settings:
                line = list(filter(lambda x: x.startswith(setting), lines))[0]
                temp.append(lines.index(line))

        WordsToUpdate = namedtuple('WordsToUpdate',
                                   ['dat_file_index', 'temp_file_index',
                                    'root_dir_index'])

        return WordsToUpdate(dat_file_index=temp[0], temp_file_index=temp[1],
                             root_dir_index=temp[2])

    def _update_config_file(fields, config, recording, temp, root):

        def _replace(new_word, line):
            return ' '.join([''.join(['\'', new_word, '\'']) if i == 2 else word
                             for i, word in enumerate(line.split())])  # 3rd word

        tmp_m = os.path.join(os.path.dirname(
            config), 'temp.m')  # !!change to param
        with open(config, 'r') as fread, open(tmp_m, 'w') as fwrite:
            for line_index, line in enumerate(fread.readlines()):
                if line_index == fields.dat_file_index:
                    line = '\n' + _replace(recording, line) + ';'
                elif line_index == fields.temp_file_index:
                    line = '\n' + _replace(tempfile, line) + ';'
                elif line_index == fields.root_dir_index:
                    line = '\n' + _replace(root, line) + ';'

                fwrite.write(line)
        os.chmod(tmp_m, 0o755)
        return

    fields = _get_line_indexes(config)
    _update_config_file(fields, config, recording, tempfile, root)


def call_kilosort(path_to_master):
    '''Use os module to call kilosort from the command line (as a subprocess)

    Parameters:
        path_to_master: path to master.m kilosort file
    '''
    call_string = '''matlab -nodisplay -nosplash -nodesktop -r \"run(\'{}\');exit;\"'''.format(
        path_to_master)

    print('Calling:\n\n{}\n\n'.format(call_string))
    os.system(call_string)


def main(recording, master, config, tempfile=None, root=None):
    '''Call kilosort from python ;)
    Given a path to a .dat file, updates kilosort config files
    and calls it as subprocess


    Parameters:
        recording: path to .dat file to do
        master: path to master.m matlab script
        config: path to StandardConfig.m script
        [tempfile: specify path to temp files created during kilosort]
        [root: specify root directory of files created during kilosort]
    '''
    if not tempfile:
        tempfile = os.path.join(os.path.dirname(recording), 'temp_wh.dat')
    if not root:
        root = os.path.dirname(recording)

    update_kilosort_config(recording, config, tempfile, root)
    call_kilosort(master)


if __name__ == '__main__':
    args = _get_options()
    main(args.recording, args.master, args.config)
