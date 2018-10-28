;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Prototype-2: raw-diff-5 nctab nutab
;
; Target: 80386 real mode, assembler: FASM
;
;-----------------------------------------------------------------------
; Register allocation:
;
;       AL - param, result: loaded word on LSBs
;       AH - param, word length loop counter (SHL until zero)
;       BL - local, play_note
;       BH - local, data sub correction
;       DL - global, latch counter (SHL until zero)
;       DH - global, latch value
;       CL - global, line
;       CH - local, 5of8 counter
;       SI - local, 5-byte rotation
;       DI - global, 5-byte rotation, used in 5+3 repeat
;       BP - global, load data pointer
;       ES - (free)
;
;-----------------------------------------------------------------------
        org     100H

        DB      3FH
        MOV     DX,331H
        OUTSB

        MOV     BP,data_notes
        CWD
        MOV     CL,32

@next_line:

        MOV     SI,data_start
        MOV     DI,snapshot_start

        pusha
        call    eight_of_eight
        popa

        XCHG    SI,DI

        call    eight_of_eight

;       CMP     CL,2
;       jne     @not1
;       mov     byte [delay-2],5
;@not1:
        LOOP    @next_line

        MOV     CL,5+16+16
@next:
        MOV     AL,6            ; next_simple
        CMP     CL,5+16
        JA      @set_delay
        INC     AX              ; next_last
        CMP     CL,5
        JA      @set_delay
        MOV     AL,1            ; next_finish
@set_delay:
        MOV     [delay-2],AL
        call    load_play_note
        LOOP    @next

        RETN

;-----------------------------------------------------------------------
eight_of_eight:
        PUSH    CX

        MOVSW
        MOVSW
        MOVSB

        MOV     CL,5
@five_of_eight:
        call    load_play_note
        LOOP    @five_of_eight

        MOV     CL,3
@three_of_eight:
        MOV     AL,[DI-3]       ; DI is from rotate_notes
        INC     DI
        call    play_note
        LOOP    @three_of_eight

        POP     CX
        ret
;-----------------------------------------------------------------------
load_play_note:
        mov     bl,DATA_CSUB
        mov     ax,$2000        ; AL:=0, AH:=%xx10'0000: 3 SHL from zero

@next_bit:
        or      ah,ah
        jnz     @read_bit

;word_read:
        or      al,al           ; check for %000 special value
        jnz     @adjust_word

;load_uncompressed:
        mov     bl,DATA_USUB    ; 42, also a good value for bit counter
        mov     ah,bl           ; %xxxx'xx10: 7 SHL from zero
        jmp     @next_bit

@read_bit:
        TEST    DL,DL
        jnz     @shift_latch

;load_latch:
        INC     DX              ; INC DX for DL:=1, %xxxx'xxx1: 8 SHL from zero
        MOV     DH,[BP]
        inc     bp

@shift_latch:
        SHL     DX,1
        RCL     AX,1

        jmp     @next_bit

@adjust_word:
        sub     al,bl

;rotate_notes:
        MOV     DI,data_start
        add     al,[di]
        lea     si,[di + 1]

        movsw
        movsw
        stosb

        ; fall play_note
;-----------------------------------------------------------------------
play_note:

        ;call   print_note ;;;;;;;;;;;;;

@ply:
        pusha

        PUSH   AX
        MOV    DX,330H
        MOV    AL,90H
        OUT    DX,AL
        POP    AX
        OUT    DX,AL
        MOV    AL,7FH
        OUT    DX,AL

        ; fall wait
;-----------------------------------------------------------------------
;wait:
        mov     si,5
delay:

@wait_some:
        mov     ah,2cH
        int     21H
        mov     bl,dl

@wait_tick:
        int     21H
        cmp     bl,dl
        je      @wait_tick
        dec     si
        jne     @wait_some

        popa
        ret
;-----------------------------------------------------------------------
;include "dump.asm"
include "data-3.inc"

snapshot_start:
