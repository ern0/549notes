;BYTEBEAT v0.48 by TomCat/Abaddon

;TIMINGS
KICKDRUM_    EQU 1
HIHAT_       EQU 3
INSTRUMENT1_ EQU 1
INSTRUMENT2_ EQU 5
ARPEGGIO_    EQU 4
FADEOUT_     EQU 7

KDRUMMASK = (0)
HIHATMASK = (64+32)

;KEYS
; scroll stop/play: scrlock
; exit: esc
; sample rate: left right
; sample zoom: + -
; global volume: up dn  pgup pgdn
; kick drum: 1 2  3 4  5 6  7 8 lshift rshift
; hihat: q w  e r  t y  u i  o p  [ ] lshift rshift
; instruments: TAB  z x  c v  b n  m ,  . -  capslock
; arpeggio: f1 f2  f3 f4  f5 f6  f7 f8  f9 f10  ; lshift rshift
; notes: asdfghjk capslock numlock insert lshift ctrl  l lshift rshift
; snapshot save/load: enter backspace

Divider   EQU 63
RESX      EQU 320
RESY      EQU 200
LASTLINE  EQU 165

ORG 256
 MOV    FS,AX                   ; FS: segment of BIOS variables
 MOV    AL,13H
 ADD    DH,AL
 MOV    GS,DX                   ; GS: segment of sample
 INT    10H
 PUSH   BX
 PUSH   0B6H-256
 MOV    AX,3508H
 INT    21H
 PUSH   ES
 PUSH   BX
 CALL   INIT
 PUSH   WORD 0A000H             ; ES: segment of video memory
 POP    ES
 MOV    DI,RESX*LASTLINE-RESX*65
 MOV    CX,RESX*66
 MOV    AL,15
 REP    STOSB
 JMP    DECODE

MAIN:
 MOV    AH,01H                  ; check keyboard buffer
 INT    16H
 JZ     SHOW

 MOV    AH,00H
 INT    16H
 CMP    AH,1                    ; key ESC
 JE     RESET                   ; exit

 CMP    AL,13                   ; key ENTER
 JNE    @F
 PUSHA                          ; save snapshot

 MOV    DX,fname1               ; save the irq code
 SUB    CX,CX
 MOV    AH,3CH
 INT    21H
 XCHG   BX,AX
 MOV    DX,IRQ
 MOV    CX,banotes-IRQ
 MOV    AH,40H
 INT    21H
 MOV    AH,3EH
 INT    21H

 MOV    DX,fname2               ; save the notes
 SUB    CX,CX
 MOV    AH,3CH
 INT    21H
 XCHG   BX,AX
 MOV    DX,banotes0
 MOV    CX,banotesx-banotes0
 MOV    AH,40H
 INT    21H
 MOV    AH,3EH
 INT    21H

 POPA
@@:

 CMP    AL,8                    ; key backspace
 JNE    @F
 PUSHA                          ; restore snapshot

 MOV    DX,fname1               ; restore the irq code
 MOV    AX,3D00H
 INT    21H
 XCHG   BX,AX
 MOV    DX,IRQ
 MOV    CX,banotes-IRQ
 MOV    AH,3FH
 INT    21H
 MOV    AH,3EH
 INT    21H

 MOV    DX,fname2               ; restore the notes
 MOV    AX,3D00H
 INT    21H
 XCHG   BX,AX
 MOV    DX,banotes0
 MOV    CX,banotesx-banotes0
 MOV    AH,3FH
 INT    21H
 MOV    AH,3EH
 INT    21H

 POPA
@@:

 CMP    AL,'+'                  ; zoom out
 JNE    @F
 CMP    BYTE [SHOW.ZOOM-1],127
 JE     @F
 INC    BYTE [SHOW.ZOOM-1]
@@:
 CMP    AL,'-'                  ; zoom in
 JNE    @F
 CMP    BYTE [SHOW.ZOOM-1],1
 JE     @F
 DEC    BYTE [SHOW.ZOOM-1]
@@:

 CMP    AH,80                   ; key down
 JNE    @F
 CMP    WORD [FADEOUT.VOLUME-2],0
 JE     @F
 DEC    WORD [FADEOUT.VOLUME-2]
@@:
 CMP    AH,72                   ; key up
 JNE    @F
 CMP    WORD [FADEOUT.VOLUME-2],65535
 JE     @F
 INC    WORD [FADEOUT.VOLUME-2]
@@:

 CMP    AH,81                   ; key pagedown
 JNE    @F
 SUB    WORD [FADEOUT.VOLUME-2],1000
 JNC    @F
 MOV    WORD [FADEOUT.VOLUME-2],0
@@:
 CMP    AH,73                   ; key pageup
 JNE    @F
 ADD    WORD [FADEOUT.VOLUME-2],1000
 JNC    @F
 MOV    WORD [FADEOUT.VOLUME-2],65535
@@:

 CMP    AH,2                    ; key 1
 JNE    @F
 CMP    WORD [KICKDRUM.TEMPO-2],1
 JE     @F
 SHR    WORD [KICKDRUM.TEMPO-2],1
@@:
 CMP    AH,3                    ; key 2
 JNE    @F
 CMP    WORD [KICKDRUM.TEMPO-2],32767
 JE     @F
 STC
 RCL    WORD [KICKDRUM.TEMPO-2],1
@@:

 CMP    AH,4                    ; key 3
 JNE    @F
 CMP    WORD [KICKDRUM.LENGTH-2],512
 JNA    @F
 SUB    WORD [KICKDRUM.LENGTH-2],512
@@:
 CMP    AH,5                    ; key 4
 JNE    @F
 CMP    WORD [KICKDRUM.LENGTH-2],32768-512
 JNB    @F
 ADD    WORD [KICKDRUM.LENGTH-2],512
@@:

 CMP    AH,6                    ; key 5
 JNE    @F
;CMP    WORD [KICKDRUM.VOLUME-2],1
;JE     @F
 SHR    WORD [KICKDRUM.VOLUME-2],1
@@:
 CMP    AH,7                    ; key 6
 JNE    @F
 CMP    WORD [KICKDRUM.VOLUME-2],256
 JE     @F
 SHL    WORD [KICKDRUM.VOLUME-2],1
 JNZ    @F
 INC    WORD [KICKDRUM.VOLUME-2]
@@:

 CMP    AH,8                    ; key 7
 JNE    @F
 MOV    SI,KICKDRUM.ENABLE-1
 CALL   KEYJUMP
@@:

 CMP    AH,9                    ; key 8
 JNE    @F
 MOV    SI,KICKDRUM.MASK-1
 CALL   KEYJUMP
@@:

 CMP    AH,16                   ; key q
 JNE    @F
 CMP    WORD [HIHAT.TEMPO-2],1
 JE     @F
 SHR    WORD [HIHAT.TEMPO-2],1
@@:
 CMP    AH,17                   ; key w
 JNE    @F
 CMP    WORD [HIHAT.TEMPO-2],511
 JE     @F
 STC
 RCL    WORD [HIHAT.TEMPO-2],1
@@:

 CMP    AH,18                   ; key e
 JNE    @F
 CMP    BYTE [HIHAT.SPEED-1],16+1
 JE     @F
 DEC    BYTE [HIHAT.SPEED-1]
@@:
 CMP    AH,19                   ; key r
 JNE    @F
 CMP    BYTE [HIHAT.SPEED-1],16+16
 JE     @F
 INC    BYTE [HIHAT.SPEED-1]
@@:

 CMP    AH,20                   ; key t
 JNE    @F
 CMP    WORD [HIHAT.RANDOM-2],1
 JE     @F
 DEC    WORD [HIHAT.RANDOM-2]
@@:
 CMP    AH,21                   ; key z
 JNE    @F
 CMP    WORD [HIHAT.RANDOM-2],300
 JE     @F
 INC    WORD [HIHAT.RANDOM-2]
@@:

 CMP    AH,22                   ; key u
 JNE    @F
;CMP    WORD [HIHAT.VOLUME-2],1
;JE     @F
 SHR    WORD [HIHAT.VOLUME-2],1
@@:
 CMP    AH,23                   ; key i
 JNE    .2
 CMP    WORD [HIHAT.VOLUME-2],256
 JE     .2
 SHL    WORD [HIHAT.VOLUME-2],1
 JNZ    .1
 INC    WORD [HIHAT.VOLUME-2]
.1:
 CMP    WORD [HIHAT.VOLUME-2],256
 JNE    .2
 CMP    BYTE [HIHAT.FADEOUT-1],1
 JNE    .2
 INC    BYTE [HIHAT.FADEOUT-1]
.2:

 CMP    AH,24                   ; key o
 JNE    @F
 CMP    BYTE [HIHAT.FADEOUT-1],1
 JE     @F
 DEC    BYTE [HIHAT.FADEOUT-1]
 CMP    BYTE [HIHAT.FADEOUT-1],1
 JNE    @F
 CMP    WORD [HIHAT.VOLUME-2],256
 JNE    @F
 SHR    WORD [HIHAT.VOLUME-2],1
@@:
 CMP    AH,25                   ; key p
 JNE    @F
 CMP    BYTE [HIHAT.FADEOUT-1],9
 JE     @F
 INC    BYTE [HIHAT.FADEOUT-1]
@@:

 CMP    AH,26                   ; key [
 JNE    @F
 MOV    SI,HIHAT.ENABLE-1
 CALL   KEYJUMP
@@:

 CMP    AH,27                   ; key ]
 JNE    @F
 MOV    SI,HIHAT.MASK-1
 CALL   KEYJUMP
@@:

 CMP    AH,59                   ; key F1
 JNE    @F
 CMP    BYTE [ARPEGGIO.OFFSET-1],0
 JE     @F
 DEC    BYTE [ARPEGGIO.OFFSET-1]
@@:
 CMP    AH,60                   ; key F2
 JNE    @F
 CMP    BYTE [ARPEGGIO.OFFSET-1],63
 JE     @F
 INC    BYTE [ARPEGGIO.OFFSET-1]
@@:

 CMP    AH,61                   ; key F3
 JNE    @F
 CMP    BYTE [ARPEGGIO.MASK-1],255
 JE     @F
 INC    BYTE [ARPEGGIO.MASK-1]
@@:
 CMP    AH,62                   ; key F4
 JNE    @F
 CMP    BYTE [ARPEGGIO.MASK-1],0
 JE     @F
 DEC    BYTE [ARPEGGIO.MASK-1]
@@:

 CMP    AH,63                   ; key F5
 JNE    @F
 CMP    BYTE [ARPEGGIO.RATE-1],16
 JE     @F
 INC    BYTE [ARPEGGIO.RATE-1]
@@:
 CMP    AH,64                   ; key F6
 JNE    @F
 CMP    BYTE [ARPEGGIO.RATE-1],2
 JE     @F
 DEC    BYTE [ARPEGGIO.RATE-1]
@@:

 CMP    AH,65                   ; key F7
 JNE    @F
 CMP    BYTE [ARPEGGIO.LENGTH-1],16
 JE     @F
 INC    BYTE [ARPEGGIO.LENGTH-1]
@@:
 CMP    AH,66                   ; key F8
 JNE    @F
 CMP    BYTE [ARPEGGIO.LENGTH-1],0
 JE     @F
 DEC    BYTE [ARPEGGIO.LENGTH-1]
@@:

 CMP    AH,67                   ; key F9
 JNE    @F
;CMP    WORD [ARPEGGIO.VOLUME-2],0
;JE     @F
 DEC    WORD [ARPEGGIO.VOLUME-2]
 TEST   BYTE [ARPEGGIO.VOLUME-2],1
 JNZ    @F
 ADD    WORD [ARPEGGIO.VOLUME-2],2
 SHR    WORD [ARPEGGIO.VOLUME-2],1
@@:
 CMP    AH,68                   ; key F10
 JNE    @F
 CMP    WORD [ARPEGGIO.VOLUME-2],256
 JE     @F
 INC    WORD [ARPEGGIO.VOLUME-2]
 TEST   BYTE [ARPEGGIO.VOLUME-2],1
 JZ     @F
 SUB    WORD [ARPEGGIO.VOLUME-2],2
 STC
 RCL    WORD [ARPEGGIO.VOLUME-2],1
@@:

 CMP    AH,39                   ; key ;
 JNE    @F
 MOV    SI,ARPEGGIO.ENABLE-1
 CALL   KEYJUMP
@@:

KEYINST:
 MOV    BP,INSTRUMENT1
 TEST   BYTE [FS:417H],40H      ; caps lock state
 JZ     @F
 MOV    BP,INSTRUMENT2
@@:

 CMP    AL,9                    ; key TAB
 JNE    .1
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.WAVE-2],127
 MOV    CL,64
 JE     @F
 CMP    [BP-INSTRUMENT1+INSTRUMENT1.WAVE-2],CL
 MOV    CL,255
 JE     @F
 MOV    CL,127
@@:
 MOV    [BP-INSTRUMENT1+INSTRUMENT1.WAVE-2],CL
.1:

 CMP    AH,44                   ; key z
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.OFFSET-1],0
 JE     @F
 DEC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.OFFSET-1]
@@:
 CMP    AH,45                   ; key x
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.OFFSET-1],63
 JE     @F
 INC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.OFFSET-1]
@@:

 CMP    AH,46                   ; key c
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1],0
 JE     @F
 DEC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1]
@@:
 CMP    AH,47                   ; key v
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1],63
 JE     @F
 INC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1]
@@:

 MOV    CL,[BP-INSTRUMENT1+INSTRUMENT1.PAUSE-1]
 CMP    AH,49                   ; key n
 JNE    @F
 SHR    CL,1
 OR     CL,[BP-INSTRUMENT1+INSTRUMENT1.PAUSE-1]
@@:
 CMP    AH,48                   ; key b
 JNE    .2
 SHL    CL,1
 AND    CL,[BP-INSTRUMENT1+INSTRUMENT1.PAUSE-1]
 JNZ    .2
 MOV    CH,[BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1]
 MOV    CL,255
@@:
 SHR    CL,1
 SHR    CH,1
 JNZ    @B
.2:
 MOV    [BP-INSTRUMENT1+INSTRUMENT1.PAUSE-1],CL

 CMP    AH,50                   ; key m
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.TUNE-1],0
 JE     @F
 DEC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.TUNE-1]
@@:
 CMP    AH,51                   ; key ;
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.TUNE-1],99
 JE     @F
 INC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.TUNE-1]
@@:

 CMP    AH,52                   ; key .
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.FADEOUT-1],0
 JE     @F
 DEC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.FADEOUT-1]
@@:
 CMP    AH,53                   ; key -
 JNE    @F
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.FADEOUT-1],8
 JE     @F
 INC    BYTE [BP-INSTRUMENT1+INSTRUMENT1.FADEOUT-1]
@@:

 CMP    AH,38                   ; key l
 JNE    @F
 MOV    SI,INSTRUMENT1.ENABLE-1-INSTRUMENT1
 CALL   KEYJUMP.0
@@:

 CMP    AH,30                   ; key a
 JB     .3
 CMP    AH,37                   ; key k
 JA     .3
 MOV    DI,banotes
 MOV    AL,[FS:417H]
 AND    AL,40H                  ; caps lock state
 SHR    AL,3
 ADD    AL,AH
 SUB    AL,30
 MOV    AH,[FS:417H]
 AND    AH,20H                  ; num lock state
 XOR    AH,20H
 SHR    AH,5
 MOV    BH,[FS:417H]
 AND    BH,80H                  ; insert lock state
 XOR    BH,80H
 SHR    BH,6
 ADD    AH,BH
 AAD    17
 XCHG   BX,AX
 ADD    BX,BX
 INC    BYTE [BX+DI]
 CMP    BYTE [BX+DI],' '+1
 JNE    @F
 MOV    BYTE [BX+DI],'0'
@@:
 CMP    BYTE [BX+DI],'9'+1
 JNE    @F
 MOV    BYTE [BX+DI],'A'
@@:
 CMP    BYTE [BX+DI],'B'+1
 JNE    @F
 MOV    BYTE [BX+DI],' '
@@:
 MOV    AL,[FS:417H]            ; left shift/ctrl state
 SHR    AL,1
 AND    AL,3
 ADD    AL,'2'
 MOV    [BX+DI+1],AL
 JMP    PRINT

.3:

 CMP    AH,77
 JNE    @F
 CMP    BYTE [INIT.RATE-1],31
 JE     @F
 DEC    BYTE [INIT.RATE-1]
 JMP    TIMER
@@:
 CMP    AH,75
 JNE    PRINT
 CMP    BYTE [INIT.RATE-1],255
 JE     PRINT
 INC    BYTE [INIT.RATE-1]
TIMER:
 MOV    AL,[INIT.RATE-1]
 OUT    40H,AL
 MOV    AL,0
 OUT    40H,AL

PRINT:
 MOV    BH,0
 MOV    AH,2
 CWD
 INT    10H                     ; set cursor pos to the topleft corner

 MOV    SI,infotxt
 CALL   PRINTSTRLN.1
 MOV    BL,2                    ; color green
 TEST   BYTE [FS:417H],16       ; test scroll-lock state
 JZ     @F
 MOV    BL,4                    ; color red
@@:
 MOV    AX,[COUNTER+1]          ; pattern
 SHR    AX,9
 CALL   PRINTNUM8
 MOV    AX,[COUNTER]            ; counter
 CALL   PRINTNUM16
 MOV    AL,' '
 INT    10H
 INT    10H

 CALL   NEWLINE
 MOV    SI,freqtxt
 CALL   PRINTSTR

 MOV    CH,[INIT.RATE-1]
 MOV    CL,0
 MOV    DX,01234H
 MOV    AX,0DD00H
 DIV    CX
 CALL   PRINTNUM16
 MOV    SI,zoomtxt
 CALL   PRINTSTR
 MOV    AX,[SHOW.ZOOM-1]
 CALL   PRINTNUM8
 MOV    SI,outtxt
 CALL   PRINTSTR
 MOV    BL,13                   ; color magenta
 MOV    AX,[FADEOUT.ENABLE-1]
 CALL   PRINTNUM8
 MOV    SI,volumetxt
 CALL   PRINTSTR
 MOV    AX,[FADEOUT.VOLUME-2]
 CALL   PRINTNUM16
 MOV    AL,' '
 INT    10H
 INT    10H

 MOV    SI,kdrumtxt
 CALL   PRINTSTRLN

 MOV    SI,enabletxt
 CALL   PRINTSTR
 MOV    SI,KICKDRUM.ENABLE-1
 CALL   PRINTJUMP
 MOV    SI,controltxt
 CALL   PRINTSTR
 MOV    SI,KICKDRUM.MASK-1
 CALL   PRINTJUMP

 CALL   NEWLINE
 MOV    SI,ratetxt
 CALL   PRINTSTR
 MOV    AX,[KICKDRUM.TEMPO-2]
 CALL   PRINTNUM16
 MOV    SI,lengthtxt
 CALL   PRINTSTR
 MOV    AX,[KICKDRUM.LENGTH-2]
 CALL   PRINTNUM16
 MOV    SI,volumetxt
 CALL   PRINTSTR
 MOV    AX,[KICKDRUM.VOLUME-2]
 CALL   PRINTNUM16

 MOV    SI,hihattxt
 CALL   PRINTSTRLN
 MOV    SI,enabletxt
 CALL   PRINTSTR
 MOV    SI,HIHAT.ENABLE-1
 CALL   PRINTJUMP
 MOV    SI,controltxt
 CALL   PRINTSTR
 MOV    SI,HIHAT.MASK-1
 CALL   PRINTJUMP
 CALL   NEWLINE
 MOV    SI,ratetxt
 CALL   PRINTSTR
 MOV    AX,[HIHAT.TEMPO-2]
 CALL   PRINTNUM16
 MOV    SI,lengthtxt
 CALL   PRINTSTR
 MOV    AX,[HIHAT.SPEED-1]
 CALL   PRINTNUM8
 MOV    SI,randomtxt
 CALL   PRINTSTR
 MOV    AX,[HIHAT.RANDOM-2]
 CALL   PRINTNUM16
 MOV    SI,volumetxt
 CALL   PRINTSTR
 MOV    AX,[HIHAT.VOLUME-2]
 CALL   PRINTNUM16
 MOV    SI,fadeouttxt
 CALL   PRINTSTR
 MOV    AX,[HIHAT.FADEOUT-1]
 CALL   PRINTNUM8

 MOV    SI,inst1txt
 MOV    BP,INSTRUMENT1
 CALL   PRINTINST

 MOV    SI,inst2txt
 MOV    BP,INSTRUMENT2
 CALL   PRINTINST

 MOV    SI,arpeggiotxt
 CALL   PRINTSTRLN
 MOV    SI,enabletxt
 CALL   PRINTSTR
 MOV    SI,ARPEGGIO.ENABLE-1
 CALL   PRINTJUMP
 CALL   NEWLINE
 MOV    SI,offsettxt
 CALL   PRINTSTR
 MOV    AX,[ARPEGGIO.OFFSET-1]
 CALL   PRINTNUM8

 MOV    SI,masktxt
 CALL   PRINTSTR
 MOV    AX,[ARPEGGIO.MASK-1]
 CALL   PRINTNUM8

 MOV    SI,ratetxt
 CALL   PRINTSTR
 MOV    AX,[ARPEGGIO.RATE-1]
 CALL   PRINTNUM8

 MOV    SI,lengthtxt
 CALL   PRINTSTR
 MOV    AX,[ARPEGGIO.LENGTH-1]
 SUB    AL,16
 NEG    AL
 CALL   PRINTNUM8

 MOV    SI,volumetxt
 CALL   PRINTSTR
 MOV    AX,[ARPEGGIO.VOLUME-2]
 CALL   PRINTNUM16

 MOV    SI,banotes
 CALL   PRINTSTRX
 MOV    AL,' '
 INT    10H

DECODE:
 MOV    SI,banotes
 MOV    DI,puffer
.1:
 LODSW
 SUB    AH,'2'
 JC     .1
 SUB    AL,'0'
 JNC    .2
 MOV    AL,0
 JMP    .4
.2:
 CMP    AL,9
 JNA    .3
 SUB    AL,'A'-'0'-10
.3:
 AAD    12
 XCHG   BX,AX
 MOV    AL,[BX+Notes]
.4:
 MOV    [DI],AL
 INC    DI
 CMP    SI,banotesx
 JC     .1

 JMP    SHOW.0

SHOW:
 TEST   BYTE [FS:417H],16       ; test scroll-lock state
 JNZ    MAIN
.0:
 MOV    EBX,[COUNTER]
 MOV    DI,RESX*LASTLINE
 MOV    CX,RESX
.1:
 DEC    DI
 PUSH   DI
 MOV    DL,0
.2:
 MOV    AL,6                    ; color orange
 CMP    [GS:BX],DL
 JZ     .3
 SALC                           ; color blue
 ADD    AL,9                    ; or grey
.3:
 CMP    BYTE [GS:BX],64         ; sample overflow?
 JB     .4
 MOV    AL,12                   ; color red
.4:
 STOSB
 SUB    DI,RESX+1
 INC    DX
 CMP    DL,64
 JB     .2
 SUB    BX,16
.ZOOM:
 POP    DI
 LOOP   .1
 JMP    MAIN

INIT:
 PUSH   Divider
.RATE:
 PUSH   90H-256
 PUSH   CS
 PUSH   IRQ
RESET:
 POP    DX
 POP    DS
 MOV    AX,2508H
 INT    21H
 POP    AX
 OUT    43H,AL
 POP    AX
 OUT    61H,AL
 OUT    40H,AL
 SALC
 OUT    40H,AL
RETN

NEWLINE:
 MOV    AX,0E0DH
 INT    10H
 MOV    AL,0AH
 INT    10H
RETN

PRINTSTRLN:
 CALL   NEWLINE
.1:
 MOV    BL,14                   ; color yellow
 CALL   PRINTSTR.1
 MOV    AL,' '
 INT    10H
RETN

PRINTSTR:
 MOV    BL,15
.1:
 LODSB
 MOV    AH,0EH
 INT    10H
 CMP    [SI],BH
 JNE    .1
 MOV    BL,11                   ; color cyan
RETN

PRINTSTRX:
.1:
 LODSB
 MOV    AH,0EH
 INT    10H
 XOR    BL,10                   ; swap color
 CMP    [SI],BH
 JNE    .1
RETN

PRINTNUM8:
 MOV    AH,0
PRINTNUM16:
 MOVZX  EAX,AX
PRINTNUM32:
.0:
 SUB    CX,CX
.1:
 SUB    EDX,EDX
 MOV    ESI,10
 DIV    ESI
 ADD    DL,'0'
 PUSH   DX
 INC    CX
 TEST   EAX,EAX
 JNZ    .1
.2:
 POP    AX
 MOV    AH,0EH
 INT    10H
 LOOP   .2
 MOV    AL,' '
 INT    10H
RETN

PRINTJUMP:
 PUSH   SI
 MOV    AX,cmptxt
 CMP    WORD [SI-2],0FF80H      ; CMP BH,
 JE     @F
 CMP    WORD [SI-2],0FB80H      ; CMP BL,
 JE     @F
 MOV    AX,testtxt
@@:
 MOV    BL,13-8                 ; color magenta
 TEST   BYTE [SI-1],4
 JNZ    @F
 MOV    BL,12-8                 ; color red
@@:
 XCHG   SI,AX
 PUSH   BX
 CALL   PRINTSTR.1
 POP    BX
 POP    SI
 LODSW
 PUSH   BX
 ADD    BL,8
 PUSH   AX
 CALL   PRINTNUM8
 POP    AX
 SUB    AH,70H
 SALC
 SHR    AX,6
 MOV    SI,jumptxt
 ADD    SI,AX
 POP    BX
 CALL   PRINTSTR.1
 MOV    AL,' '
 INT    10H
RETN

PRINTINST:
 CALL   PRINTSTRLN
 MOV    SI,enabletxt
 CALL   PRINTSTR
 LEA    SI,[BP-INSTRUMENT1+INSTRUMENT1.ENABLE-1]
 CALL   PRINTJUMP
 MOV    SI,wavetxt
 CALL   PRINTSTR
 MOV    SI,sawtoothtxt
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.WAVE-2],127
 JE     @F
 MOV    SI,squaretxt
 CMP    BYTE [BP-INSTRUMENT1+INSTRUMENT1.WAVE-2],64
 JE     @F
 MOV    SI,triangletxt
@@:
 MOV    BL,11                   ; color cyan
 CALL   PRINTSTR.1
 CALL   NEWLINE
 MOV    SI,offsettxt
 CALL   PRINTSTR
 MOV    AX,[BP-INSTRUMENT1+INSTRUMENT1.OFFSET-1]
 CALL   PRINTNUM8
 MOV    SI,masktxt
 CALL   PRINTSTR
 MOV    AX,[BP-INSTRUMENT1+INSTRUMENT1.LENGTH-1]
 CALL   PRINTNUM8
 MOV    SI,lengthtxt
 CALL   PRINTSTR
 MOV    AX,[BP-INSTRUMENT1+INSTRUMENT1.PAUSE-1]
 CALL   PRINTNUM8
 MOV    SI,tunetxt
 CALL   PRINTSTR
 MOV    AX,[BP-INSTRUMENT1+INSTRUMENT1.TUNE-1]
 CALL   PRINTNUM8
 MOV    SI,fadeouttxt
 CALL   PRINTSTR
 MOV    AX,[BP-INSTRUMENT1+INSTRUMENT1.FADEOUT-1]
 CALL   PRINTNUM8
RETN

KEYJUMP:
 SUB    BP,BP
.0:
 TEST   BYTE [FS:417H],1        ; right shift state
 JNZ    .2
 TEST   BYTE [FS:417H],2        ; left shift state
 JNZ    .1
 CMP    BYTE [BP+SI],255
 JE     @F
 INC    BYTE [BP+SI]
@@:
 RETN
.1:
 CMP    BYTE [BP+SI],0
 JE     @F
 DEC    BYTE [BP+SI]
@@:
 RETN
.2:
 TEST   BYTE [FS:417H],2        ; left shift state
 JNZ    .3
 MOV    CL,[BP+SI+1]
 SUB    CL,70H
 INC    CX
 OR     CL,70H
 MOV    [BP+SI+1],CL
 RETN
.3:
 XOR    WORD [BP+SI-2],3876H
RETN

fname1:
 DB 'BYTEBEAT.IRQ',0
fname2:
 DB 'BYTEBEAT.TXT',0

infotxt:
 DB 'BYTEBEAT by TomCat/Abaddon',0
ratetxt:
 DB 'rate:',0
zoomtxt:
 DB 'zoom:',0
volumetxt:
 DB 'vol:',0
enabletxt:
 DB 'no:',0
controltxt:
 DB 'skip:',0
lengthtxt:
 DB 'len:',0
fadeouttxt:
 DB 'fade:',0
outtxt:
 DB 'out:',0
freqtxt:
 DB 'freq:',0
randomtxt:
 DB 'rnd:',0
masktxt:
 DB 'mask:',0
offsettxt:
 DB 'idx:',0
wavetxt:
 DB 'wave:',0
tunetxt:
 DB 'tune:',0

kdrumtxt:
 DB 'Kick drum',0
hihattxt:
 DB 'Hihat',0
inst1txt:
 DB 'Instrument1',0
inst2txt:
 DB 'Instrument2',0
triangletxt:
 DB 'triangle',0
sawtoothtxt:
 DB 'sawtooth',0
squaretxt:
 DB 'square  ',0
arpeggiotxt:
 DB 'Arpeggio',0

cmptxt:
 DB 'CMP',0
testtxt:
 DB 'TST',0

jumptxt:
 DB 8,'O ',0
 DB 8,'NO',0
 DB 8,'B ',0
 DB 8,'NB',0
 DB 8,'Z ',0
 DB 8,'NZ',0
 DB 8,'NA',0
 DB 8,'A ',0
 DB 8,'S ',0
 DB 8,'NS',0
 DB 8,'PE',0
 DB 8,'PO',0
 DB 8,'L ',0
 DB 8,'NL',0
 DB 8,'NG',0
 DB 8,'G ',0

Notes:
;octave 1
 DB 16  ; 0
 DB 17  ; 1
 DB 18  ; 2
 DB 19  ; 3
 DB 20  ; 4
 DB 21  ; 5
 DB 23  ; 6
 DB 24  ; 7
 DB 25  ; 8
 DB 27  ; 9
 DB 29  ; 10
 DB 30  ; 11
;octave 2
 DB 32  ; 0
 DB 34  ; 1
 DB 36  ; 2
 DB 38  ; 3
 DB 40  ; 4
 DB 43  ; 5
 DB 45  ; 6
 DB 48  ; 7
 DB 51  ; 8
 DB 54  ; 9
 DB 57  ; 10
 DB 60  ; 11
;octave 3
 DB 64  ; 0
 DB 68  ; 1
 DB 72  ; 2
 DB 76  ; 3
 DB 81  ; 4
 DB 85  ; 5
 DB 91  ; 6
 DB 96  ; 7
 DB 102 ; 8
 DB 108 ; 9
 DB 114 ; 10
 DB 121 ; 11
;octave 4
 DB 128 ; 0
 DB 136 ; 1
 DB 144 ; 2
 DB 152 ; 3
 DB 161 ; 4
 DB 171 ; 5
 DB 181 ; 6
 DB 192 ; 7
 DB 203 ; 8
 DB 215 ; 9
 DB 228 ; 10
 DB 242 ; 11

IRQ:
 PUSHA
 MOV    BP,puffer
 MOV    SI,[BP-puffer+COUNTER]
 GS     LODSB
 TEST   AL,AL
 JZ     @F
 OUT    42H,AL
@@:
 MOV    BX,[BP-puffer+COUNTER+1]
 INC    DWORD [BP-puffer+COUNTER]
 SHR    BX,1                    ; BH: pattern
.PATTERN:

KICKDRUM:
 MOV    DI,16383;8191
.TEMPO:
 AND    DI,SI
 MOV    AX,25000 AND 0FE00H     ; 9728
.LENGTH:
 CMP    BH,KICKDRUM_
.ENABLE:
 JE     .SKIP
 TEST   BL,KDRUMMASK
.MASK:
 JNZ    .SKIP
 CWD
 INC    DI
 DIV    DI
.SKIP:
 DB     25H                     ; AND AX,
 DW     64
.VOLUME:
 CWD
 XCHG   CX,AX

HIHAT:
 CMP    BH,HIHAT_
.ENABLE:
 JB     .SKIP
 TEST   BL,HIHATMASK
.MASK:
 JNZ    .SKIP
 MOV    AX,SI
 MOV    DI,99
.RANDOM:
 DIV    DI
 XCHG   AX,DX
 MUL    SI
 DB     25H                     ; AND AX,
 DW     64
.VOLUME:
 CWD
 SHRD   DI,SI,16+6
.SPEED:
 DB     081H,0E7H               ; AND DI,
 DW     63
.TEMPO:
 ADD    DI,1
.FADEOUT:
 DIV    DI
 ADD    CX,AX
.SKIP:

INSTRUMENT1:
 CMP    BH,INSTRUMENT1_
.ENABLE:
 JB     .SKIP
 TEST   BL,(128) SHR 4
.PAUSE:
 JZ     .SKIP
 SHLD   DI,BX,8+4
.TEMPO:
 AND    DI,15
.LENGTH:
 DB     08AH,063H,0            ; MOV    AH,[BP+DI+]
.OFFSET:
 SALC
 MUL    SI
 IMUL   AX,DX,8/2
.TUNE:
 DB     25H                     ; AND AX,
 DW     127                     ; 127 - SAWTOOTH WAVE
;DW     64                      ; 64 - SQUARE WAVE
;DW     255                     ; 255 - TRIANGLE WAVE
.WAVE:
 CBW
 XOR    AL,AH
 CBW
 DB     0C1H,0E8H,1             ; SHR    AX,
.FADEOUT:
 ADD    CX,AX
.SKIP:

INSTRUMENT2:
 CMP    BH,INSTRUMENT2_
.ENABLE:
 JB     .SKIP
 TEST   BL,(128) SHR 5
.PAUSE:
 JZ     .SKIP
 SHLD   DI,BX,8+5
.TEMPO:
 AND    DI,31
.LENGTH:
 DB     08AH,063H,16            ; MOV    AH,[BP+DI+]
.OFFSET:
 SALC
 MUL    SI
 IMUL   AX,DX,8*2
.TUNE:
 DB     25H                     ; AND AX,
;DW     127                     ; SAWTOOTH WAVE
;DW     64                      ; SQUARE WAVE
 DW     255                     ; TRIANGLE WAVE
.WAVE:
 CBW
 XOR    AL,AH
 CBW
 DB     0C1H,0E8H,1             ; SHR    AX,
.FADEOUT:
 ADD    CX,AX
.SKIP:

ARPEGGIO:
 CMP    BH,ARPEGGIO_
.ENABLE:
 JB     .SKIP
 SHRD   AX,BX,4
.RATE:
 SHLD   DI,BX,16-(4)
.LENGTH:
 SHLD   DI,AX,2
 AND    DI,3+4
.MASK:
 DB     08AH,063H,16+32         ; MOV    AH,[BP+DI+]
.OFFSET:
 SALC
 MUL    SI
 XCHG   AX,DX
 DB     25H                     ; AND AX,
 DW     31
.VOLUME:
 ADD    CX,AX
.SKIP:

FADEOUT:
 MOV    AX,35000
.VOLUME:
 MUL    CX
 JNC    .SKIP
 CMP    BH,FADEOUT_
.ENABLE:
 JB     .SKIP
 DEC    WORD [CS:FADEOUT.VOLUME-2]
.SKIP:

 MOV    [GS:SI],DL

 MOV    AL,20H
 OUT    20H,AL
 POPA
IRET

; note:    space  0  1  2  3  4  5  6  7  8  9  A  B
;          pause  C  C# D  D# E  F  F# G  G# A  A# B
; octave:         2  3  4  5
banotes:
 DB 13,13,10,10,10,10,10,10,10,10,10,10
banotes0:
 DB '9405450574B445B425B4744525059474'
 DB 13,10
 DB ' 4 405A405743474 4 405A405743474'
 DB 13,10
 DB '0525352535052505 4 405A405743474'
 DB 13,10
 DB '042474 4043474 4 3 3 3 3 3 3 3 3'
banotesx:
 DB 0

COUNTER:
 DD     1
puffer:
