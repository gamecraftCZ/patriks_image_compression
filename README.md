# Patrik's image compression (PIC)

**This is just a scratch in python to show the algorithm. The compression is slow in this implementation.**

Custom image compression. Works on principles of finding similar patterns and reusing them as much as possible.

Searches for the most similar blob in 8x8 (6bits) area around current block.  
Tries some rotations (currently NONE, LEFT, RIGHT, DOWN (2bits)) and selects the one with best similarity.  
If similarity is not enough, save just the pixels as they are.


## Build to .exe
- Built .exe will be saved in folder dist
```
pip install pyinstaller
pyinstaller  -F --noconsole __main__.py
```

## TODO
- Find saving type where output image size is the smallest.
- Try blobs similar search in 16x16 (8bits) area
- Add more rotations (+calculate missing pixels)
- Add finding similarity using blob movement by 1-2 pixels (+calculate missing pixels)
- AI for calculating missing pixels
- AI for hiding artifacts

## LICENSE
Feel free to use this algorithm in your projects. You must credit me and my repository in your project credits.  
This license is for the whole algorithm, not just this python program.

