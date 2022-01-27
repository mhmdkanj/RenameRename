import argparse
import os
from glob import glob
from renamerename.handlers.handlers import FileListHandler
from renamerename.executor.executor import RenameExecutor


def parse_args():
    parser = argparse.ArgumentParser(description='Bulk renaming of files made easy.', usage="%(prog)s dir [options]")
    parser.add_argument("directory", type=str, help="directory whose filenames are processed", metavar="dir")
    parser.add_argument("--only-output-results", "-o", action="store_true", help="only show renaming results without execution", required=False)
    parser.add_argument("--filter", "-f", type=str, help="filter the directory contents according to a Python regex", required=False, default=None)
    parser.add_argument("--prefix", "-p", type=str, help="add a prefix to filtered filenames", required=False, default=None)
    parser.add_argument("--suffix", "-s", type=str, help="add a suffix to filtered filenames", required=False, default=None)
    parser.add_argument("--change-extension", "-e", type=str, help="change the filtered filenames' extensions", required=False, default=None)
    parser.add_argument("--add-numbering", "-n", type=str, help="change filtered filenames to same name suffixed with increasing numbers", required=False, default=None)
    parser.add_argument("--version", action="version", version="%(prog)s 0.0.1")
    return parser.parse_args()

def run(args=None):
    if not args:
        args = parse_args()
    
    assert os.path.isdir(args.directory), "Given directory is not a valid directory."

    # Get all (non-hidden) files in a directory
    names = [name for name in glob("*", root_dir=args.directory) if os.path.isfile(os.path.join(args.directory, name))]
    
    file_list_handler = FileListHandler(names)
    file_list_handler.filter_names(filter=args.filter)

    if args.prefix:
        file_list_handler.add_prefix(args.prefix)   
    if args.suffix:
        file_list_handler.add_suffix(args.suffix)
    if args.change_extension:
        file_list_handler.change_extension(args.change_extensions)
    if args.add_numbering:
        file_list_handler.add_numbering(args.add_numbering)

    executor = RenameExecutor(args.directory)
    
    if args.only_output_results:
        executor.display_output(file_list_handler.names, file_list_handler.filetransformations)
    else:
        executor.execute(file_list_handler.names, file_list_handler.filetransformations)
