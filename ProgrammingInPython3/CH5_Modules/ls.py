#! python3
import os
import time
from operator import itemgetter

def list_dir(start='.', hidden=False, modified=False, order='n', recur=False, sizes=False):
    dir_list = []
    max_size = 0

    if recur:
        for root, dirs, files in os.walk(start, topdown=True):
            for file in files:
                dir = os.path.join(root, file)
                if hidden or os.path.split(dir)[1][0] != '.':
                    try:
                        dir_list.append((dir, os.path.getmtime(dir), os.path.getsize(dir)))
                        max_size = len(str(dir_list[-1][-1])) if max_size < len(str(dir_list[-1][-1])) else max_size
                    except PermissionError:
                        print("skipping:  {}".format(dir))
    else:
        dirs = os.listdir(start)
        for dir in dirs: #(os.path.join(start, d) for d in dirs):
            if hidden or os.path.split(dir)[1][0] != '.':
                try:
                    dir_list.append((dir, os.path.getmtime(dir), os.path.getsize(dir)))
                    max_size = len(str(dir_list[-1][-1])) if max_size < len(str(dir_list[-1][-1])) else max_size
                except PermissionError:
                    print("skipping:  {}".format(dir))

    print_dirs(dir_list, modified, order, sizes, max_size)


def print_dirs(dirlist, modified=False, order='n', sizes=False, max_size=8):
    template = []
    if modified: template.append('{lastmod} ')
    if sizes:    template.append('{size:>{maxsize}} ')
    template.append('{path}')

    for dir in sorted(dirlist, key=ordering(order)):
        try:
            print(' '.join(template).format(path=dir[0], lastmod=time.ctime(dir[1]), size=dir[2], maxsize=max_size))
        except UnicodeError:
            pass


def ordering(order):
    if order[0] in 'nN':
        return None
    elif order[0] in 'mM':
        return itemgetter(1)
    elif order[0] in 'sS':
        return itemgetter(2)


# =========================================================================== #
if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    oparser = OptionParser()
    oparser.add_option('-H', '--hidden', action='store_true', dest='hidden',
                        help='show hidden filed [default: off]',
                        default=False)
    oparser.add_option('-m', '--modified', action='store_true', dest='modified',
                        help='show last modified date/time [default: off]',
                        default=False)
    oparser.add_option('-o', '--order', action='store', dest='order',
                        help='order by ("name", "n", "modified", "m", "size", "s") [default: name])',
                        metavar='ORDER', default='n')
    oparser.add_option('-r', '--recursive', action='store_true', dest='recur',
                        help='recurse into subdirectories [default: off]',
                        default=False)
    oparser.add_option('-s', '--sizes', action='store_true', dest='sizes',
                        help='show sizes [default: off]',
                        default=False)


    opt, args = oparser.parse_args()
    print(opt)
    print(args)
    for dir in args or '.':
        list_dir(dir, opt.hidden, opt.modified, opt.order, opt.recur, opt.sizes)
