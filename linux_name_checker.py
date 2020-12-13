"""File name checker for Windows
This program crawls through a directory and lets you know if there are
names that will be considered duplicates in Windows. i.e. two folders
named example and Example in Linux would be the same folder in Windows.
Therefore if you copied this directory from Linux to Windows not
everything would copy.
Michael Tiday mtiday@tidayventures.com
"""

import os


def start():
    """This function starts the program. Gets the directory to scan."""
    # Create loop, user has unlimited attempts to get the path correct
    while True:
        print('\nPlease enter a directory to scan for names that '
              'would be considered invalid duplicate in Windows.'
              '\nOr simply enter D to scan your Documents folder.'
              '\nEnter \'Q\' to quit the program:'
              '\n\nPlease note: It may take a while to scan large directories, like "home"\n')
        directory_to_scan = str(input())

        # 'Q' Raises SystemExit() to end program
        if directory_to_scan in ('q', 'Q'):
            print('\nHave a great day!!!\n')
            raise SystemExit()

        # D to  to select Documents folder
        if directory_to_scan in ('d', 'D'):
            directory_to_scan = os.path.expanduser('~/Documents')

        # Verify valid path was entered, if valid call the crawler
        try:
            os.chdir(directory_to_scan)
            directory_crawler(directory_to_scan)
        # Raise exception if directory isn't valid
        except FileNotFoundError:
            print(f"\n'{directory_to_scan}' is not a valid path\nPlease try again.")


def directory_crawler(top_folder):
    """Builds a list of file and directory names for duplicate
    checking. Scans the directory and sub-directories of the top_folder
    :param str top_folder: filesystem path to begin working in

    Raises:
    - SystemExit on completion"""

    # list of all scanned directories and files
    directories_and_files = []
    # Contents of this list will be lower case
    directories_and_files_lower = []
    # list will contain files Windows would consider duplicates
    duplicates = []

    # Navigate to directory to scan
    os.chdir(top_folder)
    print('\nChecking for name issues in "' + os.getcwd() + '"\n')

    for path, dirnames, filenames in os.walk('.'):
        # Add directories to list
        for subdirname in dirnames:
            directories_and_files.append(os.path.join(path, subdirname))

        # Add files to list
        for filename in filenames:
            directories_and_files.append(os.path.join(path, filename))

    # Make everything in the list the same case
    for path in directories_and_files:
        directories_and_files_lower.append(path.lower())

    # Create a list of that Windows would consider duplicates
    for entry, lc_entry in zip(directories_and_files, directories_and_files_lower):
        if directories_and_files_lower.count(lc_entry) > 1:
            duplicates.append(entry)
    if len(duplicates) > 0:
        build_desktop_file(duplicates, top_folder)
    else:
        print('There were no names found that would conflict in Windows')
        print('Have a great day!!!\n')
    raise SystemExit()


def build_desktop_file(duplicates, directory_to_scan):
    """Given a list of "Windows" duplicate names, will save the list to
    a file on the Desktop.
    :param: List duplicates: any duplicates will be stored here
    :param: List directory_to_scan:
    the directory that was scanned for duplicates
    """

    os.chdir(os.path.expanduser('~/Desktop'))
    with open('Problem name(s) in Windows.txt', 'w') as problem_names:
        problem_names.write(f'The conflict(s) below were found scanning directory '
                            f'{directory_to_scan}')
        for element in duplicates:
            problem_names.write('\n')
            problem_names.write(element)
        print('A file named "Problem name(s) in Windows.txt" has been saved on your Desktop\n')


# start the program
if __name__ == "__main__":
    start()
