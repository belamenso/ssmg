#!/usr/bin/env python3

#######################
#### PARSING
#######################

ALLOWED='abcdefghijklmnopqrstuvwxyz0123456789-'

def clean_lyrics(dirty_lyrics):
    lyrics = dirty_lyrics.lower()
    ret = []
    current = ''
    for c in lyrics:
        if c in ALLOWED:
            current += c
        else:
            if current != '': ret += [current]
            current = ''
    if current != '': ret += [current]
    return ret

def clean_lyrics_to_SSMatrix(lyrics):
    return [[word_1 == word_2 for word_1 in lyrics] for word_2 in lyrics]

#######################
#### PNG GENERATION
#######################

from PIL import Image as PILImage

def color_array(ssmatrix, color_match, color_mismatch):
    return [color_match if x else color_mismatch
        for row in ssmatrix
            for x in row]

def save_png(ssmatrix, file_name, colors=((240, 194, 14), (30, 15, 30))):
    assert file_name.endswith('.png'), "file_name must end with <.png>"
    im = PILImage.new('RGB', (len(ssmatrix), len(ssmatrix)))
    im.putdata(color_array(ssmatrix, colors[0], colors[1]))
    im.save(file_name)

#######################
#### ENTROPY ANALYSIS
#######################

import zlib

def lyrics_to_entrypy(words):
    data_in = ' '.join(words).encode('utf-8')
    data_out = zlib.compress(data_in, level=9)
    return (len(data_out) / len(data_in)) if data_in != 0 else 0

#######################
#### GUI
#######################

from tkinter import *
from tkinter import ttk
from os import system

color_schemes = {
    'Green on black': ((32, 194, 14), (0, 0, 0)),
    'Poziomka': ((240, 57, 87), (30, 15, 30)),
    'Złoty': ((197, 179, 88), (30, 30, 30)),
}

def generate(*args):
    ls = text.get(1.0, END)
    lyrics = clean_lyrics(ls)
    save_png(clean_lyrics_to_SSMatrix(lyrics), 'hello.png', color_schemes[combo_var.get()])
    system('xdg-open hello.png')
    entropy_label['text']  ='Entropy of input: {:0.2f}%'.format(lyrics_to_entrypy(lyrics) * 100)

def clear_screen(*args):
    text.delete(1.0, END)

root = Tk()
root.title('Self-Similarity Matrix Generator')
root.update()
root.minsize(500, 250)

text = Text(root)
text.grid(row=0, column=0, sticky=(N, E, S, W))

btn_frame = ttk.Frame(root, padding=10)
btn_frame.grid(row=0, column=1)
ttk.Button(btn_frame, text='Generate (^Ret)', command=generate).grid(row=0, column=0, pady=5)
ttk.Button(btn_frame, text='Clear text area (^L)', command=clear_screen).grid(row=1, column=0, pady=5)

root.bind('<Control-Return>', generate)
root.bind('<Control-l>', clear_screen)
root.bind('<Control-L>', clear_screen)

combo_var = StringVar()
combo = ttk.Combobox(btn_frame, textvariable=combo_var)
combo_var.set('Poziomka')
combo.grid(row=2, column=0, pady=5)
combo['values'] = tuple(color_schemes.keys())

entropy_label = ttk.Label(btn_frame, text='Entropy of input: unknown')
entropy_label.grid(row=3, column=0, pady=5)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)

root.mainloop()

