'''This program crawls through a directory and lets you know if there are
names that will be considered duplicates in Windows. i.e. two folders named
example and Example in Linux would be the same folder in Windows. Therefore
if you copied this directory from Linux to Windows not everything would
copy. I have had issues with SpiderOak backing up files from Linux to Widows
and visa-versa. Michael Tiday mtiday@tidayventures.com'''
import os
#Create Global variables
GLOBAL_DIRECTORY_TO_SCAN = ''

def start():
    '''This function starts the program. Gets the directory to scan'''
    # Create a loop so the user has unlimited attempts to get the path correct
    while True:
        print('\nPlease enter a directory to scan for names that '
              'would be considered invalid duplicate in Windows.'
              '\nOr simply enter D to scan your Documents folder.'
              '\nEnter \'Q\' to quit the program:'
              '\n\nPlease note: It may take a while to scan large directories, like "home"\n')
        directory_to_scan= str(input())

        # Q to end program
        if directory_to_scan in ('q', 'Q'):
            print('\nHave a great day!!!\n')
            raise SystemExit()

        # D to  to select Documents folder
        if directory_to_scan in ('d', 'D'):
            directory_to_scan= os.path.expanduser('~/Documents')

        # Verify valid path was entered, if valid call the crawler
        try:
            os.chdir(directory_to_scan)
            global GLOBAL_DIRECTORY_TO_SCAN
            GLOBAL_DIRECTORY_TO_SCAN = directory_to_scan
            directory_crawler(directory_to_scan)
        except FileNotFoundError:
            print(f'\n\'{directory_to_scan}\' isn\'t a valid path\n'
                  'Please try again')

def directory_crawler(top_folder):
    '''This function does the 'work' it will scan the directory and sub-directories'''
    # create the needed lists:
    # list of all scanned directories and files
    directories_and_files = []
    # list that will contain all scanned directories 
    check_for_duplicates = []
    duplicates = []

    #Navigate to directory to scan
    os.chdir(top_folder)
    print('\nChecking for name issues in "' + os.getcwd() +'"\n')

    for path, dirnames, filenames in os.walk('.'):
        #Add directories to list
        for subdirname in dirnames:
            check_for_duplicates.append(os.path.join(path, subdirname))

        #Add files to list
        for filename in filenames:
            check_for_duplicates.append(os.path.join(path, filename))

    #Make everything in the list the same case
    for entry in directories_and_files:
        if list_to_check_for_duplicates.count(entry) > 1:
            duplicates.append(entry)
    if len(duplicates) > 0:
        build_desktop_file(duplicates)
    raise SystemExit()

def build_desktop_file(list_to_check):
    '''This function creates a list of "Windows" duplicates.
    Then saves the list as a file on the Desktop'''
    #clean list a little, removing '.'
    list_to_check = [entries.replace('.', '"\n"') for entries in list_to_check]
    # Create file on Desktop with possible duplicates, if applicable
    if len(list_to_check) > 0:
        os.chdir(os.path.expanduser('~/Desktop'))
        with open('Problem name(s) in Windows.txt', 'w') as problem_names:
            list_to_string = ' '.join([str(entry) for entry in list_to_check])
            problem_names.write(GLOBAL_DIRECTORY_TO_SCAN)
            problem_names.write(list_to_string)
        print('A file named "Problem name(s) in Windows.txt" has been saved on your Desktop')
    else:
        print('There were no names that would conflict in Windows')


#start the program eee
start()
