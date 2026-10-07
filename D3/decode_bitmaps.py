"""Decode the firmware's 4-bit grayscale run length stream, from 08000d8c/08000dc0."""
import struct
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent
b=(ROOT/'firmware/B10_REV_D3.bin').read_bytes()
def bitmap(off, details=False):
    w,h,p=struct.unpack_from('<HHI',b,off);p-=0x08000000
    free=24;bits=0;val=0;run=0;out=[]
    for _ in range(w*h):
        if run>0:run-=1
        else:
            while free>7:
                free-=8;bits |= b[p]<<free;p+=1
            if bits&0x800000:
                n=5;val=(bits&0x780000)>>19
            else:
                n=(bits&0x700000)>>20
                run=((bits&0xff000)>>(20-n)) | (1<<n)
                run-=1;n+=4
            bits=(bits<<n)&0xffffff;free+=n
        out.append(val*17)
    im=Image.new('L',(w,h));im.putdata(out)
    return (im,p) if details else im
