08006490: 2de9f043   push.w    {r4, r5, r6, r7, r8, sb, lr}
08006494: 90f87830   ldrb.w    r3, [r0, #0x78]
08006498: 2ded028b   vpush     {d8}
0800649c: 032b       cmp       r3, #3
0800649e: 83b0       sub       sp, #0xc
080064a0: 0446       mov       r4, r0
080064a2: 00f08c80   beq.w     #0x80065be
080064a6: 90f87830   ldrb.w    r3, [r0, #0x78]
080064aa: 012b       cmp       r3, #1
080064ac: 1cd0       beq       #0x80064e8
080064ae: 90f87830   ldrb.w    r3, [r0, #0x78]
080064b2: 022b       cmp       r3, #2
080064b4: 18d0       beq       #0x80064e8
080064b6: c64d       ldr       r5, [pc, #0x318] ; [080067d0]=100004b4
080064b8: c64b       ldr       r3, [pc, #0x318] ; [080067d4]=100006e0
080064ba: c74e       ldr       r6, [pc, #0x31c] ; [080067d8]=100003a9
080064bc: c749       ldr       r1, [pc, #0x31c] ; [080067dc]=1000033c
080064be: d3e90023   ldrd      r2, r3, [r3]
080064c2: 94f87830   ldrb.w    r3, [r4, #0x78]
080064c6: 02f51c52   add.w     r2, r2, #0x2700
080064ca: 1032       adds      r2, #0x10
080064cc: 0120       movs      r0, #1
080064ce: a3f10303   sub.w     r3, r3, #3
080064d2: b3fa83f3   clz       r3, r3
080064d6: 5b09       lsrs      r3, r3, #5
080064d8: 6a61       str       r2, [r5, #0x14]
080064da: 3370       strb      r3, [r6]
080064dc: 0870       strb      r0, [r1]
080064de: 03b0       add       sp, #0xc
080064e0: bdec028b   vpop      {d8}
080064e4: bde8f083   pop.w     {r4, r5, r6, r7, r8, sb, pc}
080064e8: 94f87820   ldrb.w    r2, [r4, #0x78]
080064ec: b84d       ldr       r5, [pc, #0x2e0] ; [080067d0]=100004b4
080064ee: e36f       ldr       r3, [r4, #0x7c]
080064f0: 4ff44871   mov.w     r1, #0x320
080064f4: 1e20       movs      r0, #0x1e
080064f6: 012a       cmp       r2, #1
080064f8: 85e80300   stm.w     r5, {r0, r1}
080064fc: b849       ldr       r1, [pc, #0x2e0] ; [080067e0]=100003f8
080064fe: 47d0       beq       #0x8006590
08006500: b84a       ldr       r2, [pc, #0x2e0] ; [080067e4]=0800b410 ','
08006502: 91f86400   ldrb.w    r0, [r1, #0x64]
08006506: 02f59661   add.w     r1, r2, #0x4b0
0800650a: 8d28       cmp       r0, #0x8d
0800650c: 08bf       it        eq
0800650e: 1146       moveq     r1, r2
08006510: 642b       cmp       r3, #0x64
08006512: 3ad8       bhi       #0x800658a
08006514: 1bb1       cbz       r3, #0x800651e
08006516: 013b       subs      r3, #1
08006518: 03eb4303   add.w     r3, r3, r3, lsl #1
0800651c: 9b00       lsls      r3, r3, #2
0800651e: c818       adds      r0, r1, r3
08006520: 40f63512   movw      r2, #0x935
08006524: 067a       ldrb      r6, [r0, #8]
08006526: cb58       ldr       r3, [r1, r3]
08006528: ab60       str       r3, [r5, #8]
0800652a: 02fb06f3   mul       r3, r2, r6
0800652e: 4168       ldr       r1, [r0, #4]
08006530: e960       str       r1, [r5, #0xc]
08006532: 1b12       asrs      r3, r3, #8
08006534: 6b82       strh      r3, [r5, #0x12]
08006536: ac48       ldr       r0, [pc, #0x2b0] ; [080067e8]=100002c8
08006538: ac49       ldr       r1, [pc, #0x2b0] ; [080067ec]=100002fc
0800653a: a54a       ldr       r2, [pc, #0x294] ; [080067d0]=100004b4
0800653c: 00f08efd   bl        #0x800705c
08006540: 94f87830   ldrb.w    r3, [r4, #0x78]
08006544: 022b       cmp       r3, #2
08006546: 03d0       beq       #0x8006550
08006548: 94f87830   ldrb.w    r3, [r4, #0x78]
0800654c: 012b       cmp       r3, #1
0800654e: b3d1       bne       #0x80064b8
08006550: e36f       ldr       r3, [r4, #0x7c]
08006552: a74a       ldr       r2, [pc, #0x29c] ; [080067f0]=10000074
08006554: 9fedbd7a   vldr      s14, [pc, #0x2f4] ; [0800684c]=3dcccccd
08006558: 92ed028a   vldr      s16, [r2, #8]
0800655c: 5bb2       sxtb      r3, r3
0800655e: 07ee903a   vmov      s15, r3
08006562: f8eee77a   vcvt.f32.s32 s15, s15
08006566: faee040a   vmov.f32  s1, #-1.000000e+01
0800656a: e7ee870a   vfma.f32  s1, s15, s14
0800656e: b0ee000a   vmov.f32  s0, #2.000000e+00
08006572: 02f0f1f9   bl        #0x8008958
08006576: b8ee488a   vcvt.f32.u32 s16, s16
0800657a: 9e4b       ldr       r3, [pc, #0x278] ; [080067f4]=10000014
0800657c: 28ee000a   vmul.f32  s0, s16, s0
08006580: bceec00a   vcvt.u32.f32 s0, s0
08006584: 83ed000a   vstr      s0, [r3]
08006588: 96e7       b         #0x80064b8
0800658a: 40f2a443   movw      r3, #0x4a4
0800658e: c6e7       b         #0x800651e
08006590: 994a       ldr       r2, [pc, #0x264] ; [080067f8]=0800b0f0
08006592: 91f86400   ldrb.w    r0, [r1, #0x64]
08006596: 02f5c871   add.w     r1, r2, #0x190
0800659a: 8d28       cmp       r0, #0x8d
0800659c: 18bf       it        ne
0800659e: 0a46       movne     r2, r1
080065a0: 642b       cmp       r3, #0x64
080065a2: 00f20381   bhi.w     #0x80067ac
080065a6: 002b       cmp       r3, #0
080065a8: 00f00981   beq.w     #0x80067be
080065ac: 03f18043   add.w     r3, r3, #0x40000000
080065b0: 013b       subs      r3, #1
080065b2: 52f82330   ldr.w     r3, [r2, r3, lsl #2]
080065b6: ab60       str       r3, [r5, #8]
080065b8: 0023       movs      r3, #0
080065ba: eb60       str       r3, [r5, #0xc]
080065bc: bbe7       b         #0x8006536
080065be: d0f88430   ldr.w     r3, [r0, #0x84]
080065c2: d0f88050   ldr.w     r5, [r0, #0x80]
080065c6: 002d       cmp       r5, #0
080065c8: 40f04281   bne.w     #0x8006850
080065cc: 8b4f       ldr       r7, [pc, #0x22c] ; [080067fc]=10000704
080065ce: d4f88030   ldr.w     r3, [r4, #0x80]
080065d2: 41f65831   movw      r1, #0x1b58
080065d6: 03f5fa63   add.w     r3, r3, #0x7d0
080065da: 8b42       cmp       r3, r1
080065dc: 19d9       bls       #0x8006612
080065de: b3f5fa5f   cmp.w     r3, #0x1f40
080065e2: 40f25b81   bls.w     #0x800689c
080065e6: 42f6e061   movw      r1, #0x2ee0
080065ea: 8b42       cmp       r3, r1
080065ec: 11d9       bls       #0x8006612
080065ee: b3f57a5f   cmp.w     r3, #0x3e80
080065f2: 40f26481   bls.w     #0x80068be
080065f6: 45f6c051   movw      r1, #0x5dc0
080065fa: 8b42       cmp       r3, r1
080065fc: 09d9       bls       #0x8006612
080065fe: 48f6a041   movw      r1, #0x8ca0
08006602: 8b42       cmp       r3, r1
08006604: 05d9       bls       #0x8006612
08006606: b3f57a4f   cmp.w     r3, #0xfa00
0800660a: 7d49       ldr       r1, [pc, #0x1f4] ; [08006800]=00017700
0800660c: 98bf       it        ls
0800660e: 4ff47a41   movls.w   r1, #0xfa00
08006612: d7f80480   ldr.w     r8, [r7, #4]
08006616: 794b       ldr       r3, [pc, #0x1e4] ; [080067fc]=10000704
08006618: b8f1010f   cmp.w     r8, #1
0800661c: 40f24181   bls.w     #0x80068a2
08006620: 1b68       ldr       r3, [r3]
08006622: 9e68       ldr       r6, [r3, #8]
08006624: d3f800c0   ldr.w     ip, [r3]
08006628: da68       ldr       r2, [r3, #0xc]
0800662a: d3f804e0   ldr.w     lr, [r3, #4]
0800662e: 4ff47a79   mov.w     sb, #0x3e8
08006632: 09fb06f6   mul       r6, sb, r6
08006636: b142       cmp       r1, r6
08006638: 10d9       bls       #0x800665c
0800663a: 0120       movs      r0, #1
0800663c: 0130       adds      r0, #1
0800663e: 4045       cmp       r0, r8
08006640: 00f02f81   beq.w     #0x80068a2
08006644: 1e69       ldr       r6, [r3, #0x10]
08006646: d3f808c0   ldr.w     ip, [r3, #8]
0800664a: 5a69       ldr       r2, [r3, #0x14]
0800664c: d3f80ce0   ldr.w     lr, [r3, #0xc]
08006650: 09fb06f6   mul       r6, sb, r6
08006654: 8e42       cmp       r6, r1
08006656: 03f10803   add.w     r3, r3, #8
0800665a: efd3       blo       #0x800663c
0800665c: 4ff47a73   mov.w     r3, #0x3e8
08006660: 03fb0cf3   mul       r3, r3, ip
08006664: c91a       subs      r1, r1, r3
08006666: f61a       subs      r6, r6, r3
08006668: 02fb01f2   mul       r2, r2, r1
0800666c: b2fbf6f2   udiv      r2, r2, r6
08006670: 7244       add       r2, lr
08006672: 0efb01f1   mul       r1, lr, r1
08006676: b1fbf6f6   udiv      r6, r1, r6
0800667a: 931b       subs      r3, r2, r6
0800667c: 00ee103a   vmov      s0, r3
08006680: b8ee408a   vcvt.f32.u32 s16, s0
08006684: 564b       ldr       r3, [pc, #0x158] ; [080067e0]=100003f8
08006686: dfed5f0a   vldr      s1, [pc, #0x17c] ; [08006804]=3c23d70a
0800668a: d3ed1d7a   vldr      s15, [r3, #0x74]
0800668e: f8eee77a   vcvt.f32.s32 s15, s15
08006692: b0ee000a   vmov.f32  s0, #2.000000e+00
08006696: 67eea00a   vmul.f32  s1, s15, s1
0800669a: 02f05df9   bl        #0x8008958
0800669e: 20ee080a   vmul.f32  s0, s0, s16
080066a2: bb68       ldr       r3, [r7, #8]
080066a4: 584f       ldr       r7, [pc, #0x160] ; [08006808]=39d1b717
080066a6: bceec00a   vcvt.u32.f32 s0, s0
080066aa: 9d42       cmp       r5, r3
080066ac: b8bf       it        lt
080066ae: 1d46       movlt     r5, r3
080066b0: 10ee103a   vmov      r3, s0
080066b4: ab42       cmp       r3, r5
080066b6: a8bf       it        ge
080066b8: 2b46       movge     r3, r5
080066ba: 00ee103a   vmov      s0, r3
080066be: b8eec08a   vcvt.f32.s32 s16, s0
080066c2: 524d       ldr       r5, [pc, #0x148] ; [0800680c]=1000049c
080066c4: fceec87a   vcvt.u32.f32 s15, s16
080066c8: 17ee900a   vmov      r0, s15
080066cc: 17ee906a   vmov      r6, s15
080066d0: 00f03afc   bl        #0x8006f48
080066d4: 4e49       ldr       r1, [pc, #0x138] ; [08006810]=10000004
080066d6: 4f4a       ldr       r2, [pc, #0x13c] ; [08006814]=10000000
080066d8: 4f4b       ldr       r3, [pc, #0x13c] ; [08006818]=100004a4
080066da: d2ed008a   vldr      s17, [r2]
080066de: d1ed000a   vldr      s1, [r1]
080066e2: 07ee900a   vmov      s15, r0
080066e6: 0022       movs      r2, #0
080066e8: b0ee480a   vmov.f32  s0, s16
080066ec: 1a70       strb      r2, [r3]
080066ee: b8ee678a   vcvt.f32.u32 s16, s15
080066f2: 02f031f9   bl        #0x8008958
080066f6: dfed497a   vldr      s15, [pc, #0x124] ; [0800681c]=42780000
080066fa: 9fed497a   vldr      s14, [pc, #0x124] ; [08006820]=474d1400
080066fe: 4948       ldr       r0, [pc, #0x124] ; [08006824]=10000498
08006700: 494b       ldr       r3, [pc, #0x124] ; [08006828]=1000048c
08006702: 4a4a       ldr       r2, [pc, #0x128] ; [0800682c]=100004a0
08006704: 4a49       ldr       r1, [pc, #0x128] ; [08006830]=3b449ba6
08006706: 2f60       str       r7, [r5]
08006708: c7ee887a   vdiv.f32  s15, s15, s16
0800670c: 1160       str       r1, [r2]
0800670e: 28ee800a   vmul.f32  s0, s17, s0
08006712: b4eec78a   vcmpe.f32 s16, s14
08006716: bceec00a   vcvt.u32.f32 s0, s0
0800671a: f1ee10fa   vmrs      apsr_nzcv, fpscr
0800671e: c0ed007a   vstr      s15, [r0]
08006722: 83ed000a   vstr      s0, [r3]
08006726: 4cdc       bgt       #0x80067c2
08006728: dfed427a   vldr      s15, [pc, #0x108] ; [08006834]=46d6d800
0800672c: b4eee78a   vcmpe.f32 s16, s15
08006730: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006734: 3ddc       bgt       #0x80067b2
08006736: dfed407a   vldr      s15, [pc, #0x100] ; [08006838]=451c4000
0800673a: b4eee78a   vcmpe.f32 s16, s15
0800673e: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006742: 00f3b180   bgt.w     #0x80068a8
08006746: dfed3d7a   vldr      s15, [pc, #0xf4] ; [0800683c]=449c4000
0800674a: 3d4b       ldr       r3, [pc, #0xf4] ; [08006840]=100003f4
0800674c: b4eee78a   vcmpe.f32 s16, s15
08006750: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006754: 00f3ae80   bgt.w     #0x80068b4
08006758: b6ee007a   vmov.f32  s14, #5.000000e-01
0800675c: f0ee477a   vmov.f32  s15, s14
08006760: 83ed007a   vstr      s14, [r3]
08006764: 88ee278a   vdiv.f32  s16, s16, s15
08006768: 3648       ldr       r0, [pc, #0xd8] ; [08006844]=40009808
0800676a: 214a       ldr       r2, [pc, #0x84] ; [080067f0]=10000074
0800676c: 2149       ldr       r1, [pc, #0x84] ; [080067f4]=10000014
0800676e: 184d       ldr       r5, [pc, #0x60] ; [080067d0]=100004b4
08006770: d2ed016a   vldr      s13, [r2, #4]
08006774: bdeec88a   vcvt.s32.f32 s16, s16
08006778: 8ded018a   vstr      s16, [sp, #4]
0800677c: bdf80430   ldrh.w    r3, [sp, #4]
08006780: 0360       str       r3, [r0]
08006782: d4f88000   ldr.w     r0, [r4, #0x80]
08006786: d2ed007a   vldr      s15, [r2]
0800678a: d4f88030   ldr.w     r3, [r4, #0x80]
0800678e: 00fb06f0   mul       r0, r0, r6
08006792: 07ee100a   vmov      s14, r0
08006796: f8ee677a   vcvt.f32.u32 s15, s15
0800679a: b8ee477a   vcvt.f32.u32 s14, s14
0800679e: e7ee267a   vfma.f32  s15, s14, s13
080067a2: fceee77a   vcvt.u32.f32 s15, s15
080067a6: c1ed007a   vstr      s15, [r1]
080067aa: 85e6       b         #0x80064b8
080067ac: d2f88c31   ldr.w     r3, [r2, #0x18c]
080067b0: 01e7       b         #0x80065b6
080067b2: 234b       ldr       r3, [pc, #0x8c] ; [08006840]=100003f4
080067b4: f3ee057a   vmov.f32  s15, #2.100000e+01
080067b8: c3ed007a   vstr      s15, [r3]
080067bc: d2e7       b         #0x8006764
080067be: 1368       ldr       r3, [r2]
080067c0: f9e6       b         #0x80065b6
080067c2: 1f4b       ldr       r3, [pc, #0x7c] ; [08006840]=100003f4
080067c4: dfed207a   vldr      s15, [pc, #0x80] ; [08006848]=431f0000
080067c8: c3ed007a   vstr      s15, [r3]
080067cc: cae7       b         #0x8006764
080067ce: 00bf       nop       
080067d0: b404       lsls      r4, r6, #0x12
080067d2: 0010       asrs      r0, r0, #0x20
080067d4: e006       lsls      r0, r4, #0x1b
080067d6: 0010       asrs      r0, r0, #0x20
080067d8: a903       lsls      r1, r5, #0xe
080067da: 0010       asrs      r0, r0, #0x20
080067dc: 3c03       lsls      r4, r7, #0xc
080067de: 0010       asrs      r0, r0, #0x20
080067e0: f803       lsls      r0, r7, #0xf
080067e2: 0010       asrs      r0, r0, #0x20
080067e4: 10b4       push      {r4}
080067e6: 0008       lsrs      r0, r0, #0x20
080067e8: c802       lsls      r0, r1, #0xb
080067ea: 0010       asrs      r0, r0, #0x20
080067ec: fc02       lsls      r4, r7, #0xb
080067ee: 0010       asrs      r0, r0, #0x20
080067f0: 7400       lsls      r4, r6, #1
080067f2: 0010       asrs      r0, r0, #0x20
080067f4: 1400       movs      r4, r2
080067f6: 0010       asrs      r0, r0, #0x20
080067f8: f0b0       sub       sp, #0x1c0
080067fa: 0008       lsrs      r0, r0, #0x20
080067fc: 0407       lsls      r4, r0, #0x1c
080067fe: 0010       asrs      r0, r0, #0x20
08006800: 0077       strb      r0, [r0, #0x1c]
08006802: 0100       movs      r1, r0
08006804: 0ad7       bvc       #0x800681c
08006806: 233c       subs      r4, #0x23
08006808: 17b7       .byte     0x17, 0xb7
0800680a: d139       subs      r1, #0xd1
0800680c: 9c04       lsls      r4, r3, #0x12
0800680e: 0010       asrs      r0, r0, #0x20
08006810: 0400       movs      r4, r0
08006812: 0010       asrs      r0, r0, #0x20
08006814: 0000       movs      r0, r0
08006816: 0010       asrs      r0, r0, #0x20
08006818: a404       lsls      r4, r4, #0x12
0800681a: 0010       asrs      r0, r0, #0x20
0800681c: 0000       movs      r0, r0
0800681e: 7842       rsbs      r0, r7, #0
08006820: 0014       asrs      r0, r0, #0x10
08006822: 4d47       bxns      sb
08006824: 9804       lsls      r0, r3, #0x12
08006826: 0010       asrs      r0, r0, #0x20
08006828: 8c04       lsls      r4, r1, #0x12
0800682a: 0010       asrs      r0, r0, #0x20
0800682c: a004       lsls      r0, r4, #0x12
0800682e: 0010       asrs      r0, r0, #0x20
08006830: a69b       ldr       r3, [sp, #0x298]
08006832: 443b       subs      r3, #0x44
08006834: 00d8       bhi       #0x8006838
08006836: d646       mov       lr, sl
08006838: 0040       ands      r0, r0
0800683a: 1c45       cmp       r4, r3
0800683c: 0040       ands      r0, r0
0800683e: 9c44       add       ip, r3
08006840: f403       lsls      r4, r6, #0xf
08006842: 0010       asrs      r0, r0, #0x20
08006844: 0898       ldr       r0, [sp, #0x20]
08006846: 0040       ands      r0, r0
08006848: 0000       movs      r0, r0
0800684a: 1f43       orrs      r7, r3
0800684c: cdcc       ldm       r4!, {r0, r2, r3, r6, r7}
0800684e: cc3d       subs      r5, #0xcc
08006850: 07ee903a   vmov      s15, r3
08006854: 1fed037a   vldr      s14, [pc, #-0xc] ; [0800684c]=3dcccccd
08006858: 1a4f       ldr       r7, [pc, #0x68] ; [080068c4]=10000704
0800685a: f8eee77a   vcvt.f32.s32 s15, s15
0800685e: faee040a   vmov.f32  s1, #-1.000000e+01
08006862: e7ee870a   vfma.f32  s1, s15, s14
08006866: b0ee000a   vmov.f32  s0, #2.000000e+00
0800686a: 02f075f8   bl        #0x8008958
0800686e: 164b       ldr       r3, [pc, #0x58] ; [080068c8]=10624dd3
08006870: d7ed037a   vldr      s15, [r7, #0xc]
08006874: a3fb0535   umull     r3, r5, r3, r5
08006878: ad09       lsrs      r5, r5, #6
0800687a: 20ee270a   vmul.f32  s0, s0, s15
0800687e: 07ee905a   vmov      s15, r5
08006882: f8eee77a   vcvt.f32.s32 s15, s15
08006886: c0ee277a   vdiv.f32  s15, s0, s15
0800688a: fceee77a   vcvt.u32.f32 s15, s15
0800688e: f8ee677a   vcvt.f32.u32 s15, s15
08006892: fdeee77a   vcvt.s32.f32 s15, s15
08006896: 17ee905a   vmov      r5, s15
0800689a: 98e6       b         #0x80065ce
0800689c: 4ff4fa51   mov.w     r1, #0x1f40
080068a0: b7e6       b         #0x8006612
080068a2: 9fed0a8a   vldr      s16, [pc, #0x28] ; [080068cc]=00000000
080068a6: ede6       b         #0x8006684
080068a8: 094b       ldr       r3, [pc, #0x24] ; [080068d0]=100003f4
080068aa: f2ee067a   vmov.f32  s15, #1.100000e+01
080068ae: c3ed007a   vstr      s15, [r3]
080068b2: 57e7       b         #0x8006764
080068b4: f7ee007a   vmov.f32  s15, #1.000000e+00
080068b8: c3ed007a   vstr      s15, [r3]
080068bc: 52e7       b         #0x8006764
080068be: 4ff47a51   mov.w     r1, #0x3e80
080068c2: a6e6       b         #0x8006612
080068c4: 0407       lsls      r4, r0, #0x1c
080068c6: 0010       asrs      r0, r0, #0x20
080068c8: d34d       ldr       r5, [pc, #0x34c] ; [08006c18]=0800b0f0
080068ca: 6210       asrs      r2, r4, #1
080068cc: 0000       movs      r0, r0
080068ce: 0000       movs      r0, r0
080068d0: f403       lsls      r4, r6, #0xf
080068d2: 0010       asrs      r0, r0, #0x20
080068d4: b74b       ldr       r3, [pc, #0x2dc] ; [08006bb4]=100002a6
080068d6: b84a       ldr       r2, [pc, #0x2e0] ; [08006bb8]=1000033d
080068d8: 1b78       ldrb      r3, [r3]
080068da: 0021       movs      r1, #0
080068dc: 1170       strb      r1, [r2]
080068de: 002b       cmp       r3, #0
080068e0: 40f00581   bne.w     #0x8006aee
080068e4: 2de9f041   push.w    {r4, r5, r6, r7, r8, lr}
080068e8: b44b       ldr       r3, [pc, #0x2d0] ; [08006bbc]=100002bd
080068ea: 2ded048b   vpush     {d8, d9}
080068ee: 1b78       ldrb      r3, [r3]
080068f0: 82b0       sub       sp, #8
080068f2: 002b       cmp       r3, #0
080068f4: 32d1       bne       #0x800695c
080068f6: 90f83810   ldrb.w    r1, [r0, #0x38]
080068fa: b14a       ldr       r2, [pc, #0x2c4] ; [08006bc0]=100004b4
080068fc: 0368       ldr       r3, [r0]
080068fe: 4ff44874   mov.w     r4, #0x320
08006902: 1e20       movs      r0, #0x1e
08006904: 82e81100   stm.w     r2, {r0, r4}
08006908: ae48       ldr       r0, [pc, #0x2b8] ; [08006bc4]=100003f8
0800690a: 0029       cmp       r1, #0
0800690c: 40f0f680   bne.w     #0x8006afc
08006910: ad49       ldr       r1, [pc, #0x2b4] ; [08006bc8]=0800b410 ','
08006912: 90f86440   ldrb.w    r4, [r0, #0x64]
08006916: 01f59660   add.w     r0, r1, #0x4b0
0800691a: 8d2c       cmp       r4, #0x8d
0800691c: 08bf       it        eq
0800691e: 0846       moveq     r0, r1
08006920: 642b       cmp       r3, #0x64
08006922: 00f2e880   bhi.w     #0x8006af6
08006926: 1bb1       cbz       r3, #0x8006930
08006928: 013b       subs      r3, #1
0800692a: 03eb4303   add.w     r3, r3, r3, lsl #1
0800692e: 9b00       lsls      r3, r3, #2
08006930: c418       adds      r4, r0, r3
08006932: 40f63511   movw      r1, #0x935
08006936: 257a       ldrb      r5, [r4, #8]
08006938: c358       ldr       r3, [r0, r3]
0800693a: 9360       str       r3, [r2, #8]
0800693c: 01fb05f3   mul       r3, r1, r5
08006940: 6068       ldr       r0, [r4, #4]
08006942: d060       str       r0, [r2, #0xc]
08006944: 1b12       asrs      r3, r3, #8
08006946: 5382       strh      r3, [r2, #0x12]
08006948: a048       ldr       r0, [pc, #0x280] ; [08006bcc]=100002c8
0800694a: a149       ldr       r1, [pc, #0x284] ; [08006bd0]=100002fc
0800694c: 9c4a       ldr       r2, [pc, #0x270] ; [08006bc0]=100004b4
0800694e: 02b0       add       sp, #8
08006950: bdec048b   vpop      {d8, d9}
08006954: bde8f041   pop.w     {r4, r5, r6, r7, r8, lr}
08006958: 00f080bb   b.w       #0x800705c
0800695c: 0446       mov       r4, r0
0800695e: c06a       ldr       r0, [r0, #0x2c]
08006960: 02f0eafe   bl        #0x8009738
08006964: 974b       ldr       r3, [pc, #0x25c] ; [08006bc4]=100003f8
08006966: 2568       ldr       r5, [r4]
08006968: e26a       ldr       r2, [r4, #0x2c]
0800696a: 93f86420   ldrb.w    r2, [r3, #0x64]
0800696e: 07ee900a   vmov      s15, r0
08006972: 8d2a       cmp       r2, #0x8d
08006974: b8ee678a   vcvt.f32.u32 s16, s15
08006978: 00f0ba80   beq.w     #0x8006af0
0800697c: 93f86420   ldrb.w    r2, [r3, #0x64]
08006980: 8f2a       cmp       r2, #0x8f
08006982: 14bf       ite       ne
08006984: 6ff00201   mvnne     r1, #2
08006988: 6ff00501   mvneq     r1, #5
0800698c: 5b6f       ldr       r3, [r3, #0x74]
0800698e: 9148       ldr       r0, [pc, #0x244] ; [08006bd4]=66666667
08006990: da17       asrs      r2, r3, #0x1f
08006992: 80fb0303   smull     r0, r3, r0, r3
08006996: c2eba303   rsb       r3, r2, r3, asr #2
0800699a: 0d44       add       r5, r1
0800699c: 2b44       add       r3, r5
0800699e: c3f16403   rsb.w     r3, r3, #0x64
080069a2: 00ee903a   vmov      s1, r3
080069a6: f8eee00a   vcvt.f32.s32 s1, s1
080069aa: f2ee047a   vmov.f32  s15, #1.000000e+01
080069ae: c0eea70a   vdiv.f32  s1, s1, s15
080069b2: b0ee000a   vmov.f32  s0, #2.000000e+00
080069b6: 01f0cfff   bl        #0x8008958
080069ba: e36a       ldr       r3, [r4, #0x2c]
080069bc: 41f65832   movw      r2, #0x1b58
080069c0: 9342       cmp       r3, r2
080069c2: 88ee008a   vdiv.f32  s16, s16, s0
080069c6: 08d9       bls       #0x80069da
080069c8: b3f5fa5f   cmp.w     r3, #0x1f40
080069cc: 40f2bf80   bls.w     #0x8006b4e
080069d0: 42f6e062   movw      r2, #0x2ee0
080069d4: 9342       cmp       r3, r2
080069d6: 00f2c680   bhi.w     #0x8006b66
080069da: 7f4b       ldr       r3, [pc, #0x1fc] ; [08006bd8]=10000704
080069dc: 5868       ldr       r0, [r3, #4]
080069de: 0128       cmp       r0, #1
080069e0: 40f2da80   bls.w     #0x8006b98
080069e4: 1b68       ldr       r3, [r3]
080069e6: 9968       ldr       r1, [r3, #8]
080069e8: d3f800c0   ldr.w     ip, [r3]
080069ec: df68       ldr       r7, [r3, #0xc]
080069ee: 5e68       ldr       r6, [r3, #4]
080069f0: 4ff47a74   mov.w     r4, #0x3e8
080069f4: 04fb01fe   mul       lr, r4, r1
080069f8: 9645       cmp       lr, r2
080069fa: 10d2       bhs       #0x8006a1e
080069fc: a046       mov       r8, r4
080069fe: 0121       movs      r1, #1
08006a00: 0131       adds      r1, #1
08006a02: 8142       cmp       r1, r0
08006a04: 00f0c880   beq.w     #0x8006b98
08006a08: 1c69       ldr       r4, [r3, #0x10]
08006a0a: d3f808c0   ldr.w     ip, [r3, #8]
08006a0e: 5f69       ldr       r7, [r3, #0x14]
08006a10: de68       ldr       r6, [r3, #0xc]
08006a12: 08fb04fe   mul       lr, r8, r4
08006a16: 9645       cmp       lr, r2
08006a18: 03f10803   add.w     r3, r3, #8
08006a1c: f0d3       blo       #0x8006a00
08006a1e: 4ff47a70   mov.w     r0, #0x3e8
08006a22: 00fb0cf0   mul       r0, r0, ip
08006a26: 121a       subs      r2, r2, r0
08006a28: 07fb02f3   mul       r3, r7, r2
08006a2c: c0eb0e01   rsb       r1, r0, lr
08006a30: b3fbf1f3   udiv      r3, r3, r1
08006a34: 3344       add       r3, r6
08006a36: 06fb02f2   mul       r2, r6, r2
08006a3a: b2fbf1f1   udiv      r1, r2, r1
08006a3e: 5b1a       subs      r3, r3, r1
08006a40: 07ee903a   vmov      s15, r3
08006a44: f8ee678a   vcvt.f32.u32 s17, s15
08006a48: c5f16403   rsb.w     r3, r5, #0x64
08006a4c: 00ee903a   vmov      s1, r3
08006a50: f8eee00a   vcvt.f32.s32 s1, s1
08006a54: f2ee047a   vmov.f32  s15, #1.000000e+01
08006a58: c0eea70a   vdiv.f32  s1, s1, s15
08006a5c: 5f4c       ldr       r4, [pc, #0x17c] ; [08006bdc]=1000049c
08006a5e: 604d       ldr       r5, [pc, #0x180] ; [08006be0]=39d1b717
08006a60: b0ee000a   vmov.f32  s0, #2.000000e+00
08006a64: 01f078ff   bl        #0x8008958
08006a68: 5e49       ldr       r1, [pc, #0x178] ; [08006be4]=10000004
08006a6a: 5f4a       ldr       r2, [pc, #0x17c] ; [08006be8]=10000000
08006a6c: 5f4b       ldr       r3, [pc, #0x17c] ; [08006bec]=100004a4
08006a6e: 92ed009a   vldr      s18, [r2]
08006a72: d1ed000a   vldr      s1, [r1]
08006a76: 0022       movs      r2, #0
08006a78: 88ee800a   vdiv.f32  s0, s17, s0
08006a7c: 1a70       strb      r2, [r3]
08006a7e: 01f06bff   bl        #0x8008958
08006a82: 5b4b       ldr       r3, [pc, #0x16c] ; [08006bf0]=1000048c
08006a84: 5b48       ldr       r0, [pc, #0x16c] ; [08006bf4]=10000498
08006a86: 5c4a       ldr       r2, [pc, #0x170] ; [08006bf8]=100004a0
08006a88: 5c49       ldr       r1, [pc, #0x170] ; [08006bfc]=3b449ba6
08006a8a: 2560       str       r5, [r4]
08006a8c: 1160       str       r1, [r2]
08006a8e: dfed5c7a   vldr      s15, [pc, #0x170] ; [08006c00]=42780000
08006a92: 9fed5c7a   vldr      s14, [pc, #0x170] ; [08006c04]=474d1400
08006a96: c7ee887a   vdiv.f32  s15, s15, s16
08006a9a: 29ee000a   vmul.f32  s0, s18, s0
08006a9e: b4eec78a   vcmpe.f32 s16, s14
08006aa2: bceec00a   vcvt.u32.f32 s0, s0
08006aa6: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006aaa: c0ed007a   vstr      s15, [r0]
08006aae: 83ed000a   vstr      s0, [r3]
08006ab2: 38dc       bgt       #0x8006b26
08006ab4: dfed547a   vldr      s15, [pc, #0x150] ; [08006c08]=46d6d800
08006ab8: b4eee78a   vcmpe.f32 s16, s15
08006abc: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006ac0: 48dc       bgt       #0x8006b54
08006ac2: dfed527a   vldr      s15, [pc, #0x148] ; [08006c0c]=451c4000
08006ac6: b4eee78a   vcmpe.f32 s16, s15
08006aca: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006ace: 66dc       bgt       #0x8006b9e
08006ad0: dfed4f7a   vldr      s15, [pc, #0x13c] ; [08006c10]=449c4000
08006ad4: 4f4b       ldr       r3, [pc, #0x13c] ; [08006c14]=100003f4
08006ad6: b4eee78a   vcmpe.f32 s16, s15
08006ada: f1ee10fa   vmrs      apsr_nzcv, fpscr
08006ade: 56dc       bgt       #0x8006b8e
08006ae0: b6ee007a   vmov.f32  s14, #5.000000e-01
08006ae4: f0ee477a   vmov.f32  s15, s14
08006ae8: 83ed007a   vstr      s14, [r3]
08006aec: 20e0       b         #0x8006b30
08006aee: 7047       bx        lr
08006af0: 6ff00501   mvn       r1, #5
08006af4: 4ae7       b         #0x800698c
08006af6: 40f2a443   movw      r3, #0x4a4
08006afa: 19e7       b         #0x8006930
08006afc: 4649       ldr       r1, [pc, #0x118] ; [08006c18]=0800b0f0
08006afe: 90f86440   ldrb.w    r4, [r0, #0x64]
08006b02: 01f5c870   add.w     r0, r1, #0x190
08006b06: 8d2c       cmp       r4, #0x8d
08006b08: 18bf       it        ne
08006b0a: 0146       movne     r1, r0
08006b0c: 642b       cmp       r3, #0x64
08006b0e: 27d8       bhi       #0x8006b60
08006b10: 002b       cmp       r3, #0
08006b12: 4ad0       beq       #0x8006baa
08006b14: 03f18043   add.w     r3, r3, #0x40000000
08006b18: 013b       subs      r3, #1
08006b1a: 51f82330   ldr.w     r3, [r1, r3, lsl #2]
08006b1e: 9360       str       r3, [r2, #8]
08006b20: 0023       movs      r3, #0
08006b22: d360       str       r3, [r2, #0xc]
08006b24: 10e7       b         #0x8006948
08006b26: 3b4b       ldr       r3, [pc, #0xec] ; [08006c14]=100003f4
08006b28: dfed3c7a   vldr      s15, [pc, #0xf0] ; [08006c1c]=431f0000
08006b2c: c3ed007a   vstr      s15, [r3]
08006b30: 88ee278a   vdiv.f32  s16, s16, s15
08006b34: 3a4a       ldr       r2, [pc, #0xe8] ; [08006c20]=40009808
08006b36: bdeec88a   vcvt.s32.f32 s16, s16
08006b3a: 8ded018a   vstr      s16, [sp, #4]
08006b3e: bdf80430   ldrh.w    r3, [sp, #4]
08006b42: 1360       str       r3, [r2]
08006b44: 02b0       add       sp, #8
08006b46: bdec048b   vpop      {d8, d9}
08006b4a: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
08006b4e: 4ff4fa52   mov.w     r2, #0x1f40
08006b52: 42e7       b         #0x80069da
08006b54: 2f4b       ldr       r3, [pc, #0xbc] ; [08006c14]=100003f4
08006b56: f3ee057a   vmov.f32  s15, #2.100000e+01
08006b5a: c3ed007a   vstr      s15, [r3]
08006b5e: e7e7       b         #0x8006b30
08006b60: d1f88c31   ldr.w     r3, [r1, #0x18c]
08006b64: dbe7       b         #0x8006b1e
08006b66: b3f57a5f   cmp.w     r3, #0x3e80
08006b6a: 20d9       bls       #0x8006bae
08006b6c: 45f6c052   movw      r2, #0x5dc0
08006b70: 9342       cmp       r3, r2
08006b72: 7ff632af   bls.w     #0x80069da
08006b76: 48f6a042   movw      r2, #0x8ca0
08006b7a: 9342       cmp       r3, r2
08006b7c: 7ff62daf   bls.w     #0x80069da
08006b80: b3f57a4f   cmp.w     r3, #0xfa00
08006b84: 274a       ldr       r2, [pc, #0x9c] ; [08006c24]=00017700
08006b86: 98bf       it        ls
08006b88: 4ff47a42   movls.w   r2, #0xfa00
08006b8c: 25e7       b         #0x80069da
08006b8e: f7ee007a   vmov.f32  s15, #1.000000e+00
08006b92: c3ed007a   vstr      s15, [r3]
08006b96: cbe7       b         #0x8006b30
08006b98: dfed238a   vldr      s17, [pc, #0x8c] ; [08006c28]=00000000
08006b9c: 54e7       b         #0x8006a48
08006b9e: 1d4b       ldr       r3, [pc, #0x74] ; [08006c14]=100003f4
08006ba0: f2ee067a   vmov.f32  s15, #1.100000e+01
08006ba4: c3ed007a   vstr      s15, [r3]
08006ba8: c2e7       b         #0x8006b30
08006baa: 0b68       ldr       r3, [r1]
08006bac: b7e7       b         #0x8006b1e
08006bae: 4ff47a52   mov.w     r2, #0x3e80
08006bb2: 12e7       b         #0x80069da
08006bb4: a602       lsls      r6, r4, #0xa
08006bb6: 0010       asrs      r0, r0, #0x20
08006bb8: 3d03       lsls      r5, r7, #0xc
08006bba: 0010       asrs      r0, r0, #0x20
08006bbc: bd02       lsls      r5, r7, #0xa
08006bbe: 0010       asrs      r0, r0, #0x20
08006bc0: b404       lsls      r4, r6, #0x12
08006bc2: 0010       asrs      r0, r0, #0x20
08006bc4: f803       lsls      r0, r7, #0xf
08006bc6: 0010       asrs      r0, r0, #0x20
08006bc8: 10b4       push      {r4}
08006bca: 0008       lsrs      r0, r0, #0x20
08006bcc: c802       lsls      r0, r1, #0xb
08006bce: 0010       asrs      r0, r0, #0x20
08006bd0: fc02       lsls      r4, r7, #0xb
08006bd2: 0010       asrs      r0, r0, #0x20
08006bd4: 6766       str       r7, [r4, #0x64]
08006bd6: 6666       str       r6, [r4, #0x64]
08006bd8: 0407       lsls      r4, r0, #0x1c
08006bda: 0010       asrs      r0, r0, #0x20
08006bdc: 9c04       lsls      r4, r3, #0x12
08006bde: 0010       asrs      r0, r0, #0x20
08006be0: 17b7       .byte     0x17, 0xb7
08006be2: d139       subs      r1, #0xd1
08006be4: 0400       movs      r4, r0
08006be6: 0010       asrs      r0, r0, #0x20
08006be8: 0000       movs      r0, r0
08006bea: 0010       asrs      r0, r0, #0x20
08006bec: a404       lsls      r4, r4, #0x12
08006bee: 0010       asrs      r0, r0, #0x20
08006bf0: 8c04       lsls      r4, r1, #0x12
08006bf2: 0010       asrs      r0, r0, #0x20
08006bf4: 9804       lsls      r0, r3, #0x12
08006bf6: 0010       asrs      r0, r0, #0x20
08006bf8: a004       lsls      r0, r4, #0x12
08006bfa: 0010       asrs      r0, r0, #0x20
08006bfc: a69b       ldr       r3, [sp, #0x298]
08006bfe: 443b       subs      r3, #0x44
08006c00: 0000       movs      r0, r0
08006c02: 7842       rsbs      r0, r7, #0
08006c04: 0014       asrs      r0, r0, #0x10
08006c06: 4d47       bxns      sb
08006c08: 00d8       bhi       #0x8006c0c
08006c0a: d646       mov       lr, sl
08006c0c: 0040       ands      r0, r0
08006c0e: 1c45       cmp       r4, r3
08006c10: 0040       ands      r0, r0
08006c12: 9c44       add       ip, r3
08006c14: f403       lsls      r4, r6, #0xf
08006c16: 0010       asrs      r0, r0, #0x20
08006c18: f0b0       sub       sp, #0x1c0
08006c1a: 0008       lsrs      r0, r0, #0x20
08006c1c: 0000       movs      r0, r0
08006c1e: 1f43       orrs      r7, r3
08006c20: 0898       ldr       r0, [sp, #0x20]
08006c22: 0040       ands      r0, r0
08006c24: 0077       strb      r0, [r0, #0x1c]
08006c26: 0100       movs      r1, r0
08006c28: 0000       movs      r0, r0
08006c2a: 0000       movs      r0, r0
08006c2c: a44b       ldr       r3, [pc, #0x290] ; [08006ec0]=100002c4
08006c2e: 2de9f041   push.w    {r4, r5, r6, r7, r8, lr}
08006c32: 1b78       ldrb      r3, [r3]
08006c34: a34c       ldr       r4, [pc, #0x28c] ; [08006ec4]=100002c0
08006c36: 0025       movs      r5, #0
08006c38: 2570       strb      r5, [r4]
08006c3a: 6570       strb      r5, [r4, #1]
08006c3c: a570       strb      r5, [r4, #2]
08006c3e: e570       strb      r5, [r4, #3]
08006c40: 0bb9       cbnz      r3, #0x8006c46
08006c42: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
08006c46: a049       ldr       r1, [pc, #0x280] ; [08006ec8]=40021018
08006c48: a04a       ldr       r2, [pc, #0x280] ; [08006ecc]=40017400
08006c4a: 0b68       ldr       r3, [r1]
08006c4c: a04f       ldr       r7, [pc, #0x280] ; [08006ed0]=48000418
08006c4e: 43f00053   orr       r3, r3, #0x20000000
08006c52: 0b60       str       r3, [r1]
08006c54: d2f8cc33   ldr.w     r3, [r2, #0x3cc]
08006c58: 23f00d03   bic       r3, r3, #0xd
08006c5c: 43f00e03   orr       r3, r3, #0xe
08006c60: 4ff00041   mov.w     r1, #-0x80000000
08006c64: c2f8cc33   str.w     r3, [r2, #0x3cc]
08006c68: 0646       mov       r6, r0
08006c6a: 3960       str       r1, [r7]
08006c6c: 4ff08040   mov.w     r0, #0x40000000
08006c70: 03f0fbfd   bl        #0x800a86a
08006c74: 4ff08040   mov.w     r0, #0x40000000
08006c78: 0121       movs      r1, #1
08006c7a: 03f0b3fd   bl        #0x800a7e4
08006c7e: 2946       mov       r1, r5
08006c80: 9448       ldr       r0, [pc, #0x250] ; [08006ed4]=40014000
08006c82: 03f09ffe   bl        #0x800a9c4
08006c86: 944b       ldr       r3, [pc, #0x250] ; [08006ed8]=48000810
08006c88: 1b68       ldr       r3, [r3]
08006c8a: 1b07       lsls      r3, r3, #0x1c
08006c8c: 1cd4       bmi       #0x8006cc8
08006c8e: 032e       cmp       r6, #3
08006c90: 00f08580   beq.w     #0x8006d9e
08006c94: 012e       cmp       r6, #1
08006c96: 17d1       bne       #0x8006cc8
08006c98: 904f       ldr       r7, [pc, #0x240] ; [08006edc]=100002bd
08006c9a: 914d       ldr       r5, [pc, #0x244] ; [08006ee0]=100003f8
08006c9c: 3a78       ldrb      r2, [r7]
08006c9e: 002a       cmp       r2, #0
08006ca0: 00f0e680   beq.w     #0x8006e70
08006ca4: dff88082   ldr.w     r8, [pc, #0x280] ; [08006f28]=10000008
08006ca8: 8b4b       ldr       r3, [pc, #0x22c] ; [08006ed8]=48000810
08006caa: 1b68       ldr       r3, [r3]
08006cac: 83f00803   eor       r3, r3, #8
08006cb0: c3f3c003   ubfx      r3, r3, #3, #1
08006cb4: 6370       strb      r3, [r4, #1]
08006cb6: 8b4b       ldr       r3, [pc, #0x22c] ; [08006ee4]=48000818
08006cb8: 4ff40021   mov.w     r1, #0x80000
08006cbc: 1960       str       r1, [r3]
08006cbe: dab1       cbz       r2, #0x8006cf8
08006cc0: e86a       ldr       r0, [r5, #0x2c]
08006cc2: fef709fc   bl        #0x80054d8
08006cc6: 1be0       b         #0x8006d00
08006cc8: 834b       ldr       r3, [pc, #0x20c] ; [08006ed8]=48000810
08006cca: 1b68       ldr       r3, [r3]
08006ccc: 83f00803   eor       r3, r3, #8
08006cd0: c3f3c003   ubfx      r3, r3, #3, #1
08006cd4: 6370       strb      r3, [r4, #1]
08006cd6: 042e       cmp       r6, #4
08006cd8: 58d8       bhi       #0x8006d8c
08006cda: dfe816f0   tbh       [pc, r6, lsl #1] ; [08006cdc]=003af016
08006cde: 3a00       movs      r2, r7
08006ce0: 9b00       lsls      r3, r3, #2
08006ce2: 3200       movs      r2, r6
08006ce4: ea00       lsls      r2, r5, #3
08006ce6: 0500       movs      r5, r0
08006ce8: 7e4b       ldr       r3, [pc, #0x1f8] ; [08006ee4]=48000818
08006cea: 7d4d       ldr       r5, [pc, #0x1f4] ; [08006ee0]=100003f8
08006cec: 7b4f       ldr       r7, [pc, #0x1ec] ; [08006edc]=100002bd
08006cee: dff83882   ldr.w     r8, [pc, #0x238] ; [08006f28]=10000008
08006cf2: 4ff40022   mov.w     r2, #0x80000
08006cf6: 1a60       str       r2, [r3]
08006cf8: 7b48       ldr       r0, [pc, #0x1ec] ; [08006ee8]=100002c8
08006cfa: 7c49       ldr       r1, [pc, #0x1f0] ; [08006eec]=100002fc
08006cfc: fff7faf8   bl        #0x8005ef4
08006d00: 95f84130   ldrb.w    r3, [r5, #0x41]
08006d04: 042b       cmp       r3, #4
08006d06: 72d0       beq       #0x8006dee
08006d08: 6f4a       ldr       r2, [pc, #0x1bc] ; [08006ec8]=40021018
08006d0a: 7549       ldr       r1, [pc, #0x1d4] ; [08006ee0]=100003f8
08006d0c: 1368       ldr       r3, [r2]
08006d0e: 23f00053   bic       r3, r3, #0x20000000
08006d12: 1360       str       r3, [r2]
08006d14: d8f80030   ldr.w     r3, [r8]
08006d18: 2a68       ldr       r2, [r5]
08006d1a: 9a42       cmp       r2, r3
08006d1c: 03d0       beq       #0x8006d26
08006d1e: 0846       mov       r0, r1
08006d20: 0b60       str       r3, [r1]
08006d22: fff7d7fd   bl        #0x80068d4
08006d26: 3b78       ldrb      r3, [r7]
08006d28: 002b       cmp       r3, #0
08006d2a: 34d1       bne       #0x8006d96
08006d2c: 95f87830   ldrb.w    r3, [r5, #0x78]
08006d30: 032b       cmp       r3, #3
08006d32: 30d0       beq       #0x8006d96
08006d34: 6e4a       ldr       r2, [pc, #0x1b8] ; [08006ef0]=100004b1
08006d36: 0123       movs      r3, #1
08006d38: 1278       ldrb      r2, [r2]
08006d3a: e270       strb      r2, [r4, #3]
08006d3c: 2370       strb      r3, [r4]
08006d3e: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
08006d42: 674d       ldr       r5, [pc, #0x19c] ; [08006ee0]=100003f8
08006d44: 654f       ldr       r7, [pc, #0x194] ; [08006edc]=100002bd
08006d46: 286b       ldr       r0, [r5, #0x30]
08006d48: dff8dc81   ldr.w     r8, [pc, #0x1dc] ; [08006f28]=10000008
08006d4c: 01f040f8   bl        #0x8007dd0
08006d50: d6e7       b         #0x8006d00
08006d52: 644b       ldr       r3, [pc, #0x190] ; [08006ee4]=48000818
08006d54: 4ff48022   mov.w     r2, #0x40000
08006d58: 1a60       str       r2, [r3]
08006d5a: 03f0e7ff   bl        #0x800ad2c
08006d5e: 41f21856   movw      r6, #0x1518
08006d62: 0546       mov       r5, r0
08006d64: 03f0e2ff   bl        #0x800ad2c
08006d68: a6f58c33   sub.w     r3, r6, #0x11800
08006d6c: a842       cmp       r0, r5
08006d6e: a0eb0502   sub.w     r2, r0, r5
08006d72: a3f5a073   sub.w     r3, r3, #0x140
08006d76: dabf       itte      le
08006d78: 451b       suble     r5, r0, r5
08006d7a: 7619       addle     r6, r6, r5
08006d7c: 9e18       addgt     r6, r3, r2
08006d7e: 002e       cmp       r6, #0
08006d80: 0546       mov       r5, r0
08006d82: efdc       bgt       #0x8006d64
08006d84: 5b4b       ldr       r3, [pc, #0x16c] ; [08006ef4]=100003a8
08006d86: 1b78       ldrb      r3, [r3]
08006d88: 002b       cmp       r3, #0
08006d8a: 49d1       bne       #0x8006e20
08006d8c: 544d       ldr       r5, [pc, #0x150] ; [08006ee0]=100003f8
08006d8e: 534f       ldr       r7, [pc, #0x14c] ; [08006edc]=100002bd
08006d90: dff89481   ldr.w     r8, [pc, #0x194] ; [08006f28]=10000008
08006d94: b4e7       b         #0x8006d00
08006d96: 584b       ldr       r3, [pc, #0x160] ; [08006ef8]=10000484
08006d98: 1b78       ldrb      r3, [r3]
08006d9a: a370       strb      r3, [r4, #2]
08006d9c: cae7       b         #0x8006d34
08006d9e: 574b       ldr       r3, [pc, #0x15c] ; [08006efc]=100003a9
08006da0: 4f4d       ldr       r5, [pc, #0x13c] ; [08006ee0]=100003f8
08006da2: 1b78       ldrb      r3, [r3]
08006da4: 002b       cmp       r3, #0
08006da6: 48d0       beq       #0x8006e3a
08006da8: 4b4b       ldr       r3, [pc, #0x12c] ; [08006ed8]=48000810
08006daa: 1b68       ldr       r3, [r3]
08006dac: 83f00803   eor       r3, r3, #8
08006db0: c3f3c003   ubfx      r3, r3, #3, #1
08006db4: 6370       strb      r3, [r4, #1]
08006db6: 4b4b       ldr       r3, [pc, #0x12c] ; [08006ee4]=48000818
08006db8: 4ff40022   mov.w     r2, #0x80000
08006dbc: 1a60       str       r2, [r3]
08006dbe: 95f87830   ldrb.w    r3, [r5, #0x78]
08006dc2: 032b       cmp       r3, #3
08006dc4: 09d8       bhi       #0x8006dda
08006dc6: dfe803f0   tbb       [pc, r3] ; [08006dc8]=2034f003
08006dca: 3420       movs      r0, #0x34
08006dcc: 2002       lsls      r0, r4, #8
08006dce: d5f88000   ldr.w     r0, [r5, #0x80]
08006dd2: 00f5fa60   add.w     r0, r0, #0x7d0
08006dd6: fef77ffb   bl        #0x80054d8
08006dda: 4949       ldr       r1, [pc, #0x124] ; [08006f00]=1000033d
08006ddc: 494b       ldr       r3, [pc, #0x124] ; [08006f04]=1000033c
08006dde: 3f4f       ldr       r7, [pc, #0xfc] ; [08006edc]=100002bd
08006de0: dff84481   ldr.w     r8, [pc, #0x144] ; [08006f28]=10000008
08006de4: 0120       movs      r0, #1
08006de6: 0022       movs      r2, #0
08006de8: 0870       strb      r0, [r1]
08006dea: 1a70       strb      r2, [r3]
08006dec: 88e7       b         #0x8006d00
08006dee: 464a       ldr       r2, [pc, #0x118] ; [08006f08]=100006e0
08006df0: dff838e1   ldr.w     lr, [pc, #0x138] ; [08006f2c]=10000330
08006df4: 454e       ldr       r6, [pc, #0x114] ; [08006f0c]=1000000c
08006df6: 464b       ldr       r3, [pc, #0x118] ; [08006f10]=10000332
08006df8: d2e90001   ldrd      r0, r1, [r2]
08006dfc: 0521       movs      r1, #5
08006dfe: 0a22       movs      r2, #0xa
08006e00: aef80000   strh.w    r0, [lr]
08006e04: 3170       strb      r1, [r6]
08006e06: 1a80       strh      r2, [r3]
08006e08: 7ee7       b         #0x8006d08
08006e0a: 3748       ldr       r0, [pc, #0xdc] ; [08006ee8]=100002c8
08006e0c: 3749       ldr       r1, [pc, #0xdc] ; [08006eec]=100002fc
08006e0e: fff771f8   bl        #0x8005ef4
08006e12: e2e7       b         #0x8006dda
08006e14: 314f       ldr       r7, [pc, #0xc4] ; [08006edc]=100002bd
08006e16: 324d       ldr       r5, [pc, #0xc8] ; [08006ee0]=100003f8
08006e18: 3a78       ldrb      r2, [r7]
08006e1a: dff80c81   ldr.w     r8, [pc, #0x10c] ; [08006f28]=10000008
08006e1e: 4ae7       b         #0x8006cb6
08006e20: 3c48       ldr       r0, [pc, #0xf0] ; [08006f14]=10000374
08006e22: 3d49       ldr       r1, [pc, #0xf4] ; [08006f18]=10000340
08006e24: 2e4d       ldr       r5, [pc, #0xb8] ; [08006ee0]=100003f8
08006e26: 2d4f       ldr       r7, [pc, #0xb4] ; [08006edc]=100002bd
08006e28: dff8fc80   ldr.w     r8, [pc, #0xfc] ; [08006f28]=10000008
08006e2c: fff762f8   bl        #0x8005ef4
08006e30: 66e7       b         #0x8006d00
08006e32: 286b       ldr       r0, [r5, #0x30]
08006e34: 00f0ccff   bl        #0x8007dd0
08006e38: cfe7       b         #0x8006dda
08006e3a: dfed387a   vldr      s15, [pc, #0xe0] ; [08006f1c]=43fa0000
08006e3e: 95ed187a   vldr      s14, [r5, #0x60]
08006e42: dfed376a   vldr      s13, [pc, #0xdc] ; [08006f20]=42480000
08006e46: ea6f       ldr       r2, [r5, #0x7c]
08006e48: 37eec77a   vsub.f32  s14, s15, s14
08006e4c: c7ee277a   vdiv.f32  s15, s14, s15
08006e50: 67eea67a   vmul.f32  s15, s15, s13
08006e54: fdeee77a   vcvt.s32.f32 s15, s15
08006e58: 17ee903a   vmov      r3, s15
08006e5c: 002b       cmp       r3, #0
08006e5e: 02dd       ble       #0x8006e66
08006e60: 1a44       add       r2, r3
08006e62: 642a       cmp       r2, #0x64
08006e64: 27dc       bgt       #0x8006eb6
08006e66: 1e48       ldr       r0, [pc, #0x78] ; [08006ee0]=100003f8
08006e68: ea67       str       r2, [r5, #0x7c]
08006e6a: fff711fb   bl        #0x8006490
08006e6e: 9be7       b         #0x8006da8
08006e70: dfed2a7a   vldr      s15, [pc, #0xa8] ; [08006f1c]=43fa0000
08006e74: 95ed187a   vldr      s14, [r5, #0x60]
08006e78: dfed296a   vldr      s13, [pc, #0xa4] ; [08006f20]=42480000
08006e7c: dff8a880   ldr.w     r8, [pc, #0xa8] ; [08006f28]=10000008
08006e80: 37eec77a   vsub.f32  s14, s15, s14
08006e84: d8f80020   ldr.w     r2, [r8]
08006e88: c7ee277a   vdiv.f32  s15, s14, s15
08006e8c: 67eea67a   vmul.f32  s15, s15, s13
08006e90: fdeee77a   vcvt.s32.f32 s15, s15
08006e94: 17ee903a   vmov      r3, s15
08006e98: 002b       cmp       r3, #0
08006e9a: 04dd       ble       #0x8006ea6
08006e9c: 1a44       add       r2, r3
08006e9e: 642a       cmp       r2, #0x64
08006ea0: c4bf       itt       gt
08006ea2: 204b       ldrgt     r3, [pc, #0x80] ; [08006f24]=100004a5
08006ea4: 1e70       strbgt    r6, [r3]
08006ea6: 0e48       ldr       r0, [pc, #0x38] ; [08006ee0]=100003f8
08006ea8: 2a60       str       r2, [r5]
08006eaa: fff713fd   bl        #0x80068d4
08006eae: 3a78       ldrb      r2, [r7]
08006eb0: fae6       b         #0x8006ca8
08006eb2: 0b4d       ldr       r5, [pc, #0x2c] ; [08006ee0]=100003f8
08006eb4: 7fe7       b         #0x8006db6
08006eb6: 1b4b       ldr       r3, [pc, #0x6c] ; [08006f24]=100004a5
08006eb8: 0121       movs      r1, #1
08006eba: 1970       strb      r1, [r3]
08006ebc: d3e7       b         #0x8006e66
08006ebe: 00bf       nop       
08006ec0: c402       lsls      r4, r0, #0xb
08006ec2: 0010       asrs      r0, r0, #0x20
08006ec4: c002       lsls      r0, r0, #0xb
08006ec6: 0010       asrs      r0, r0, #0x20
08006ec8: 1810       asrs      r0, r3, #0x20
08006eca: 0240       ands      r2, r0
08006ecc: 0074       strb      r0, [r0, #0x10]
08006ece: 0140       ands      r1, r0
08006ed0: 1804       lsls      r0, r3, #0x10
08006ed2: 0048       ldr       r0, [pc, #0] ; [08006ed4]=40014000
08006ed4: 0040       ands      r0, r0
08006ed6: 0140       ands      r1, r0
08006ed8: 1008       lsrs      r0, r2, #0x20
08006eda: 0048       ldr       r0, [pc, #0] ; [08006edc]=100002bd
08006edc: bd02       lsls      r5, r7, #0xa
08006ede: 0010       asrs      r0, r0, #0x20
08006ee0: f803       lsls      r0, r7, #0xf
08006ee2: 0010       asrs      r0, r0, #0x20
08006ee4: 1808       lsrs      r0, r3, #0x20
08006ee6: 0048       ldr       r0, [pc, #0] ; [08006ee8]=100002c8
08006ee8: c802       lsls      r0, r1, #0xb
08006eea: 0010       asrs      r0, r0, #0x20
08006eec: fc02       lsls      r4, r7, #0xb
08006eee: 0010       asrs      r0, r0, #0x20
08006ef0: b104       lsls      r1, r6, #0x12
08006ef2: 0010       asrs      r0, r0, #0x20
08006ef4: a803       lsls      r0, r5, #0xe
08006ef6: 0010       asrs      r0, r0, #0x20
08006ef8: 8404       lsls      r4, r0, #0x12
08006efa: 0010       asrs      r0, r0, #0x20
08006efc: a903       lsls      r1, r5, #0xe
08006efe: 0010       asrs      r0, r0, #0x20
08006f00: 3d03       lsls      r5, r7, #0xc
08006f02: 0010       asrs      r0, r0, #0x20
08006f04: 3c03       lsls      r4, r7, #0xc
08006f06: 0010       asrs      r0, r0, #0x20
08006f08: e006       lsls      r0, r4, #0x1b
08006f0a: 0010       asrs      r0, r0, #0x20
08006f0c: 0c00       movs      r4, r1
08006f0e: 0010       asrs      r0, r0, #0x20
08006f10: 3203       lsls      r2, r6, #0xc
08006f12: 0010       asrs      r0, r0, #0x20
08006f14: 7403       lsls      r4, r6, #0xd
08006f16: 0010       asrs      r0, r0, #0x20
08006f18: 4003       lsls      r0, r0, #0xd
08006f1a: 0010       asrs      r0, r0, #0x20
08006f1c: 0000       movs      r0, r0
08006f1e: fa43       mvns      r2, r7
08006f20: 0000       movs      r0, r0
08006f22: 4842       rsbs      r0, r1, #0
08006f24: a504       lsls      r5, r4, #0x12
08006f26: 0010       asrs      r0, r0, #0x20
08006f28: 0800       movs      r0, r1
08006f2a: 0010       asrs      r0, r0, #0x20
08006f2c: 3003       lsls      r0, r6, #0xc
08006f2e: 0010       asrs      r0, r0, #0x20
08006f30: 4268       ldr       r2, [r0, #4]
08006f32: 4b68       ldr       r3, [r1, #4]
08006f34: 9a42       cmp       r2, r3
08006f36: 03d3       blo       #0x8006f40
08006f38: 8cbf       ite       hi
08006f3a: 0120       movhi     r0, #1
08006f3c: 0020       movls     r0, #0
08006f3e: 7047       bx        lr
08006f40: 4ff0ff30   mov.w     r0, #-1
08006f44: 7047       bx        lr
08006f46: 00bf       nop       
08006f48: 2de9f041   push.w    {r4, r5, r6, r7, r8, lr}
08006f4c: 404d       ldr       r5, [pc, #0x100] ; [08007050]=100003f8
08006f4e: 95f86530   ldrb.w    r3, [r5, #0x65]
08006f52: 002b       cmp       r3, #0
08006f54: 4bd1       bne       #0x8006fee
08006f56: 95f86c30   ldrb.w    r3, [r5, #0x6c]
08006f5a: 0bb9       cbnz      r3, #0x8006f60
08006f5c: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
08006f60: ab6e       ldr       r3, [r5, #0x68]
08006f62: 41f65832   movw      r2, #0x1b58
08006f66: 9342       cmp       r3, r2
08006f68: 4fd8       bhi       #0x800700a
08006f6a: 3a4b       ldr       r3, [pc, #0xe8] ; [08007054]=10000704
08006f6c: d3f80480   ldr.w     r8, [r3, #4]
08006f70: b8f1010f   cmp.w     r8, #1
08006f74: 65d9       bls       #0x8007042
08006f76: 1b68       ldr       r3, [r3]
08006f78: 9c68       ldr       r4, [r3, #8]
08006f7a: d3f800c0   ldr.w     ip, [r3]
08006f7e: de68       ldr       r6, [r3, #0xc]
08006f80: 5f68       ldr       r7, [r3, #4]
08006f82: 4ff47a7e   mov.w     lr, #0x3e8
08006f86: 0efb04f4   mul       r4, lr, r4
08006f8a: a242       cmp       r2, r4
08006f8c: 0ed9       bls       #0x8006fac
08006f8e: 0121       movs      r1, #1
08006f90: 0131       adds      r1, #1
08006f92: 4145       cmp       r1, r8
08006f94: 55d0       beq       #0x8007042
08006f96: 1c69       ldr       r4, [r3, #0x10]
08006f98: d3f808c0   ldr.w     ip, [r3, #8]
08006f9c: 5e69       ldr       r6, [r3, #0x14]
08006f9e: df68       ldr       r7, [r3, #0xc]
08006fa0: 0efb04f4   mul       r4, lr, r4
08006fa4: 9442       cmp       r4, r2
08006fa6: 03f10803   add.w     r3, r3, #8
08006faa: f1d3       blo       #0x8006f90
08006fac: 4ff47a73   mov.w     r3, #0x3e8
08006fb0: 03fb0cf3   mul       r3, r3, ip
08006fb4: d21a       subs      r2, r2, r3
08006fb6: e41a       subs      r4, r4, r3
08006fb8: 06fb02f6   mul       r6, r6, r2
08006fbc: b6fbf4f6   udiv      r6, r6, r4
08006fc0: 3e44       add       r6, r7
08006fc2: 07fb02f2   mul       r2, r7, r2
08006fc6: 6423       movs      r3, #0x64
08006fc8: b2fbf4f4   udiv      r4, r2, r4
08006fcc: 341b       subs      r4, r6, r4
08006fce: a4fb0323   umull     r2, r3, r4, r3
08006fd2: 296f       ldr       r1, [r5, #0x70]
08006fd4: 5524       movs      r4, #0x55
08006fd6: a1fb0445   umull     r4, r5, r1, r4
08006fda: a4fb0067   umull     r6, r7, r4, r0
08006fde: 00fb0577   mla       r7, r0, r5, r7
08006fe2: 3946       mov       r1, r7
08006fe4: 3046       mov       r0, r6
08006fe6: 02f0bdfe   bl        #0x8009d64
08006fea: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
08006fee: ab6e       ldr       r3, [r5, #0x68]
08006ff0: 95f86610   ldrb.w    r1, [r5, #0x66]
08006ff4: 1b01       lsls      r3, r3, #4
08006ff6: 44f62062   movw      r2, #0x4e20
08006ffa: 00fb03f0   mul       r0, r0, r3
08006ffe: 02fb01f3   mul       r3, r2, r1
08007002: b0fbf3f0   udiv      r0, r0, r3
08007006: bde8f081   pop.w     {r4, r5, r6, r7, r8, pc}
0800700a: b3f5fa5f   cmp.w     r3, #0x1f40
0800700e: 15d9       bls       #0x800703c
08007010: 42f6e062   movw      r2, #0x2ee0
08007014: 9342       cmp       r3, r2
08007016: a8d9       bls       #0x8006f6a
08007018: b3f57a5f   cmp.w     r3, #0x3e80
0800701c: 14d9       bls       #0x8007048
0800701e: 45f6c052   movw      r2, #0x5dc0
08007022: 9342       cmp       r3, r2
08007024: a1d9       bls       #0x8006f6a
08007026: 48f6a042   movw      r2, #0x8ca0
0800702a: 9342       cmp       r3, r2
0800702c: 9dd9       bls       #0x8006f6a
0800702e: b3f57a4f   cmp.w     r3, #0xfa00
08007032: 094a       ldr       r2, [pc, #0x24] ; [08007058]=00017700
08007034: 98bf       it        ls
08007036: 4ff47a42   movls.w   r2, #0xfa00
0800703a: 96e7       b         #0x8006f6a
0800703c: 4ff4fa52   mov.w     r2, #0x1f40
08007040: 93e7       b         #0x8006f6a
08007042: 0022       movs      r2, #0
08007044: 0023       movs      r3, #0
08007046: c4e7       b         #0x8006fd2
08007048: 4ff47a52   mov.w     r2, #0x3e80
0800704c: 8de7       b         #0x8006f6a
0800704e: 00bf       nop       
08007050: f803       lsls      r0, r7, #0xf
08007052: 0010       asrs      r0, r0, #0x20
08007054: 0407       lsls      r4, r0, #0x1c
08007056: 0010       asrs      r0, r0, #0x20
08007058: 0077       strb      r0, [r0, #0x1c]
0800705a: 0100       movs      r1, r0
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
