import os


def mkdir(ops, dirname):
    path = os.path.join(ops.parent_dir, dirname)
    if not os.path.exists(path):
        os.mkdir(path)
    setattr(ops, '_'.join([dirname, 'dir']), path)
    ops.dirname = path
