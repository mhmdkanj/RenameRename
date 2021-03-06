# RenameRename

![docs](https://github.com/mhmdkanj/RenameRename/actions/workflows/docs.yml/badge.svg?branch=main)
![test](https://github.com/mhmdkanj/RenameRename/actions/workflows/test.yml/badge.svg?branch=main)
[![codecov](https://codecov.io/gh/mhmdkanj/RenameRename/branch/main/graph/badge.svg?token=VYS7K7KRVB)](https://codecov.io/gh/mhmdkanj/RenameRename)

**RenameRename** is a command-line utility app that bulk renames a set of files based on some specifications.
What's special about this tool, among so many other similar ones, is that it's straightforward to use.

If you don't feel like dealing with complex regex's and just want the job done without any learning effort,
then hopefully RenameRename can cater to your bulk renaming needs. 😄

The main usage of RenameRename is as a CLI tool.
Nevertheless, it can also be used as a package of modules containing utility classes and functions for your own modules.

Feel free to take a look at the [API reference / documentation](https://mhmdkanj.github.io/RenameRename/html/index.html).

## Requirements

To run the CLI tool, you primarily need the following installed on your system:
- [Python 3.6+](https://www.python.org/)

## Install

To install the package, you can do so with [pip](https://pypi.org/project/pip/).

```sh
pip install renamerename
```

Otherwise, if you want to install from source, just clone the repository in the directory of your choice,
and then install it with `pip`, as such:

```sh
git clone https://github.com/mhmdkanj/RenameRename.git
pip install -e RenameRename
```

## Usage

In order to use RenameRename, run the Python package with:
```sh
renamerename [options]
```

### Filtering

By default, RenameRename searches for files in the current working directory.
Otherwise, a different one can be set using the `--dir` option.

Filtering of files is done via Unix filename patterns supplied with the `--filter`, such as:

|  Pattern  |  Usage  |  Example  |
|  -------  |  ------ |  -------  |
|  *None*   |  exact characters  |  `file` -> `file` |
|  `*`      |  any number of characters |  `img*` -> `img_foo.tar.gz`, `img123.png`, `img`, etc.  |
|  `?`      |  any single character  | `doc?file` -> `doc_file`, `doc1file`, `docsfile`, etc.  |
|  `[seq]`  |  any character in *seq*  |  `file_[abcdef].txt` -> `file_a.txt`, `file_b.txt`, etc.  |
|  `[!seq]` |  any character not in *seq*  |  `file_[!abc].txt` -> `file_d.txt`, `file_1.txt`, `file__.txt`, etc.  |

You can check which files are filtered out by providing the filter option without any actions.
```sh
renamerename --filter "img_*"
# OUTPUT: filter all files beginning with: img_
```

**NOTES**:
- It is necessary to enclose filter arguments with double quotation marks `" "`, as this would allow you to pass the literal filter expression to the command (otherwise, the shell would process it, resolve the filenames itself, and pass invalid arguments to the command).
- RenameRename acts on non-hidden files inside a directory. Also, the file search is non-recursive and does not take into account directory names.

### Basic Actions

Some basic actions to rename filtered files are provided.
The more specific the action, the better.

|  Action   |  Usage   |  Example  |
|  -------  |  ------  | -------   |
|  `--prefix PREFIX`         |  prepends `PREFIX` to the filename  |  `file.txt` -> `PREFIXfile.txt` |
|  `--suffix SUFFIX`         |  appends `SUFFIX` to the filename   |  `file.txt` -> `fileSUFFIX.txt` |
|  `--change-extension .ext` |  changes the file extension         |  `file.txt` -> `file.ext`       |
|  `--add-numbering PREFIX`  |  changes the filename to `PREFIX` and appends a counter  |  `myarchive.tar.gz`, `myfile.txt` -> `PREFIX1.tar.gz`, `PREFIX2.txt`  |

You can of course use multiple actions at the same time.

For instance, if you want to add a prefix, suffix, and change the extension of files beginning with "myfile" and ending with ".png", execute the following:
```sh
renamerename --filter "myfile*.png" --prefix foo_ --suffix _bar --change-extension .jpeg
# Filtered files: myfile_a.png , myfileee.png , myfile_somechars.png
# OUTPUT:
#        myfile_a.png  --->  foo_myfile_a_bar.jpeg
#        myfileee.png  --->  foo_myfileee_bar.jpeg
#        myfile_somechars.png ---> foo_myfile_somechars_bar.jpeg
```

### Only Show Renaming Output without Execution

If you just want to *see* what would happen if some options and actions were supplied without actually renaming your files,
you can do so by supplying the `--only-output-results` or `-o` flag.
This way, you can review if the renaming will be done as intended and without any consequences.

```sh
renamerename [actions] -o
```

### Saving What Was Renamed to What

If you want to save all the source and target filenames for future reference (in case wrong files were renamed),
you can supply the `--save-renaming` flag to do that.

```sh
renamerename [actions] --save-renaming
```

This creates a `JSON` file in the directory supplied with `--dir` (or if no directory was supplied, the current directory) that contains the necessary changes.

### Rename by Loading a JSON file

Renaming can also be done by supplying a JSON file that dictates the source and target filenames needed.
In this case, no filtering is done, but rather the source filenames are manually entered in the JSON file.

The supplied file, via the `--from-json` option, should be a dictionary of source filenames mapped to target filenames. Example:
```json
{
"myfile_a.png": "foo_myfile_a_bar.jpeg",
"myfileee.png": "foo_myfileee_bar.jpeg",
"myfile_somechars.png": "foo_myfile_somechars_bar.jpeg"
}
```

Suppose this file was called `renaming.json`, you can execute the renaming by:
```sh
renamerename --dir DIR --from-json renaming.json
```

### Undo Renaming

In case you did not intend to execute the renaming of files, you can undo this with the `--undo-from-json` option,
in which RenameRename will reverse the renaming.

The renaming can only be undone if in the previous call to RenameRename, you used the `--save-renaming` option.
The JSON file created in that call needs to be supplied to the `--undo-from-json` option.
The mapping is reversed internally.

```sh
renamerename --dir DIR --undo-from-json renaming.json
```

Otherwise, if you do not have the JSON file, you can create one manually and execute RenameRename with the `--from-json` option.

### Synopsis


```
usage: renamerename [options]

Bulk renaming of files made easy.

optional arguments:
  -h, --help            show this help message and exit
  --dir directory       directory whose filenames are processed
  --only-output-results, -o
                        only show renaming results without execution
  --filter FILTER, -f FILTER
                        filter the directory contents according to Unix
                        patterns
  --prefix PREFIX, -p PREFIX
                        add a prefix to filtered filenames
  --suffix SUFFIX, -s SUFFIX
                        add a suffix to filtered filenames
  --change-extension CHANGE_EXTENSION, -e CHANGE_EXTENSION
                        change the extension of the filtered filenames
  --add-numbering ADD_NUMBERING, -n ADD_NUMBERING
                        change filtered filenames to same name suffixed with
                        increasing numbers
  --save-renaming, -sr  create JSON file containing all files renamed
  --from-json JSON file path
                        rename set of files as described from JSON file
  --undo-from-json JSON file path
                        undo renaming of set of files based on saved renaming
                        specification
  --version             show program's version number and exit
```

## Test

The RenameRename Python package includes unit tests for developers who wish to locally test it (especially upon contributing).

For that, you first need to install the testing dependencies via:
```sh
pip install -r requirements-dev.txt
```

The tests can be run with `pytest` and executed via the following:
```sh
cd repository_root   # enter the root directory of the repository
pytest
```

## Documentation

The [documentation](https://mhmdkanj.github.io/RenameRename/html/index.html) (mostly the API reference) to the Python package currently resides on GitHub Pages.

For contributing developers, building the docs locally requires the following:

```sh
pip install -r docs/requirements-docs.txt
apt-get install make
```

You can then build the docs with:

```sh
cd docs   # relative to repository root
make html
```
