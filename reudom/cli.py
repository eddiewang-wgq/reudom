import os
# import re
import sys
import ssl
# import shutil
# import zipfile
# import tarfile
import logging
import argparse
import platform
# from os import makedirs
# from os.path import join, isfile, basename
# from os.path import isdir, dirname, abspath
# from urllib.request import urlopen

from reudom import __description__, __version__

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PY3 = sys.version_info[0] == 3

versions = sorted(['32', '64'], key=lambda v: not platform.machine().endswith(v))
os_opts = [('win', 'win', '.exe'), ('darwin', 'mac', ''), ('linux', 'linux', '')]

current_os = None
ext = ''
for o in os_opts:
    if o[0] in platform.system().lower():
        current_os = o[1]
        ext = o[2]

ssl._create_default_https_context = ssl._create_unverified_context


def main():
    """
    API test: parse command line options and run commands.
    """

    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-v', '--version', dest='version', action='store_true',
        help="show version")

    parser.add_argument(
        '--project',
        help="Create an Reudom automation test project.")

    parser.add_argument(
        '-r',
        help="run test case")

    args = parser.parse_args()

    if args.version:
        print("version {}".format(__version__), )
        return 0

    project_name = args.project
    if project_name:
        create_scaffold(project_name)
        return 0

    run_file = args.r
    if run_file:
        logger.info("Run the python version:")
        if PY3:
            ret = os.system("python -V")
            if ret != 0:
                os.system("python3 -V")
                command = "python3 " + run_file
            else:
                command = "python " + run_file
        else:
            raise NameError("Does not support python2")
        os.system(command)
        return 0

def create_scaffold(project_name):
    """
    create scaffold with specified project name.
    """
    if os.path.isdir(project_name):
        logger.info(u"Folder {} exists, please specify a new folder name.".format(project_name))
        return

    logger.info("Start to create new test project: {}".format(project_name))
    logger.info("CWD: {}\n".format(os.getcwd()))

    def create_folder(path):
        os.makedirs(path)
        msg = "created folder: {}".format(path)
        logger.info(msg)

    def create_file(path, file_content=""):
        with open(path, 'w') as f:
            f.write(file_content)
        msg = "created file: {}".format(path)
        logger.info(msg)

    test_sample = '''
import reudom
class YouTest(reudom.TestCase):
    def test_case01(self):
        """Write the test case again"""
    
    
if __name__ == '__main__':
    reudom.main("test_sample.py")
'''
    run_test = """
import reudom


if __name__ == '__main__':
    # run test
    # reudom.main("./test_dir/")
    reudom.main("./test_dir/test_sample.py")

"""
    create_folder(project_name)
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_file(os.path.join(project_name, "test_dir", "test_sample.py"), test_sample)
    create_file(os.path.join(project_name, "run.py"), run_test)
