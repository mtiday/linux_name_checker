"""This program is compatible with Python3.6 and higher. It crawls through
a directory and lets you know if there are names that will be considered
duplicates in Windows. i.e. two folders named example and Example in Linux
would be the same folder in Windows. Therefore if you copied this directory
from Linux to Windows not everything would copy. I have had issues with
SpiderOak backing up files from Linux to Widows and visa-versa.
Michael Tiday mtiday@tidayventures.com"""
import os


def start():
    """This function starts the program. Gets the directory to scan"""
    # Create a loop so the user has unlimited attempts to get the path correct
    while True:
        print('\nPlease enter a directory to scan for names that '
              'would be considered invalid duplicate in Windows.'
              '\nOr simply enter D to scan your Documents folder.'
              '\nEnter \'Q\' to quit the program:'
              '\n\nPlease note: It may take a while to scan large directories, like "home"\n')
        directory_to_scan = str(input())

        # Q to end program
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
        except FileNotFoundError:
            print(f'\n\'{directory_to_scan}\' isn\'t a valid path\n'
                  'Please try again')


def directory_crawler(directory_to_scan):
    """This function does the 'work' it will scan the directory and sub-directories"""
    # create the needed lists:
    # list of all scanned directories and files
    directories_and_files = []
    # Contents of this list will be lower case
    directories_and_files_lower = []
    duplicates = []

    # Navigate to directory to scan
    os.chdir(directory_to_scan)
    print('\nChecking for name issues in "' + os.getcwd() + '"\n')

    for path, dirnames, filenames in os.walk('.'):
        # Add directories to list
        for subdir in dirnames:
            directories_and_files.append(os.path.join(path, subdir))

        # Add files to list
        for file in filenames:
            directories_and_files.append(os.path.join(path, file))

    # Make a list with all the same case
    for path in directories_and_files:
        directories_and_files_lower.append(path.lower())

    # Create a list of duplicates, where each element matches what's stored on disk
    for entry, lc_entry in zip(directories_and_files, directories_and_files_lower):
        if directories_and_files_lower.count(lc_entry) > 1:
            duplicates.append(entry)
    if len(duplicates) > 0:
        build_desktop_file(duplicates, directory_to_scan)
    else:
        print('There were no names found that would conflict in Windows')
        print('Have a great day!!!\n')
    raise SystemExit()


def build_desktop_file(list_to_check, directory_to_scan):
    """If any "Windows" duplicates are found; this function creates a list
     and saves the list as a file on the Desktop."""
    # Change directory to Desktop so the file will be saved there
    os.chdir(os.path.expanduser('~/Desktop'))

    # Create file on Desktop with possible duplicates
    with open('Problem names in Windows.txt', 'w') as problem_names:
        problem_names.write(f'The conflict(s) below were found scanning directory'
                            f' {directory_to_scan}')
        for element in list_to_check:
            problem_names.write('\n')
            problem_names.write(element)
    print('A file named "Problem names in Windows.txt" has been saved on your Desktop')
    print('Have a great day!!!\n')


# start the program
start()

