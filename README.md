# runescape-text
Generates a gif of text based on runescape chatbox effects

If you long for the days of selling your rune scimmy:

`python runescapetext.py wave:glow1:This will generate a convincing replica`

![A convincing replica](https://imgur.com/XGM9rjr.gif)

Or as an import:
```python
import runescape_text as rst

img = rst.parse_string("wave:glow1:Hello World")
if(len(img)==1):
	rst.single_frame_save(img[0], file="out.png")
else:
	rst.multi_frame_save(img, file="out.gif")
```

A Discord bot implementing this has been broken out into a seperate repository. Find it [here](https://github.com/sircinnamon/runescape-text-discord).