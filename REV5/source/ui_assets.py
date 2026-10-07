# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Caimankekw.
"""Compose RC5 recharge/ECO assets from original B10 REV-D3 21 px glyphs.

No firmware mutation. build_assets(base) returns a relocatable bitmap blob and
descriptor addresses. CLI writes preview PNG and per-asset binary metadata.
"""
from pathlib import Path
import sys, struct, json
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'D3'))
import decode_bitmaps as original

HOME_PROFILE_TEXTS = ('NON-X', 'X', 'BOOST', 'NON-X !', 'X !', 'BOOST !')
ASSET_TEXTS = ('RECHARGE CTRL', 'NON-X', 'X', 'NON-X !', 'X !',
              'BOOST', 'BOOST !', 'ECO', 'ECO !', 'ECO_HOME') + tuple(
                  'RECHARGE_HOME_' + text for text in HOME_PROFILE_TEXTS)
RECHARGE_VALUES = ('NON-X', 'X', 'BOOST', 'NON-X !', 'X !', 'BOOST !')
NATIVE_EXTRA_GLYPHS = {'B': 0x38634, 'S': 0x38abc}
HOME_GLYPH_SOURCES = {'E': (0x34774, 25, 7, 32, 16),
                      'C': (0x345e8, 3, 7, 12, 16),
                      'O': (0x345e8, 12, 7, 22, 16)}


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
    # Original bold 21 px standalone glyphs; no font substitution or resizing.
    for ch, addr in NATIVE_EXTRA_GLYPHS.items():
        result[ch] = original.bitmap(addr).transpose(Image.Transpose.ROTATE_90)
        assert result[ch].height == 21
    bang = original.bitmap(0x3e620).transpose(Image.Transpose.ROTATE_90).crop((12,0,16,21))
    ImageDraw.Draw(bang).rectangle((0,11,3,12), fill=0)
    result['!'] = bang
    return result


def compose(text):
    if text.startswith('RECHARGE_HOME_'):
        # The native home status strip has a 12 px gap above the mode cell.
        # Fit a 9 px word there without moving any native icons or power text.
        # Downsample only the existing D3 glyph raster, never a system font;
        # quantize back to the original decoder's 4-bit grayscale alphabet.
        source = compose(text[len('RECHARGE_HOME_'):])
        source = source.crop(source.getbbox())
        width = round(source.width * 9 / source.height)
        small = source.resize((width, 9), Image.Resampling.LANCZOS)
        small = small.point(lambda value: min(15, (value + 8) // 17) * 17)
        assert width <= 64
        im = Image.new('L', (64, 9))
        im.paste(small, ((64-width)//2, 0))
        return im
    if text == 'ECO_HOME':
        # Match the original FREEZE status badge's 64 x 24 cell and 9 px
        # capitals. Copy native small glyphs without scaling or font changes.
        im = Image.new('L', (64, 24))
        x = 18
        for c in 'ECO':
            addr, left, top, right, bottom = HOME_GLYPH_SOURCES[c]
            letter = original.bitmap(addr).transpose(Image.Transpose.ROTATE_90).crop((left, top, right, bottom))
            im.paste(letter, (x, 7))
            x += letter.width + 1
        assert x - 1 == 46
        return im
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
    assert 0x08000000 <= base <= 0x080fffff
    for text in ASSET_TEXTS:
        human = compose(text)
        assert all(v % 17 == 0 for v in human.getdata()), text
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
            assert decoded.size == native.size
            assert decoded.tobytes() == native.tobytes()
        finally:
            original.b = saved
        meta[text] = dict(descriptor=descriptor, data=p, size=len(encoded),
                          native_wh=list(native.size), human_wh=list(human.size))
    label_width = meta['RECHARGE CTRL']['human_wh'][0]
    max_value_width = max(meta[text]['human_wh'][0] for text in RECHARGE_VALUES)
    assert label_width == 149
    assert label_width + max_value_width + 16 < 300
    return bytes(blob), meta


def asset(address):
    return original.bitmap(address).transpose(Image.Transpose.ROTATE_90)


def menu_row(label, value, selected=True):
    """Recovered 0800D044 geometry; assert label/value bounds before drawing."""
    assert label.height <= 40 and value.height <= 40
    assert 8 + label.width < 300 - 8 - value.width
    im = Image.new('L', (300, 40), 0)
    if selected:
        leftcap, rightcap = asset(0x47e28), asset(0x47e38)
        im.paste(leftcap, (0, 0))
        im.paste(rightcap, (300-rightcap.width, 0))
        ImageDraw.Draw(im).rectangle(
            (leftcap.width, 0, 299-rightcap.width, 39), fill=255)
        label, value = ImageOps.invert(label), ImageOps.invert(value)
    else:
        label = label.point(lambda v: round(v*160/255))
    im.paste(label, (8, (40-label.height)//2))
    im.paste(value, (300-8-value.width, (40-value.height)//2))
    return im


def recharge_screen(mode):
    screen = Image.new('L', (320, 240), 0)
    title = asset(0x3d8fc)
    screen.paste(title, ((320-title.width)//2, 4))
    rows = [asset(0x3c268), asset(0x3c394), asset(0x3c668), compose('RECHARGE CTRL')]
    for index, label in enumerate(rows):
        value = compose(mode) if index == 3 else asset(0x341f4)
        screen.paste(menu_row(label, value, index == 3), (10, 40+index*41))
    return screen


def flash_screen(mode):
    # Show the selected row alone: unrelated settings/scroll offset are omitted.
    screen = Image.new('L', (320, 240), 0)
    title = asset(0x3b424)
    screen.paste(title, ((320-title.width)//2, 4))
    value = {'NORMAL': lambda: asset(0x3ab40),
             'FREEZE': lambda: asset(0x3acc0)}.get(mode, lambda: compose(mode))()
    screen.paste(menu_row(asset(0x3a9ec), value), (10, 81))
    return screen


def menu_preview():
    """Renderer-derived reconstruction, not a hardware capture or UI test."""
    canvas = Image.new('RGB', (1000, 605), '#242424')
    draw = ImageDraw.Draw(canvas)
    for col, mode in enumerate(('NON-X', 'X', 'BOOST')):
        draw.text((col*330+10, 12), f'ADVANCED / RECHARGE CTRL: {mode}', fill='white')
        canvas.paste(recharge_screen(mode), (col*330+5, 35))
    for col, mode in enumerate(('NORMAL', 'FREEZE', 'ECO')):
        draw.text((col*330+10, 300), f'SETTINGS / FLASH MODE: {mode}', fill='white')
        canvas.paste(flash_screen(mode), (col*330+5, 323))
    draw.text((10, 578), 'Reconstruction, not a device capture. Native row geometry; outer spacing illustrative.', fill='white')
    draw.text((10, 592), 'FLASH MODE panels omit unrelated rows. These images do not verify menu navigation or firmware behavior.', fill='white')
    return canvas


def error_preview():
    canvas = Image.new('RGB', (660, 185), '#242424')
    draw = ImageDraw.Draw(canvas)
    for index, mode in enumerate(('NON-X !', 'X !', 'BOOST !', 'ECO !')):
        col, row = index % 2, index // 2
        label = compose('RECHARGE CTRL') if index < 3 else asset(0x3a9ec)
        draw.text((10+330*col, 8+70*row), mode, fill='white')
        canvas.paste(menu_row(label, compose(mode)), (10+330*col, 26+70*row))
    draw.text((10, 160), 'Error-value row reconstruction; not a device capture.', fill='white')
    return canvas


if __name__ == '__main__':
    blob, meta = build_assets(0x080A0000)
    out = Path(__file__).resolve().parent.parent / "build"
    out.mkdir(parents=True, exist_ok=True)
    (out/'ui_assets_preview.bin').write_bytes(blob)
    (out/'ui_assets_preview.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    preview = Image.new('RGB', (900, len(meta)*85+20), '#222222')
    d = ImageDraw.Draw(preview)
    for i, text in enumerate(meta):
        im = compose(text)
        preview.paste(im.resize((im.width*3, im.height*3)), (15, i*85+12))
        d.text((550, i*85+25), f'{text}: {im.width} x {im.height}', fill='white')
    preview.save(out/'ui_assets_preview.png')
    menu_preview().save(out/'ui_menu_preview.png')
    error_preview().save(out/'ui_error_preview.png')
    # Exercise an unaligned relocation base as well as the CLI's aligned base.
    build_assets(0x080a0031)
    validation = dict(result='PASS', asset_count=len(meta),
                      round_trip_cases=len(meta)*2, pixel_comparison='exact',
                      relocation_bases=['0x080a0000', '0x080a0031'],
                      native_extra_glyphs={ch:hex(addr+0x08000000) for ch,addr in NATIVE_EXTRA_GLYPHS.items()},
                      home_glyph_sources=HOME_GLYPH_SOURCES,
                      home_badge_size=[64,24], home_capital_height=9,
                      resized_glyphs=['RECHARGE_HOME_' + text for text in HOME_PROFILE_TEXTS],
                      home_profile_size=[64,9],
                      home_profile_source='Cropped native D3 menu glyph raster, Lanczos to 9 px; requantized 4-bit grayscale.',
                      recharge_label_width=149,
                      max_recharge_value_width=max(meta[t]['human_wh'][0] for t in RECHARGE_VALUES),
                      min_label_value_gap=300-16-149-max(meta[t]['human_wh'][0] for t in RECHARGE_VALUES),
                      preview_is_device_capture=False)
    (out/'ui_assets_validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
    print(json.dumps(meta, indent=2))
    print(json.dumps(validation, indent=2))
