from optparse import OptionParser
import os

from schemaobject.connection import build_database_url
from schemadoc.version import  __version__

def _doc(url, folder):
    raise NotImplementedError()

def main(argv):

    """
    Entry point which parse parameters and run generation routine

    :param argv: list with calling parameters except actual executable path
    :return: exit_code which will be passed to OS
    """
    option_host = 'host'
    default_host = 'localhost'
    option_user = 'user'
    default_user = 'root'
    option_password = 'password'
    default_password = ''
    option_port = 'port'
    default_port = 3306
    option_folder = 'folder'

    parser = OptionParser(usage="usage: %prog [options]",
                          version="schemadoc v%s" % (__version__,))
    parser.add_option('-s', help='host name to connect to MySQL server (default %s)' % (default_host,),
                      dest=option_host, action='store', default=default_host)
    parser.add_option('-u', help='user name to connect to MySQL server (default %s)'% (default_user,),
                      dest=option_user, action='store', default=default_user)
    parser.add_option('-p', help='password to connect to MySQL server (default %s)' % (default_password,),
                      dest=option_password, action='store', default=default_password)
    parser.add_option('-P', help='port used to connect (default %s)' % (default_port,),
                      dest=option_port, action='store', default=default_port)
    parser.add_option('-o', help='Output folder',
                      dest=option_folder, action='store')


    opts, args = parser.parse_args(argv)

    if len(argv) == 0:
        parser.print_help()
        return 1

    if not opts.folder:
        print('parameter -o is required', file=os.sys.stdout)
        parser.print_help()
        return 1

    url = build_database_url(host=opts.host, username=opts.user, password=opts.password)
    folder = opts.folder
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        elif len(os.listdir(folder)) != 0:
            print('Folder %s is not empty'%folder)
            return 1

    except OSError as e:
        print(repr(e), file=os.sys.stdout)
        print('Can not create folder %s'%folder, file=os.sys.stdout)
        return 1

    try:
        print("Generating documentation for %s \nOutput folder is %s" % (url, folder,), file=os.sys.stdout)
        _doc(url, folder)
    except Exception as e:
        print(repr(e), file=os.sys.stdout)
        return 1

    print("Documentation is generated in folder %s" % (folder,), file=os.sys.stdout)
    return 0

if __name__ == "__main__":
    exit_code = main(os.sys.argv[1:])
    os.sys.exit(exit_code)