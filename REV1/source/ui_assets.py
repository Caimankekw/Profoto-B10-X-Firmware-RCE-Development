"""Compose native-style RECHARGE CTRL/NON-X/X assets from original glyphs.

No firmware mutation. build_assets(base) returns a relocatable bitmap blob and
descriptor addresses. CLI writes preview PNG and per-asset binary metadata.
"""
from pathlib import Path
import sys, struct, json
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'D3'))
import decode_bitmaps as original


def glyphs():
    # Explicit boundaries account for touching antialias columns (AI, DY, AX).
    # x coordinates are in human-readable images after ROTATE_90.
    source = {'A': (0x3e620, 0, 12), 'R': (0x3e620, 17, 28),
              'C': (0x3e620, 31, 43), 'H': (0x3e620, 44, 55),
              'E': (0x3e620, 94, 105), 'L': (0x3e620, 105, 113),
              'G': (0x3bb3c, 76, 88), 'Y': (0x3bb3c, 46, 57),
              'T': (0x3be68, 38, 48), 'X': (0x3af74, 26, 37),
              'N': (0x3e620, 68, 79), 'O': (0x3be68, 12, 24),
              '-': (0x38d90, 0, 7)}
    result = {ch: original.bitmap(addr).transpose(Image.Transpose.ROTATE_90)
              .crop((a, 0, b, 21)) for ch, (addr, a, b) in source.items()}
    bang = original.bitmap(0x3e620).transpose(Image.Transpose.ROTATE_90).crop((12,0,16,21))
    ImageDraw.Draw(bang).rectangle((0,11,3,12), fill=0)
    result['!'] = bang
    return result


def compose(text):
    chars = glyphs()
    w = sum(5 if c == ' ' else chars[c].width for c in text) + len(text) - 1
    im = Image.new('L', (w, 21))
    x = 0
    for c in text:
        if c == ' ':
            x += 6
        else:
            im.paste(chars[c], (x, 0))
            x += chars[c].width + 1
    return im


def encode(im):
    """Original codec: 1vvvv literal, 0nnn[extra n bits] repeat prev."""
    vals = [v // 17 for v in im.getdata()]
    bits = ''
    last = 0
    i = 0
    while i < len(vals):
        v = vals[i]
        nrun = 1
        while i + nrun < len(vals) and vals[i + nrun] == v:
            nrun += 1
        if v != last:
            bits += '1' + format(v, '04b')
            last = v
            i += 1
            nrun -= 1
        while nrun:
            count = min(nrun, 255)
            n = count.bit_length() - 1
            bits += '0' + format(n, '03b')
            if n:
                bits += format(count - (1 << n), f'0{n}b')
            i += count
            nrun -= count
    bits += '0' * ((-len(bits)) % 8)
    # Original decoder prefetches a 24-bit window; provide harmless zero pad.
    return bytes(int(bits[k:k+8], 2) for k in range(0, len(bits), 8)) + b'\0\0\0'


def build_assets(base):
    blob = bytearray()
    meta = {}
    for text in ['RECHARGE CTRL', 'NON-X', 'X', 'NON-X !', 'X !']:
        human = compose(text)
        native = human.transpose(Image.Transpose.ROTATE_270)
        encoded = encode(native)
        while (base + len(blob)) % 4:
            blob.append(0)
        p = base + len(blob)
        blob += encoded
        while (base + len(blob)) % 4:
            blob.append(0)
        descriptor = base + len(blob)
        blob += struct.pack('<HHI', native.width, native.height, p)
        # Round trip through the existing independent recovered decoder.
        saved = original.b
        try:
            temp = bytearray(descriptor - 0x08000000 + 8)
            temp[p - 0x08000000:p - 0x08000000 + len(encoded)] = encoded
            temp[descriptor - 0x08000000:] = blob[-8:]
            original.b = temp
            decoded = original.bitmap(descriptor - 0x08000000)
            assert decoded.tobytes() == native.tobytes()
        finally:
            original.b = saved
        meta[text] = dict(descriptor=descriptor, data=p, size=len(encoded),
                          native_wh=list(native.size), human_wh=list(human.size))
    return bytes(blob), meta


def menu_preview():
    """Reconstruct menu layout from 0800D044/0800E2A0, not a hardware capture."""
    asset = lambda a: original.bitmap(a).transpose(Image.Transpose.ROTATE_90)
    canvas = Image.new('RGB',(1000,570),'#242424')
    draw = ImageDraw.Draw(canvas)
    modes = ['NON-X', 'X', 'NON-X !']
    for col,mode in enumerate(modes):
        # Native row renderer uses 300 px horizontal width, 40 px tall endcaps,
        # 41 px row pitch and 8 px text inset. Screen surrounding margin is
        # illustrative; all row assets and inset/width measurements are exact.
        screen = Image.new('L',(320,240),0)
        title=asset(0x3d8fc)
        screen.paste(title,((320-title.width)//2,4))
        leftcap=asset(0x47e28);rightcap=asset(0x47e38)
        rows=[asset(0x3c268),asset(0x3c394),asset(0x3c668),compose('RECHARGE CTRL')]
        arrow=asset(0x341f4)
        for row,label in enumerate(rows):
            im=Image.new('L',(300,40),0)
            selected=row==3
            value=compose(mode) if selected else arrow
            if selected:
                im.paste(leftcap,(0,0));im.paste(rightcap,(300-rightcap.width,0))
                ImageDraw.Draw(im).rectangle((leftcap.width,0,299-rightcap.width,39),fill=255)
                im.paste(ImageOps.invert(label),(8,(40-label.height)//2))
                im.paste(ImageOps.invert(value),(300-8-value.width,(40-value.height)//2))
            else:
                im.paste(label.point(lambda v:round(v*160/255)),(8,(40-label.height)//2))
                im.paste(value,(300-8-value.width,(40-value.height)//2))
            screen.paste(im,(10,40+row*41))
        canvas.paste(screen,(col*330+5,35))
        canvas.paste(screen.resize((320,240),Image.Resampling.NEAREST),(col*330+5,310))
        draw.text((col*330+10,12),f'ADVANCED item 10: {mode}',fill='white')
    draw.text((10,285),'Renderer-derived reconstruction; row geometry/assets exact; surrounding screen spacing illustrative.',fill='white')
    return canvas


if __name__ == '__main__':
    blob, meta = build_assets(0x080A0000)
    out = Path(__file__).resolve().parent.parent / "build"
    out.mkdir(parents=True, exist_ok=True)
    (out/'ui_assets_preview.bin').write_bytes(blob)
    (out/'ui_assets_preview.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    preview = Image.new('RGB', (900, 430), '#222222')
    d = ImageDraw.Draw(preview)
    for i, text in enumerate(meta):
        im = compose(text)
        preview.paste(im.resize((im.width*3, im.height*3)), (15, i*85+12))
        d.text((550, i*85+25), f'{text}: {im.width} x {im.height}', fill='white')
    preview.save(out/'ui_assets_preview.png')
    menu_preview().save(out/'ui_menu_preview.png')
    print(json.dumps(meta, indent=2))
    print('All 5 assets round-trip through recovered original decoder.')
