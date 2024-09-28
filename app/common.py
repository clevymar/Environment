import os
import sys

#add the directories
#look for the path of the Files directory
dirFiles = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Files')
print(dirFiles)