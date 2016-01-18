#!/bin/python
import os
import sys
import subprocess
import shlex
import argparse
import platform


LINUX_DISTRIBUTION = platform.linux_distribution()[0].lower()
if LINUX_DISTRIBUTION.startswith('arch'):
    LINUX_DISTRIBUTION = 'arch'
elif LINUX_DISTRIBUTION.startswith('gentoo'):
    LINUX_DISTRIBUTION = 'gentoo'


DEPENDENCIES = [
    'pygmentize',
    'cowsay',
    'toilet',
    'asciiquarium',
    'cinnamon-session'
]


if LINUX_DISTRIBUTION == 'arch':
    DEPENDENCIES.append('yaourt')
elif LINUX_DISTRIBUTION == 'gentoo':
    DEPENDENCIES.append('layman')


INSTALL_DIR = os.path.dirname(os.path.realpath(__file__)) 
USER_DIR = os.path.expanduser('~')
ROOT_DIR = '/root'
CONFIGS_DIR = os.path.join(INSTALL_DIR, 'Configs')
SCRIPTS_DIR = os.path.join(INSTALL_DIR, 'Scripts')
DESKTOP_CONFIG_FILE = os.path.join(CONFIGS_DIR, 'dconf_backup.dconf')

USER_CONFIGS_DIR = os.path.join(CONFIGS_DIR, 'user_only')
SHARED_CONFIGS_DIR = os.path.join(CONFIGS_DIR, 'shared')
ROOT_CONFIGS_DIR = os.path.join(CONFIGS_DIR, 'root_only')


def get_arguments():
    parser = argparse.ArgumentParser(description="Installs Morzeux's dotfiles.")
    parser.add_argument('-r', '--root', action='store_true', help='configures root-dotfiles')
    parser.add_argument('-f', '--force', action='store_true', help='overrides existing files')
    parser.add_argument('-v', '--verbose', action='store_true', help='prints useful output')
    return parser.parse_args()


ARGS = get_arguments()


def my_print(msg):
    if ARGS.verbose is True:
        print(msg)


def handle_existing_items(dst_path):
    if os.path.exists(dst_path) or os.path.islink(dst_path):
        if ARGS.force is True:
            os.remove(dst_path)
            my_print('  Removed file "%s"' % dst_path)
        else:
            sys.stderr.write('  File "%s" already exists!\n' % dst_path)
            sys.exit(1)


def process(cmd):
    my_print('  Executing "%s"' % cmd)
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    output, err = process.communicate()
    exit_code = process.wait()

    if exit_code != 0:
        sys.exit(exit_code)
    else:
        return output.decode('UTF-8').strip()

def installed(filename):
    with open(os.devnull, 'w') as DEVNULL:
        return subprocess.Popen(['which', filename], stdout=DEVNULL, stderr=DEVNULL).wait() == 0


def check_dependencies():
    for appname in DEPENDENCIES:
        if installed(appname) is False:
            sys.stderr.write('Warning! Application "%s" not found!\n' % appname)


def create_symlinks(src_configs_dir, dst_base_dir, ext=False, all_files=False):
    for fname in os.listdir(src_configs_dir):
        if fname == '.config':
            for root_path, folders, files in os.walk(os.path.join(src_configs_dir, fname)):
                if files:
                    dst_base_path = os.path.join(dst_base_dir, root_path[len(src_configs_dir) + 1:])
                    if not os.path.exists(dst_base_path):
                        os.makedirs(dst_base_path)

                    create_symlinks(root_path, dst_base_path, all_files=True)

        elif fname == LINUX_DISTRIBUTION:
            create_symlinks(os.path.join(src_configs_dir, fname), dst_base_dir, ext=True)
            continue

        elif all_files is True or fname.startswith('.'):
            src_path = os.path.join(src_configs_dir, fname)
            dst_path = os.path.join(dst_base_dir, fname + ('_ext' if ext is True else ''))

            handle_existing_items(dst_path)
            process('ln -s %s %s' % (src_path, dst_path))


def create_dotfiles_conf(dst_path):
    with open(os.path.join(dst_path, '.dotfiles_conf'), 'w') as fw:
        fw.write("""
#!/bin/bash

export DOTFILES_PATH='%s'
""".strip() % INSTALL_DIR)


def load_desktop_configs():
    if not installed('dconf'):
        sys.stderr.write('Warning! Application "dconf" not found!\n')
        return

    process('dconf load / < %s' % DESKTOP_CONFIG_FILE)


def main():
    check_dependencies()

    if ARGS.root is True:
        src_configs_dir = ROOT_CONFIGS_DIR
        dst_base_dir = ROOT_DIR
    else:
        src_configs_dir = USER_CONFIGS_DIR
        dst_base_dir = USER_DIR

    print('Creating dotfiles config...')
    create_dotfiles_conf(dst_base_dir)

    print('Creating sym links for %s configs...' % (
        'root' if ARGS.root is True else 'user')
    )
    create_symlinks(src_configs_dir, dst_base_dir)

    print('Creating sym links for shared configs...')
    create_symlinks(SHARED_CONFIGS_DIR, dst_base_dir)

    print('Creating sym links for scripts...')
    dst_scripts_dir = os.path.join(dst_base_dir, 'Scripts')
    if not os.path.exists(dst_scripts_dir):
        os.makedirs(dst_scripts_dir)
    create_symlinks(SCRIPTS_DIR, dst_scripts_dir, all_files=True)

    # print('Loading desktop config...')
    # load_desktop_configs()

    print('FINISHED')


if __name__ == '__main__':
    main()
