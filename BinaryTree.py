import os
import re

songNameRegex = re.compile(r'.\w+$')
os.chdir('c:\\users\\alex_\\Desktop\\dis')
workingFolder = 'testFolder'

class Node:

    def __init__(self, data, path, size):

        self.left = None
        self.right = None
        self.data = data
        self.hdata = hash(data)
        self.path = path
        self.size = size

    def insert(self, data, path, size):
        # Compare the new value with the parent node
        mo = songNameRegex.search(data)
        if mo.group() in ('.db', '.txt', '.m3u', '.nfo', '.torrent', '.sfv', '.log', '.pls', '.doc',
                          '.html', '.ini', '.TXT', '.url', '.htm', '.m3u8', '.cue', '.BUP', '.IFO',
                          '.tmp', '.missing', '.rtf', '.DS_Store'):
            os.unlink(data)
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
                #this is where the song should actually get deleted
                print('Which file to delete: 1 or 2 ')
                if input('1: ' + data + ' of size ' + size + ' at path: ' + path + ' or \n'
                            '2: ' + self.data + ' of size ' + self.size + ' at path: ' + self.path) == '1':
                    os.unlink(path + data)
                    return
                else:
                    os.unlink(self.path + self.data)
                    self.data = data
                    self.path = path
                    self.size = size
        else:
            self.data = data
            self.path = path
            self.size = size


    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data, self.path, self.size),
        if self.right:
            self.right.PrintTree()


root = Node('a', 'b', 'c')
for folderName, subf, filenames in os.walk(workingFolder, topdown=True):
    for data in filenames:
        path = os.path.join(folderName +'\\')
        size = str(os.stat(os.path.join(folderName +'\\'+ data)).st_size)
        root.insert(data, path, size)


root.PrintTree()
