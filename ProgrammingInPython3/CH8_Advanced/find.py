#! python3
import os

def coroutine(function):
    def wrapper(*args, **kwargs):
        generator = function(*args, **kwargs)
        next(generator)
        return generator
    wrapper.__name__ = function.__name__
    wrapper.__doc__  = function.__doc__
    return wrapper


@coroutine
def reporter(output):
    while True:
        filename, stat = (yield)
        result = []
        if output:
            if 'date' in output:
                result.append(datetime.datetime.fromtimestamp(
                    stat.st_mtime).isoformat(' '))
            if 'size' in output:
                result.append('{0:12,}'.format(stat.st_size))
        result.append(filename)
        print(' '.join(result))


@coroutine
def get_files(receiver):
    while True:
        path = (yield)
        if os.path.isfile(path):
            abs_path = os.path.abspath(path)
            receiver.send((abs_path, os.stat(abs_path)))
        else:
            for root, dirs, files in os.walk(path):
                for file in files:
                    abs_path = os.path.abspath(os.path.join(root, file))
                    receiver.send((abs_path, os.stat(abs_path)))


@coroutine
def suffix_matcher(receiver, suffixes):
    while True:
        filename, stat = (yield)
        if filename.endswith(suffixes):
            receiver.send((filename, stat))


@coroutine
def size_matcher(receiver, minimum=None, maximum=None):
    while True:
        filename, stat = (yield)
        size = stat.st_size
        if((minimum is None or size >= minimum) and
           (maximum is None or size <= maximum)):
            receiver.send((filename, stat))


@coroutine
def date_matcher(receiver, date):
    while True:
        filename, stat = (yield)
        if stat.st_mtime >= date:
            receiver.send((filename, stat))


if __name__ == '__main__':
    import sys
    from optparse import OptionParser
    import datetime
    import time

    def get_bytes(s):
        suf = s[-1]
        if suf in 'kK':
            return 1024 * int(s[:-1])
        if suf in 'mM':
            return 1024 ** 2 * int(s[:-1])
        else:
            return int(s)


    oparser = OptionParser()
    oparser.add_option('-d', '--days', action='store', dest='modified', type=int,
            help='show only files not older than the specified number of days'
                 '[default: show all files]', metavar='DAYS', default=None)
    oparser.add_option('-b', '--bigger', action='store', dest='minimum',
            help='show only files bigger than the specified number of bytes',
            default=None)
    oparser.add_option('-s', '--smaller', action='store', dest='maximum',
            help='show only files smaller than the specified number of bytes',
            default=None)
    oparser.add_option('-o', '--output', action='store', dest='output',
            help='Additional file information to output. Valid options: size, date.'
                 'Filenames are output always.', metavar='what', default=None)
    oparser.add_option('-u', '--suffix', action='store', dest='suffixes',
            help='show only files with the specified suffix(es).')

    opt, args = oparser.parse_args()
    if len(args) == 0:
        oparser.error("No files of paths have been specified")
    if opt.minimum is not None:
        opt.minimum = get_bytes(opt.minimum)
    if opt.maximum is not None:
        opt.maximum = get_bytes(opt.maximum)
    if(opt.minimum and opt.maximum and opt.minimum > opt.maximum):
        oparser.error('cannot find files bigger than {0} and smaller than {1}'.format(
                    opt.minimum, opt.maximum))
    if opt.modified:
        delta = datetime.timedelta(days=opt.modified)
        days = datetime.datetime.today() - delta
        opt.modified = time.mktime(days.timetuple())

    print(opt)
    print(args)

    pipes = []
    pipes.append(reporter(opt.output))
    if opt.minimum or opt.maximum:
        pipes.append(size_matcher(pipes[-1], minimum=opt.minimum,
                                            maximum=opt.maximum))
    if opt.suffixes:
        pipes.append(suffix_matcher(pipes[-1], opt.suffixes))
    if opt.modified:
        pipes.append(date_matcher(pipes[-1], opt.modified))
    pipes.append(get_files(pipes[-1]))
    pipeline = pipes[-1]
    try:
        for path in args:
            print(path)
            pipeline.send(path)
    finally:
        for pipe in pipes:
            pipe.close()

