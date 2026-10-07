0800128a: 2330       adds      r0, #0x23
0800128c: 83ea1221   eor.w     r1, r3, r2, lsr #8
08001290: c943       mvns      r1, r1
08001292: c1f30720   ubfx      r0, r1, #8, #8
08001296: ef28       cmp       r0, #0xef
08001298: 84bf       itt       hi
0800129a: c043       mvnhi     r0, r0
0800129c: c0b2       uxtbhi    r0, r0
0800129e: 04f11c02   add.w     r2, r4, #0x1c
080012a2: 1368       ldr       r3, [r2]
080012a4: 1e06       lsls      r6, r3, #0x18
080012a6: fcd5       bpl       #0x80012a2
080012a8: c9b2       uxtb      r1, r1
080012aa: a062       str       r0, [r4, #0x28]
080012ac: ef29       cmp       r1, #0xef
080012ae: 6868       ldr       r0, [r5, #4]
080012b0: 84bf       itt       hi
080012b2: c943       mvnhi     r1, r1
080012b4: c9b2       uxtbhi    r1, r1
080012b6: 00f11c02   add.w     r2, r0, #0x1c
080012ba: 1368       ldr       r3, [r2]
080012bc: 1c06       lsls      r4, r3, #0x18
080012be: fcd5       bpl       #0x80012ba
080012c0: 8162       str       r1, [r0, #0x28]
080012c2: 6968       ldr       r1, [r5, #4]
080012c4: 01f11c02   add.w     r2, r1, #0x1c
080012c8: 1368       ldr       r3, [r2]
080012ca: 1b06       lsls      r3, r3, #0x18
080012cc: fcd5       bpl       #0x80012c8
080012ce: 66e6       b         #0x8000f9e
080012d0: d5f804c0   ldr.w     ip, [r5, #4]
080012d4: 0cf11c02   add.w     r2, ip, #0x1c
080012d8: 1368       ldr       r3, [r2]
080012da: 1b06       lsls      r3, r3, #0x18
080012dc: fcd5       bpl       #0x80012d8
080012de: 7be7       b         #0x80011d8
080012e0: 092d       cmp       r5, #9
080012e2: 7ff472ab   bne.w     #0x80009ca
080012e6: b1f90320   ldrsh.w   r2, [r1, #3]
080012ea: d1f80530   ldr.w     r3, [r1, #5]
080012ee: 0320       movs      r0, #3
080012f0: 86f87800   strb.w    r0, [r6, #0x78]
080012f4: c6f88420   str.w     r2, [r6, #0x84]
080012f8: 3046       mov       r0, r6
080012fa: c6f88030   str.w     r3, [r6, #0x80]
080012fe: 05f0c7f8   bl        #0x8006490
08001302: 1f4b       ldr       r3, [pc, #0x7c] ; [08001380]=100002a0
08001304: 0122       movs      r2, #1
08001306: 1a77       strb      r2, [r3, #0x1c]
08001308: fef781bf   b.w       #0x800020e
0800130c: 042d       cmp       r5, #4
0800130e: 7ff45cab   bne.w     #0x80009ca
08001312: cb78       ldrb      r3, [r1, #3]
08001314: 03b1       cbz       r3, #0x8001318
08001316: 0123       movs      r3, #1
08001318: 86f83830   strb.w    r3, [r6, #0x38]
0800131c: fef777bf   b.w       #0x800020e
