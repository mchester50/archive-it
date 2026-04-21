# archive-it
Used to find dups. 
# setup
The variables located at the beginning of the file require modification.
 BASE_PATH: This is where all the files to search are stored. In my case the share for my NAS. (archive)
1. Source: The source directory where the files that need to be checked for duplicates before being stored in the archive are located.
2. Search: The local directory where you put the files that you are wanting to archive after checking that there are no dupes. Something like "Downloads"
3. Destination: The local 'sorted' directory. 
4. Safety: Where to put duplicates. This is similar to a trashcan, but since it’s most likely to be run on a machine without a graphical user interface, we use this instead of the trashcan folder.

There is also a CATEGORIES list that you can add to which will determine where files that don't have dups are placed. The default CATEGORIES will place files with the file types of .stl .zip .step .scad .3mf .gcode
## 3d
'3d': ['.stl', '.zip', '.step', '.scad', '.3mf', '.gcode']
## Documents
'doc': ['.pdf', '.xml', '.gp5']
## image
'image': ['.png', '.jpg']
## win
'win': ['.exe']
## mac
'mac': ['.dmg']
