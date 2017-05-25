opensauce-python
================

This is a Python port of
[VoiceSauce](http://www.seas.ucla.edu/spapl/voicesauce/) (written in MATLAB) /
[OpenSauce](https://github.com/voicesauce/opensauce) (written in GNU Octave).
It provides a set of command-line tools for taking automatic voice measurements
from audio recordings.

# Requirements

* Python 2.7
* Python packages [NumPy](http://www.numpy.org/) and [SciPy](http://www.scipy.org/)

If you want to use Snack to estimate parameters:
* Tcl/Tk 8.4+ (needed to run Snack Sound Toolkit)
* [Snack Sound Toolkit](http://www.speech.kth.se/snack/)

# Installation

1.  Install Python, the Pythons package NumPy and SciPy, and Snack Sound
    Toolkit, if you don't already have them. Installing Snack is non-trivial,
    so we recommend that you follow the recommendations in the instructions
    below for this step.

    * [Windows specific instructions](WINDOWS.md)
    * [Mac OS X specific instructions](MAC-OS-X.md)
    * [Linux specific instructions](LINUX.md)

2.  Install Git, if you don't have it on your machine.  See the official Git
    website for [recommendations on how to install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

3.  Finally, navigate to the directory where you want to download opensauce and
    clone this repository using Git.

        $ git clone https://github.com/voicesauce/opensauce-python.git

4.  To get updates to the software, use the `git pull` command inside the
    `opensauce-python` directory.

        $ git pull

# Quickstart

(Note that these are interim instructions. Eventually there will be an
'opensauce' command.)

To run OpenSauce, open a new terminal window, `cd` into the directory where you
cloned `opensauce-python`:

    $ cd /path/to/opensauce-python

You can view the command help by typing:

    $ python -m opensauce --help

or alternatively:

    $ python -m opensauce --h

Here's an example of how to use the command line interface.  To process a sound
file and get the snackF0 and SHR measurements written to a CSV file, do:

    $ python -m opensauce --measurements snackF0 SHR -o out.csv /path/to/file.wav

Or alternatively, you can put file path to the sound file first.

    $ python -m opensauce /path/to/file.wav --measurements snackF0 SHR -o out.csv

The CSV format used is Excel tab delimited.

You can process multiple wav files by using shell wildcards.  Suppose
your wav files are in the directory `data/sample1`.  You can process
all of them by typing:

    $ python -m opensauce --measurements snackF0 SHR -o out.csv data/sample1/*.wav

If you want to write the output to stdout (that is, displayed on the terminal)
instead of writing to a file, leave off the `-o` optional argument.  For
example, this command writes the snackF0 and SHR measurements to stdout and
does not use TextGrid information.

    $ python -m opensauce --measurements snackF0 SHR --no-textgrid /path/to/file.wav

Currently only the snackF0, shrF0, and SHR measurements are supported. (Again,
you can run `$ python -m opensauce --help` to see which measurements are
available.)

The command line interface has default values for all the different options.
To see the default values, run the help command: `python -m opensauce -h`.

If you want to use TextGrid files in your analysis, make sure that each sound
file you analyze `name.wav`, has a corresponding TextGrid file with the same
base filename followed by the `.TextGrid` extension, e.g. `name.TextGrid`.
Capitalization is important, so `name.TextGrid` will be found, but
`name.textgrid` will not.

Note there is one subtlety with using the command line interface.  You cannot
specify the sound files right after the `--measurements` option.

A command, such as,

    $ python -m opensauce --measurements SHR /path/to/file.wav

would fail to be parsed correctly because the path of the sound file is
interpreted as a measurement.  Either make sure that there is another option
specified after measurements,

    $ python -m opensauce --measurements SHR --no-labels /path/to/file.wav

or specify the sound file at the beginning.

    $ python -m opensauce /path/to/file.wav --measurements SHR

# Settings and measurement files

If it is inconvenient to enter options on the command line, you can also do
this via a settings and/or measurements file.

Any options you can specify on the command line you can put into a settings
file, one option and its arguments per line.  On the command line, you can
specify a settings file to use, with a command like

    $ python -m opensauce -s my_settings /path/to/file.wav

or alternatively,

    $ python -m opensauce --settings my_settings /path/to/file.wav

To run your favorite settings by default, you can copy your settings file to
one of the locations `./opensauce.settings`, `~/.config/opensauce/settings`,
or `~/.opensaucerc`.  Opensauce will automatically search each of these
locations, in the above order, for a default settings file, if no settings file
is explicitly specified on the command line.  The first file found will be
used.

An example settings file is included in this repository, called
`opensauce.settings.example`.  You can copy this file to `opensauce.settings`
to see how the settings file works.  Run OpenSauce on a sound file with no
settings file specified, like this:

    $ python -m opensauce /path/to/file.wav

You can also have a measurements file containing one measurement per line.  On
the command line, you can specify a measurements file to use, with a command
like

    $ python -m opensauce -m my_measurements /path/to/file.wav

To run your favorite settings by default, you can copy your measurements file
to one of the locations `./opensauce.measurements`,
`~/.config/opensauce/measurements`, or `~/.opensauce.measurements`.  Opensauce
will automatically search each of these locations, in the above order, for a
default settings file, if no settings file is explicitly specified on the
command line.  The first file found will be used.

An example settings file is included in this repository, called
`opensauce.measurements.example`.  You can copy this file to
`opensauce.measurements` to see how the measurements file works.  Run OpenSauce
on a sound file with no measurements file specified, like this:

    $ python -m opensauce /path/to/file.wav

Note that if you specify measurements in both the settings and measurements
files, the measurements in the settings file will override those in the
measurements file.  Similarly, options and measurements specified on the
command line override those specified in a settings or measurements file.

# Contributing

See [HACKING](HACKING.md).

# Resources

* Documentation: someday
* [OpenSauce](https://github.com/voicesauce/opensauce)
* [VoiceSauce](http://www.seas.ucla.edu/spapl/voicesauce/)

# Questions

Please feel free to post a question on the Issue tracker (use the label
'question').
