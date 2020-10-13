import os
import re
import sys
import PySimpleGUI as sg
# import BinaryTree

sg.theme('DarkGrey6')   # Color theme
# sg.theme_previewer()


# This is how it looks (layout):

col_layout = [[sg.Text('Selected folder is: ')],
              [sg.Text(''), sg.Text(size=(2,1))]]

col_layout_1 = [[sg.Text(''), sg.Text(size=(30, 5), key='-LOC1-')],
                []]

col_layout_2 = [[sg.Text(''), sg.Text(size=(30, 5), key='-LOC2-')],
                []]

layout = [  [sg.Column(col_layout), sg.Text(size=(40,3), key='-FOLDER-', ), sg.FolderBrowse('Choose folder', target = '-FOLDER-')],
            [sg.Button('Start'), sg.Button('Stop')],
            [sg.Text('File to delete: '), sg.Text(size=(50, 1), font = 'Any 10', text_color='yellow', key='-SONGNAME-')], # this will be updated by the main logic automatically
            [sg.Frame('First location: ', col_layout_1, element_justification='c'), sg.VSeparator(), sg.Frame('Second location: ', col_layout_2, element_justification='c')],
            [sg.Text('Delete file from:')],
            [sg.Text(' '), sg.Text(size=(9, 1)), sg.Button('Location 1'), sg.Text(''), sg.Text(size=(9, 1)), sg.VSeparator(), sg.Text(''), sg.Text(size=(9, 1)),sg.Button('Location 2')],
            [sg.Text(' '), sg.Text(size=(9, 1))],
            [sg.Text(' '), sg.Text(size=(28, 1)), sg.Button('Skip file')],
            [sg.Text(' '), sg.Text(size=(9, 1))]]



workingFolder = sg.popup_get_folder('Where to search?')

# Create the Window
window = sg.Window('FileKiller', layout, keep_on_top=True, alpha_channel=1)


# Define the binary tree class
class Node:

    def __init__(self, data, path, size):

        self.left = None
        self.right = None
        self.data = data
        self.hdata = hash(data)
        self.path = path
        self.size = size

    def insert(self, data, path, size):
        fileExtensionRegex = re.compile(r'.\w+$')
        mo = fileExtensionRegex.search(data)
        # if mo.group() in ('.db', '.txt', '.m3u', '.nfo', '.torrent', '.sfv', '.log', '.pls', '.doc',
        #                   '.html', '.ini', '.TXT', '.url', '.htm', '.m3u8', '.cue', '.BUP', '.IFO',
        #                   '.tmp', '.missing', '.rtf', '.DS_Store'):
        #     os.unlink(data)

        if mo.group() in ('.mp3', '.MP3', '.wma', '.Mp3', '.m4a', '.flac', '.mpg',
                          '.mp4', '.VOB', '.wav', '.mkv', '.avi'):
            # Compare the new value with the parent node
            if self.hdata:
                if hash(data) < self.hdata:
                    if self.left is None:
                        self.left = Node(data, path, size)
                    else:
                        self.left.insert(data, path, size)
                elif hash(data) > self.hdata:
                    if self.right is None:
                        self.right = Node(data, path, size)
                    else:
                        self.right.insert(data, path, size)
                else:
                    # this is where the file should actually get deleted

                    window['-SONGNAME-'].update(data)
                    window['-LOC1-'].update(path + '\n\nSize: ' + size)
                    window['-LOC2-'].update(self.path + '\n\nSize ' + self.size)
                    event, values = window.read()
                    if event == 'Location 1':
                        os.unlink(path + data)
                    if event == 'Location 2':
                        os.unlink(self.path + self.data)
                        self.data = data
                        self.path = path
                        self.size = size
                    if event == 'Skip file':
                        return None
            else:
                self.data = data
                self.path = path
                self.size = size

# Initialize the binary tree:
# root = Node('a', 'b', 'c')




# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read(timeout=1000)
    print(event, values )
    window['-FOLDER-'].update(workingFolder)
    if event == '-FOLDER-':
        window['-FOLDER-'].update(values['-FOLDER-'])
        workingFolder = values['-FOLDER-']
    if event == sg.WIN_CLOSED or event == 'Stop': # if user closes window or clicks cancel
        break
    if event == 'Start':
        root = Node('a', 'b', 'c')
        for folderName, subf, filenames in os.walk(workingFolder, topdown=False):
            for data in filenames:
                path = os.path.join(folderName + '\\')
                size = str(os.stat(os.path.join(folderName + '\\' + data)).st_size)
                root.insert(data, path, size)
                window.refresh()


# closes window
window.close()
