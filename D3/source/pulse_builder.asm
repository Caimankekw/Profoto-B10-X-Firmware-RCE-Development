0800705c: f0b5       push      {r4, r5, r6, r7, lr}
0800705e: 1446       mov       r4, r2
08007060: 99b0       sub       sp, #0x64
08007062: 3022       movs      r2, #0x30
08007064: 0deb0205   add.w     r5, sp, r2
08007068: 0646       mov       r6, r0
0800706a: 0f46       mov       r7, r1
0800706c: 6846       mov       r0, sp
0800706e: 4ff0ff31   mov.w     r1, #-1
08007072: 04f02bf8   bl        #0x800b0cc
08007076: 4ff0ff31   mov.w     r1, #-1
0800707a: 3022       movs      r2, #0x30
0800707c: 2846       mov       r0, r5
0800707e: 04f025f8   bl        #0x800b0cc
08007082: 2368       ldr       r3, [r4]
08007084: 6168       ldr       r1, [r4, #4]
08007086: e268       ldr       r2, [r4, #0xc]
08007088: 0193       str       r3, [sp, #4]
0800708a: 0020       movs      r0, #0
0800708c: 0b44       add       r3, r1
0800708e: 0121       movs      r1, #1
08007090: 0493       str       r3, [sp, #0x10]
08007092: 8df80000   strb.w    r0, [sp]
08007096: 8df80c10   strb.w    r1, [sp, #0xc]
0800709a: d4f808e0   ldr.w     lr, [r4, #8]
0800709e: 002a       cmp       r2, #0
080070a0: 7ed0       beq       #0x80071a0
080070a2: 638a       ldrh      r3, [r4, #0x12]
080070a4: adf83830   strh.w    r3, [sp, #0x38]
080070a8: 7244       add       r2, lr
080070aa: 0521       movs      r1, #5
080070ac: 1092       str       r2, [sp, #0x40]
080070ae: adf84430   strh.w    r3, [sp, #0x44]
080070b2: 8df83c10   strb.w    r1, [sp, #0x3c]
080070b6: 0324       movs      r4, #3
080070b8: 6846       mov       r0, sp
080070ba: 0421       movs      r1, #4
080070bc: 0c22       movs      r2, #0xc
080070be: 3b4b       ldr       r3, [pc, #0xec] ; [080071ac]=08006f31
080070c0: cdf834e0   str.w     lr, [sp, #0x34]
080070c4: 8df83040   strb.w    r4, [sp, #0x30]
080070c8: 03f0acfe   bl        #0x800ae24
080070cc: 0c22       movs      r2, #0xc
080070ce: 374b       ldr       r3, [pc, #0xdc] ; [080071ac]=08006f31
080070d0: 2846       mov       r0, r5
080070d2: 0421       movs      r1, #4
080070d4: 03f0a6fe   bl        #0x800ae24
080070d8: 0d9b       ldr       r3, [sp, #0x34]
080070da: 5a1c       adds      r2, r3, #1
080070dc: 62d0       beq       #0x80071a4
080070de: 109b       ldr       r3, [sp, #0x40]
080070e0: 0133       adds      r3, #1
080070e2: 61d0       beq       #0x80071a8
080070e4: 139b       ldr       r3, [sp, #0x4c]
080070e6: 0133       adds      r3, #1
080070e8: 14bf       ite       ne
080070ea: 0322       movne     r2, #3
080070ec: 0222       moveq     r2, #2
080070ee: 531e       subs      r3, r2, #1
080070f0: 18a9       add       r1, sp, #0x60
080070f2: 03eb4303   add.w     r3, r3, r3, lsl #1
080070f6: 01eb8303   add.w     r3, r1, r3, lsl #2
080070fa: 18ac       add       r4, sp, #0x60
080070fc: 53f82c0c   ldr       r0, [r3, #-0x2c]
08007100: 2b49       ldr       r1, [pc, #0xac] ; [080071b0]=40010400
08007102: 2c4b       ldr       r3, [pc, #0xb0] ; [080071b4]=40010404
08007104: 02eb4202   add.w     r2, r2, r2, lsl #1
08007108: 04eb8202   add.w     r2, r4, r2, lsl #2
0800710c: 0130       adds      r0, #1
0800710e: 42f82c0c   str       r0, [r2, #-0x2c]
08007112: 0868       ldr       r0, [r1]
08007114: 0524       movs      r4, #5
08007116: 20f48050   bic       r0, r0, #0x1000
0800711a: 02f8304c   strb      r4, [r2, #-0x30]
0800711e: 0860       str       r0, [r1]
08007120: 1a68       ldr       r2, [r3]
08007122: 22f48052   bic       r2, r2, #0x1000
08007126: 1a60       str       r2, [r3]
08007128: 0a68       ldr       r2, [r1]
0800712a: 22f40062   bic       r2, r2, #0x800
0800712e: 0a60       str       r2, [r1]
08007130: 1a68       ldr       r2, [r3]
08007132: 22f40062   bic       r2, r2, #0x800
08007136: 1a60       str       r2, [r3]
08007138: 0a68       ldr       r2, [r1]
0800713a: 22f08002   bic       r2, r2, #0x80
0800713e: 0a60       str       r2, [r1]
08007140: 1a68       ldr       r2, [r3]
08007142: 22f08002   bic       r2, r2, #0x80
08007146: 1a60       str       r2, [r3]
08007148: 0a68       ldr       r2, [r1]
0800714a: 22f04002   bic       r2, r2, #0x40
0800714e: 0a60       str       r2, [r1]
08007150: 1a68       ldr       r2, [r3]
08007152: 22f04002   bic       r2, r2, #0x40
08007156: 1a60       str       r2, [r3]
08007158: 0a68       ldr       r2, [r1]
0800715a: 22f00402   bic       r2, r2, #4
0800715e: 0a60       str       r2, [r1]
08007160: 1a68       ldr       r2, [r3]
08007162: 22f00402   bic       r2, r2, #4
08007166: ee46       mov       lr, sp
08007168: 1a60       str       r2, [r3]
0800716a: 7446       mov       r4, lr
0800716c: 0fcc       ldm       r4!, {r0, r1, r2, r3}
0800716e: ac42       cmp       r4, r5
08007170: 3060       str       r0, [r6]
08007172: 7160       str       r1, [r6, #4]
08007174: b260       str       r2, [r6, #8]
08007176: f360       str       r3, [r6, #0xc]
08007178: a646       mov       lr, r4
0800717a: 06f11006   add.w     r6, r6, #0x10
0800717e: f4d1       bne       #0x800716a
08007180: 18ae       add       r6, sp, #0x60
08007182: 2c46       mov       r4, r5
08007184: 0fcc       ldm       r4!, {r0, r1, r2, r3}
08007186: b442       cmp       r4, r6
08007188: 3860       str       r0, [r7]
0800718a: 7960       str       r1, [r7, #4]
0800718c: ba60       str       r2, [r7, #8]
0800718e: fb60       str       r3, [r7, #0xc]
08007190: 2546       mov       r5, r4
08007192: 07f11007   add.w     r7, r7, #0x10
08007196: f4d1       bne       #0x8007182
08007198: 02f052f8   bl        #0x8009240
0800719c: 19b0       add       sp, #0x64
0800719e: f0bd       pop       {r4, r5, r6, r7, pc}
080071a0: 0524       movs      r4, #5
080071a2: 89e7       b         #0x80070b8
080071a4: 0022       movs      r2, #0
080071a6: a3e7       b         #0x80070f0
080071a8: 0122       movs      r2, #1
080071aa: a0e7       b         #0x80070ee
080071ac: 316f       ldr       r1, [r6, #0x70]
080071ae: 0008       lsrs      r0, r0, #0x20
080071b0: 0004       lsls      r0, r0, #0x10
080071b2: 0140       ands      r1, r0
080071b4: 0404       lsls      r4, r0, #0x10
080071b6: 0140       ands      r1, r0
080071b8: 2de9f043   push.w    {r4, r5, r6, r7, r8, sb, lr}
080071bc: d04c       ldr       r4, [pc, #0x340] ; [08007500]=100006e0
080071be: d149       ldr       r1, [pc, #0x344] ; [08007504]=100004cc
080071c0: d4e90067   ldrd      r6, r7, [r4]
080071c4: 0b88       ldrh      r3, [r1]
080071c6: f21a       subs      r2, r6, r3
080071c8: 92b2       uxth      r2, r2
080071ca: 632a       cmp       r2, #0x63
080071cc: 83b0       sub       sp, #0xc
080071ce: 02d8       bhi       #0x80071d6
080071d0: 03b0       add       sp, #0xc
080071d2: bde8f083   pop.w     {r4, r5, r6, r7, r8, sb, pc}
080071d6: d1ed0c7a   vldr      s15, [r1, #0x30]
080071da: ce68       ldr       r6, [r1, #0xc]
080071dc: 4d68       ldr       r5, [r1, #4]
080071de: 0f69       ldr       r7, [r1, #0x10]
080071e0: d4e90089   ldrd      r8, sb, [r4]
080071e4: f8eee77a   vcvt.f32.s32 s15, s15
080071e8: c36c       ldr       r3, [r0, #0x4c]
080071ea: 90ed147a   vldr      s14, [r0, #0x50]
080071ee: a1f80080   strh.w    r8, [r1]
080071f2: b4eee77a   vcmpe.f32 s14, s15
080071f6: f1ee10fa   vmrs      apsr_nzcv, fpscr
080071fa: c6eb050e   rsb       lr, r6, r5
080071fe: 5bd8       bhi       #0x80072b8
08007200: 3b46       mov       r3, r7
08007202: d1ed107a   vldr      s15, [r1, #0x40]
08007206: 90ed157a   vldr      s14, [r0, #0x54]
0800720a: be4a       ldr       r2, [pc, #0x2f8] ; [08007504]=100004cc
0800720c: f8eee77a   vcvt.f32.s32 s15, s15
08007210: b4eee77a   vcmpe.f32 s14, s15
08007214: f1ee10fa   vmrs      apsr_nzcv, fpscr
08007218: 00f27a81   bhi.w     #0x8007510
0800721c: bb42       cmp       r3, r7
0800721e: b8bf       it        lt
08007220: 3b46       movlt     r3, r7
08007222: 1a46       mov       r2, r3
08007224: d1ed147a   vldr      s15, [r1, #0x50]
08007228: 90ed167a   vldr      s14, [r0, #0x58]
0800722c: b54b       ldr       r3, [pc, #0x2d4] ; [08007504]=100004cc
0800722e: f8eee77a   vcvt.f32.s32 s15, s15
08007232: b4eee77a   vcmpe.f32 s14, s15
08007236: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800723a: 00f22e81   bhi.w     #0x800749a
0800723e: 9742       cmp       r7, r2
08007240: 3b46       mov       r3, r7
08007242: b8bf       it        lt
08007244: 1346       movlt     r3, r2
08007246: 1d46       mov       r5, r3
08007248: 91ed187a   vldr      s14, [r1, #0x60]
0800724c: 4562       str       r5, [r0, #0x24]
0800724e: ae4e       ldr       r6, [pc, #0x2b8] ; [08007508]=10000080
08007250: d0ed137a   vldr      s15, [r0, #0x4c]
08007254: b568       ldr       r5, [r6, #8]
08007256: 3768       ldr       r7, [r6]
08007258: 7268       ldr       r2, [r6, #4]
0800725a: dff8a8e2   ldr.w     lr, [pc, #0x2a8] ; [08007504]=100004cc
0800725e: b8eec77a   vcvt.f32.s32 s14, s14
08007262: c5eb0708   rsb       r8, r5, r7
08007266: f4eec77a   vcmpe.f32 s15, s14
0800726a: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800726e: 80f2a282   bge.w     #0x80077b6
08007272: def85430   ldr.w     r3, [lr, #0x54]
08007276: 07ee103a   vmov      s14, r3
0800727a: f8eec76a   vcvt.f32.s32 s13, s14
0800727e: f4eee67a   vcmpe.f32 s15, s13
08007282: f1ee10fa   vmrs      apsr_nzcv, fpscr
08007286: 49da       bge       #0x800731c
08007288: def85cc0   ldr.w     ip, [lr, #0x5c]
0800728c: 07ee10ca   vmov      s14, ip
08007290: b8eec77a   vcvt.f32.s32 s14, s14
08007294: f4eec77a   vcmpe.f32 s15, s14
08007298: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800729c: 80f26d81   bge.w     #0x800757a
080072a0: 9eed167a   vldr      s14, [lr, #0x58]
080072a4: b8eec77a   vcvt.f32.s32 s14, s14
080072a8: f4eec77a   vcmpe.f32 s15, s14
080072ac: f1ee10fa   vmrs      apsr_nzcv, fpscr
080072b0: c0f2d981   blt.w     #0x8007666
080072b4: 2b46       mov       r3, r5
080072b6: 35e0       b         #0x8007324
080072b8: ca6a       ldr       r2, [r1, #0x2c]
080072ba: 07ee902a   vmov      s15, r2
080072be: f8eee77a   vcvt.f32.s32 s15, s15
080072c2: b4eee77a   vcmpe.f32 s14, s15
080072c6: f1ee10fa   vmrs      apsr_nzcv, fpscr
080072ca: 40f2c781   bls.w     #0x800765c
080072ce: 4b6a       ldr       r3, [r1, #0x24]
080072d0: 06ee903a   vmov      s13, r3
080072d4: f8eee66a   vcvt.f32.s32 s13, s13
080072d8: b4eee67a   vcmpe.f32 s14, s13
080072dc: f1ee10fa   vmrs      apsr_nzcv, fpscr
080072e0: b2d8       bhi       #0x8007248
080072e2: 06ee90ea   vmov      s13, lr
080072e6: 9b1a       subs      r3, r3, r2
080072e8: 37ee677a   vsub.f32  s14, s14, s15
080072ec: f8eee66a   vcvt.f32.s32 s13, s13
080072f0: 07ee903a   vmov      s15, r3
080072f4: 26ee877a   vmul.f32  s14, s13, s14
080072f8: f8eee77a   vcvt.f32.s32 s15, s15
080072fc: 87ee277a   vdiv.f32  s14, s14, s15
08007300: 07ee906a   vmov      s15, r6
08007304: f8eee77a   vcvt.f32.s32 s15, s15
08007308: 77ee877a   vadd.f32  s15, s15, s14
0800730c: fdeee77a   vcvt.s32.f32 s15, s15
08007310: 17ee903a   vmov      r3, s15
08007314: bb42       cmp       r3, r7
08007316: b8bf       it        lt
08007318: 3b46       movlt     r3, r7
0800731a: 72e7       b         #0x8007202
0800731c: bd42       cmp       r5, r7
0800731e: 2b46       mov       r3, r5
08007320: a8bf       it        ge
08007322: 3b46       movge     r3, r7
08007324: 91ed1c7a   vldr      s14, [r1, #0x70]
08007328: d0ed147a   vldr      s15, [r0, #0x50]
0800732c: dff8d4c1   ldr.w     ip, [pc, #0x1d4] ; [08007504]=100004cc
08007330: b8eec77a   vcvt.f32.s32 s14, s14
08007334: b4eee77a   vcmpe.f32 s14, s15
08007338: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800733c: 40f23b82   bls.w     #0x80077b6
08007340: dcf864e0   ldr.w     lr, [ip, #0x64]
08007344: 07ee10ea   vmov      s14, lr
08007348: b8eec77a   vcvt.f32.s32 s14, s14
0800734c: b4eee77a   vcmpe.f32 s14, s15
08007350: f1ee10fa   vmrs      apsr_nzcv, fpscr
08007354: 19d9       bls       #0x800738a
08007356: dcf86c90   ldr.w     sb, [ip, #0x6c]
0800735a: 07ee109a   vmov      s14, sb
0800735e: b8eec77a   vcvt.f32.s32 s14, s14
08007362: b4eee77a   vcmpe.f32 s14, s15
08007366: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800736a: 40f22481   bls.w     #0x80075b6
0800736e: 9ced1a7a   vldr      s14, [ip, #0x68]
08007372: b8eec77a   vcvt.f32.s32 s14, s14
08007376: b4eee77a   vcmpe.f32 s14, s15
0800737a: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800737e: 00f27781   bhi.w     #0x8007670
08007382: ab42       cmp       r3, r5
08007384: a8bf       it        ge
08007386: 2b46       movge     r3, r5
08007388: 02e0       b         #0x8007390
0800738a: bb42       cmp       r3, r7
0800738c: a8bf       it        ge
0800738e: 3b46       movge     r3, r7
08007390: 91ed207a   vldr      s14, [r1, #0x80]
08007394: d0ed157a   vldr      s15, [r0, #0x54]
08007398: dff868c1   ldr.w     ip, [pc, #0x168] ; [08007504]=100004cc
0800739c: b8eec77a   vcvt.f32.s32 s14, s14
080073a0: b4eee77a   vcmpe.f32 s14, s15
080073a4: f1ee10fa   vmrs      apsr_nzcv, fpscr
080073a8: 40f20582   bls.w     #0x80077b6
080073ac: dcf874e0   ldr.w     lr, [ip, #0x74]
080073b0: 07ee10ea   vmov      s14, lr
080073b4: b8eec77a   vcvt.f32.s32 s14, s14
080073b8: b4eee77a   vcmpe.f32 s14, s15
080073bc: f1ee10fa   vmrs      apsr_nzcv, fpscr
080073c0: 19d9       bls       #0x80073f6
080073c2: dcf87c90   ldr.w     sb, [ip, #0x7c]
080073c6: 07ee109a   vmov      s14, sb
080073ca: b8eec77a   vcvt.f32.s32 s14, s14
080073ce: b4eee77a   vcmpe.f32 s14, s15
080073d2: f1ee10fa   vmrs      apsr_nzcv, fpscr
080073d6: 40f20c81   bls.w     #0x80075f2
080073da: 9ced1e7a   vldr      s14, [ip, #0x78]
080073de: b8eec77a   vcvt.f32.s32 s14, s14
080073e2: b4eee77a   vcmpe.f32 s14, s15
080073e6: f1ee10fa   vmrs      apsr_nzcv, fpscr
080073ea: 00f24581   bhi.w     #0x8007678
080073ee: ab42       cmp       r3, r5
080073f0: a8bf       it        ge
080073f2: 2b46       movge     r3, r5
080073f4: 02e0       b         #0x80073fc
080073f6: bb42       cmp       r3, r7
080073f8: a8bf       it        ge
080073fa: 3b46       movge     r3, r7
080073fc: 91ed247a   vldr      s14, [r1, #0x90]
08007400: d0ed167a   vldr      s15, [r0, #0x58]
08007404: dff8fce0   ldr.w     lr, [pc, #0xfc] ; [08007504]=100004cc
08007408: b8eec77a   vcvt.f32.s32 s14, s14
0800740c: f4eec77a   vcmpe.f32 s15, s14
08007410: f1ee10fa   vmrs      apsr_nzcv, fpscr
08007414: 80f2cf81   bge.w     #0x80077b6
08007418: def88410   ldr.w     r1, [lr, #0x84]
0800741c: 07ee101a   vmov      s14, r1
08007420: b8eec77a   vcvt.f32.s32 s14, s14
08007424: f4eec77a   vcmpe.f32 s15, s14
08007428: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800742c: 0cdb       blt       #0x8007448
0800742e: bb42       cmp       r3, r7
08007430: a8bf       it        ge
08007432: 3b46       movge     r3, r7
08007434: 354a       ldr       r2, [pc, #0xd4] ; [0800750c]=100003f8
08007436: 92f84710   ldrb.w    r1, [r2, #0x47]
0800743a: 0029       cmp       r1, #0
0800743c: 40f02481   bne.w     #0x8007688
08007440: 8362       str       r3, [r0, #0x28]
08007442: 03b0       add       sp, #0xc
08007444: bde8f083   pop.w     {r4, r5, r6, r7, r8, sb, pc}
08007448: def88c60   ldr.w     r6, [lr, #0x8c]
0800744c: 07ee106a   vmov      s14, r6
08007450: b8eec77a   vcvt.f32.s32 s14, s14
08007454: f4eec77a   vcmpe.f32 s15, s14
08007458: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800745c: c0f2e780   blt.w     #0x800762e
08007460: 77eec77a   vsub.f32  s15, s15, s14
08007464: 07ee108a   vmov      s14, r8
08007468: b8eec77a   vcvt.f32.s32 s14, s14
0800746c: 891b       subs      r1, r1, r6
0800746e: 27ee277a   vmul.f32  s14, s14, s15
08007472: 07ee901a   vmov      s15, r1
08007476: f8eee77a   vcvt.f32.s32 s15, s15
0800747a: 06ee905a   vmov      s13, r5
0800747e: c7ee277a   vdiv.f32  s15, s14, s15
08007482: f8eee66a   vcvt.f32.s32 s13, s13
08007486: 76eea77a   vadd.f32  s15, s13, s15
0800748a: fdeee77a   vcvt.s32.f32 s15, s15
0800748e: 17ee902a   vmov      r2, s15
08007492: 9342       cmp       r3, r2
08007494: a8bf       it        ge
08007496: 1346       movge     r3, r2
08007498: cce7       b         #0x8007434
0800749a: df6c       ldr       r7, [r3, #0x4c]
0800749c: 07ee907a   vmov      s15, r7
080074a0: f8eee77a   vcvt.f32.s32 s15, s15
080074a4: b4eee77a   vcmpe.f32 s14, s15
080074a8: f1ee10fa   vmrs      apsr_nzcv, fpscr
080074ac: 40f2d180   bls.w     #0x8007652
080074b0: 5b6c       ldr       r3, [r3, #0x44]
080074b2: 06ee903a   vmov      s13, r3
080074b6: f8eee66a   vcvt.f32.s32 s13, s13
080074ba: b4eee67a   vcmpe.f32 s14, s13
080074be: f1ee10fa   vmrs      apsr_nzcv, fpscr
080074c2: 3ff6c1ae   bhi.w     #0x8007248
080074c6: 37ee677a   vsub.f32  s14, s14, s15
080074ca: 07ee90ea   vmov      s15, lr
080074ce: db1b       subs      r3, r3, r7
080074d0: f8eee76a   vcvt.f32.s32 s13, s15
080074d4: 07ee903a   vmov      s15, r3
080074d8: 26ee877a   vmul.f32  s14, s13, s14
080074dc: f8eee77a   vcvt.f32.s32 s15, s15
080074e0: 06ee906a   vmov      s13, r6
080074e4: c7ee277a   vdiv.f32  s15, s14, s15
080074e8: f8eee66a   vcvt.f32.s32 s13, s13
080074ec: 76eea77a   vadd.f32  s15, s13, s15
080074f0: fdeee77a   vcvt.s32.f32 s15, s15
080074f4: 17ee903a   vmov      r3, s15
080074f8: 9342       cmp       r3, r2
080074fa: b8bf       it        lt
080074fc: 1346       movlt     r3, r2
080074fe: a2e6       b         #0x8007246
08007500: e006       lsls      r0, r4, #0x1b
08007502: 0010       asrs      r0, r0, #0x20
08007504: cc04       lsls      r4, r1, #0x13
08007506: 0010       asrs      r0, r0, #0x20
08007508: 8000       lsls      r0, r0, #2
0800750a: 0010       asrs      r0, r0, #0x20
0800750c: f803       lsls      r0, r7, #0xf
0800750e: 0010       asrs      r0, r0, #0x20
08007510: d2f83cc0   ldr.w     ip, [r2, #0x3c]
08007514: 07ee90ca   vmov      s15, ip
08007518: f8eee77a   vcvt.f32.s32 s15, s15
0800751c: b4eee77a   vcmpe.f32 s14, s15
08007520: f1ee10fa   vmrs      apsr_nzcv, fpscr
08007524: 40f29080   bls.w     #0x8007648
08007528: 526b       ldr       r2, [r2, #0x34]
0800752a: 06ee902a   vmov      s13, r2
0800752e: f8eee66a   vcvt.f32.s32 s13, s13
08007532: b4eee67a   vcmpe.f32 s14, s13
08007536: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800753a: 3ff685ae   bhi.w     #0x8007248
0800753e: 06ee90ea   vmov      s13, lr
08007542: cceb0202   rsb       r2, ip, r2
08007546: 37ee677a   vsub.f32  s14, s14, s15
0800754a: f8eee66a   vcvt.f32.s32 s13, s13
0800754e: 07ee902a   vmov      s15, r2
08007552: 26ee877a   vmul.f32  s14, s13, s14
08007556: f8eee77a   vcvt.f32.s32 s15, s15
0800755a: 87ee277a   vdiv.f32  s14, s14, s15
0800755e: 07ee906a   vmov      s15, r6
08007562: f8eee77a   vcvt.f32.s32 s15, s15
08007566: 77ee877a   vadd.f32  s15, s15, s14
0800756a: fdeee77a   vcvt.s32.f32 s15, s15
0800756e: 17ee902a   vmov      r2, s15
08007572: 9a42       cmp       r2, r3
08007574: b8bf       it        lt
08007576: 1a46       movlt     r2, r3
08007578: 54e6       b         #0x8007224
0800757a: 77eec77a   vsub.f32  s15, s15, s14
0800757e: 07ee108a   vmov      s14, r8
08007582: cceb0303   rsb       r3, ip, r3
08007586: f8eec76a   vcvt.f32.s32 s13, s14
0800758a: 07ee103a   vmov      s14, r3
0800758e: 66eea77a   vmul.f32  s15, s13, s15
08007592: f8eec76a   vcvt.f32.s32 s13, s14
08007596: c7eea66a   vdiv.f32  s13, s15, s13
0800759a: 07ee905a   vmov      s15, r5
0800759e: b8eee76a   vcvt.f32.s32 s12, s15
080075a2: 76ee266a   vadd.f32  s13, s12, s13
080075a6: fdeee67a   vcvt.s32.f32 s15, s13
080075aa: 17ee903a   vmov      r3, s15
080075ae: ab42       cmp       r3, r5
080075b0: a8bf       it        ge
080075b2: 2b46       movge     r3, r5
080075b4: b6e6       b         #0x8007324
080075b6: 77eec77a   vsub.f32  s15, s15, s14
080075ba: 07ee108a   vmov      s14, r8
080075be: c9eb0e0e   rsb       lr, sb, lr
080075c2: f8eec76a   vcvt.f32.s32 s13, s14
080075c6: 07ee10ea   vmov      s14, lr
080075ca: 66eea77a   vmul.f32  s15, s13, s15
080075ce: f8eec76a   vcvt.f32.s32 s13, s14
080075d2: c7eea66a   vdiv.f32  s13, s15, s13
080075d6: 07ee905a   vmov      s15, r5
080075da: b8eee77a   vcvt.f32.s32 s14, s15
080075de: 77ee       .byte     0x77, 0xee
