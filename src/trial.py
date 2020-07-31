import os

path = 'progfiles'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if file.count('.pyc')==0:
            files.append(os.path.join(r, file))

for f in files:
    print(f)