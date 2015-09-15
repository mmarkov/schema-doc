from optparse import OptionParser
import os
from pkg_resources import resource_filename
import sys
import shutil
import sqlalchemy
from schemadoc.version import  __version__
from schemadoc.doc_generator import DocGenerator
import traceback

def _doc(url, folder):
    engine = sqlalchemy.create_engine(url)
    # copy lib into target folder
    lib_folder = os.path.join(resource_filename(__name__, 'static'), 'lib')
    output_lib_folder = os.path.join(folder, 'lib')
    shutil.copytree(src=lib_folder, dst=output_lib_folder)
    generator = DocGenerator(engine, folder)
    generator.generate_documentation()


def main():

    """
    Entry point which parse parameters and run generation routine

    :return: exit_code which will be passed to OS
    """
    argv = sys.argv[1:]

    option_connection_url = 'connection_url'
    option_folder = 'folder'

    parser = OptionParser(usage="usage: %prog [options]",
                          version="schemadoc v%s" % (__version__,))
    parser.add_option('-u', help='SQLAlchemy connection url (required)',
                      dest=option_connection_url, action='store')
    parser.add_option('-o', help='Output folder (required)',
                      dest=option_folder, action='store')

    opts, args = parser.parse_args(argv)
    if not argv or len(argv) == 0:
        parser.print_help()
        return 1

    if not opts.folder:
        print('parameter -o folder is required', file=os.sys.stdout)
        parser.print_help()
        return 1

    if not opts.connection_url:
        print('parameter -u connection is required', file=os.sys.stdout)
        parser.print_help()
        return 1

    folder = opts.folder.strip()
    url = opts.connection_url.strip()
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        elif len(os.listdir(folder)) != 0:
            print('Folder %s is not empty' % folder)
            return 1

    except OSError as e:
        print(repr(e), file=os.sys.stdout)
        print('Can not create folder %s' % folder, file=os.sys.stdout)
        return 1

    try:
        print("Generating documentation for %s \nOutput folder is %s" % (url, folder,), file=os.sys.stdout)
        _doc(url, folder)
    except Exception as e:
        print(repr(e), file=os.sys.stdout)
        traceback.print_last()
        return 1

    print("Documentation is generated in folder %s" % (folder,), file=os.sys.stdout)
    return 0

if __name__ == "__main__":
    exit_code = main()
    os.sys.exit(exit_code)