# -*- coding: utf-8 -*-
# Copyright (c) 2012, Jonas Obrist
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Jonas Obrist nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL JONAS OBRIST BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from pymaging.colors import RGB
from pymaging.exceptions import FormatNotSupported
from pymaging.formats import Format
from pymaging.image import Image
from pymaging_jpg.raw import TonyJpegDecoder
from pymaging.pixelarray import get_pixel_array
import array

PIXELSIZE = 3

def open_image(fileobj):
    decoder = TonyJpegDecoder()
    jpegsrc = fileobj.read()
    try:
        decoder.read_headers(jpegsrc)
    except:
        fileobj.seek(0)
        return None
    fileobj.seek(0)
    return Image(RGB, decoder.Width, decoder.Height, lambda: read_pixels(fileobj))


def read_pixels(fileobj):
    decoder = TonyJpegDecoder()
    bmpout = decoder.decode(fileobj.read())
    pixels = array.array('B')
    row_width = decoder.Width * PIXELSIZE
    # rows are bottom to top
    for reversed_row_num in range(decoder.Height - 1, -1, -1):
        start = reversed_row_num * (row_width + 2)
        end = start + row_width
        pixels.extend(bmpout[start:end])
        #pixels.extend(bmpout[:3 * decoder.Width])
        #del bmpout[:3 * decoder.Width]
        #del bmpout[:2] # kill padding
    pixel_array = get_pixel_array(pixels, decoder.Width, decoder.Height, PIXELSIZE)
    return pixel_array, None

def save_image(image, fileobj):
    raise FormatNotSupported('jpeg')

JPG = Format(open_image, save_image, ['jpg', 'jpeg'])
