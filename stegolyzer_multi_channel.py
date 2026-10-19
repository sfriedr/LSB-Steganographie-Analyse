#!/usr/bin/env python3

"""
stegolyzer - a tool to statistically analyze and plot the average of LSBs of an image file.

Steganography is difficult to detect. However, statistical analysis can help to find 
anomalies in the distribution of LSB values. Depending on the motive of an image, LSB values
can be expected to exhibit certain distributions. 

For example, an image that is completely white (full white, each pixel #ffffff) certainly shows 
a different LSB distribution than that with a scenic photo. Think about why that may be the case 
and you'll understand one way of (possibly) detecting steganography.

Beispiel: python stegolyzer.py stego_object_red_lsb.png red
"""

import sys
import struct
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

from PIL import Image


def analyse(in_file):
    """
    Performs statistical analysis of an image to potentially detect LSB steganography.
    Aggregates a sequence of LSBs (e.g., 1000) (per color channel) and computes the 
    average value for it.

    :param in_file: The filename of the image file
    :param channel: The name of the color channel, must be one of red, green, blue, alpha
    """
    # Block size. Aggregate this many bits to form one block for which the average is computed.
    bits_per_block = 1000
    img = Image.open(in_file)
    (width, height) = img.size
    print("[+] Image size: %dx%d pixels" % (width, height))
    conv = img.convert("RGBA").getdata()

    # Extract LSBs
    vr = [] # a list of only the LSBs from the red channel
    vg = [] # a list of only the LSBs from the green channel
    vb = [] # a list of only the LSBs from the blue channel
    va = [] # a list of only the LSBs from the alpha channel
    # Walk over the image
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            vr.append(r & 1)
            vg.append(g & 1)
            vb.append(b & 1)
            va.append(a & 1)

    # Compute the average color channel LSB per block
    avgR = []
    avgG = []
    avgB = []
    avgA = []
    # Aggregate bits_per_block and compute the average (mean)
    for i in range(0, len(vr), bits_per_block):
        avgR.append(numpy.mean(vr[i:i + bits_per_block]))
        avgG.append(numpy.mean(vg[i:i + bits_per_block]))
        avgB.append(numpy.mean(vb[i:i + bits_per_block]))
        avgA.append(numpy.mean(va[i:i + bits_per_block]))

    # Plot the average (mean) value for each block. The x-axis denotes the blocks and 
    # the y-axis denotes the average value.
    numBlocks = len(avgR)
    blocks = [i for i in range(0, numBlocks)]



    # Plot zeichnen ---------------------------------------------------------------------

    # Erstellt Plot bestehend aus 2x2 Subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 18), constrained_layout=True)
    # 2, 2 -> Erstellt 2x2 Subplots
    # constrained_layout=True -> Berechnet automatisch adequate vertikale Abstände zwischen Subplots.
    fig.suptitle('Statistical LSB analysis', fontsize=20, fontweight='bold', y=0.99)

    # Farbpalette und Axeslimits für einheitliches Design
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("viridis", as_cmap=False)

    x_axis_min_limit: int = 0
    x_axis_max_limit: int = 2000
    y_axis_min_limit: int = 0
    y_axis_max_limit: int = 1


    # --- ZEILE 0: ROT & GRÜN ---

    # 1. Red Channel (Oben Links)
    sns.scatterplot(x=blocks, y=avgR, ax=axes[0, 0], color='crimson', linewidth=0.1)
    # linewidth -> Stellt die Dicke der Umrandung der Punkte im Scatterplot ein.
    # edgecolor=None -> Deaktiviert Umrandung
    axes[0, 0].set_title('Red channel analysis', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Block number')
    axes[0, 0].set_ylabel('Average LSB per block')

    # 2. Green Channel (Oben Rechts)
    sns.scatterplot(x=blocks, y=avgG, ax=axes[0, 1], color='forestgreen', linewidth=0.1)
    axes[0, 1].set_title('Green channel analysis', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Block number')
    axes[0, 1].set_ylabel('Average LSB per block')


    # --- ZEILE 1: BLAU & ALPHA ---

    # 3. Blue Channel (Mitte Links)
    sns.scatterplot(x=blocks, y=avgB, ax=axes[1, 0], color='royalblue', linewidth=0.1)
    axes[1, 0].set_title('Blue channel analysis', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Block number')
    axes[1, 0].set_ylabel('Average LSB per block')

    # 4. Alpha Channel (Mitte Rechts)
    sns.scatterplot(x=blocks, y=avgA, ax=axes[1, 1], color='darkorange', linewidth=0.1)
    axes[1, 1].set_title('Alpha channel analysis', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Block number')
    axes[1, 1].set_ylabel('Average LSB per block')



    active_axes = [axes[0, 0], axes[0, 1], axes[1, 0], axes[1, 1]] # Liste der Subplots

    # Achsengrenzen für alle Subplots setzen:
    for ax in active_axes:
        ax.set_xlim(x_axis_min_limit, None)
        ax.set_ylim(y_axis_min_limit, y_axis_max_limit)


    plt.show() # Dashboard anzeigen

    #------------------------------------------------------------------


def usage(progName):
    print(f"""
    Usage:
        {progName} <image_file>

    where <image_file> is the image file name 
""")
    sys.exit()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    analyse(sys.argv[1])
        
