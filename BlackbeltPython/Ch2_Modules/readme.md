# Python modules


## import
The `import` keyword imports a module. It actually just invokes a builtin function `__import__`, which
can also be called directly.


## sys module
- Details about the python installation and the system it's running on.
- sys.modules - lists all modules imported in the session.
- sys.path - import search paths.


## Useful standard libraries
* `atexit` allows you to register functions for your program to call when it exits.
* `argparse` provides functions for parsing command line arguments.
* `bisect` provides bisection algorithms for sorting lists.
* `calendar` provides a number of date­related functions.
* `codecs` provides functions for encoding and decoding data.
* `collections` provides a variety of useful data structures.
* `copy` provides functions for copying data.
* `csv` provides functions for reading and writing CSV files.
* `datetime` provides classes for handling dates and times.
* `fnmatch` provides functions for matching Unix­style filename patterns.
* `concurrent` provides asynchronous computation (native in Python 3, available for 2 via PyPI).
* `glob` provides functions for matching Unix­style path patterns.
* `io` provides functions for handling I/O streams. In Python 3, it also contains StringIO
   (inside the module of the same name in Python 2), which allows you to treat strings as files.
* `json` provides functions for reading and writing data in JSON format.
* `logging` provides access to Python’s own built­in logging functionality.
* `multiprocessing` allows you to run multiple subprocesses from your application, while
   providing an API that makes them look like threads.
* `operator` provides functions implementing the basic Python operators, which you can
   use instead of having to write your own lambda expressions.
* `os` provides access to basic OS functions.
* `random` provides functions for generating pseudorandom numbers.
* `re` provides regular expression functionality.
* `sched` provides an event scheduler without using multithreading.
* `select` provides access to the select() and poll() functions for creating event loops.
* `shutil` provides access to high­level file functions.
* `signal` provides functions for handling POSIX signals.
* `tempfile` provides functions for creating temporary files and directories.
* `threading` provides access to high­level threading functionality.
* `urllib` (and urllib2 and urlparse in Python 2.x) provides functions for handling and parsing URLs.
* `uuid` allows you to generate Universally Unique Identifiers (UUIDs).


# pip
* development code can be installed without actually copying any code
  by executing
  `pip install -e .`
  This will install the current working directory module, by creating
  a reference in the python site-packages.
* The same command can be used to install from a url or directly
  from a git repository:
  `pip install -e git+https://github.com/jd/daiquiri.git\#egg=daiquiri`
  Note that the `egg=some_name` must be given after the url, to name the package.
