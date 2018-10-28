;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0 & TomCat
; Prototype-2: raw-diff-5 nctab nutab
;
; Target: 80386 real mode, assembler: FASM
;
;-----------------------------------------------------------------------
; Register allocation:
;
;       AL - local, bit counter (SHL until carry) + result
;       AH - local, data sub correction
;       BX - global, delay
;       DX - free
;       CL - local, line counter, note counter
;       CH - global, constant zero
;       SI - local, 5-byte rotation, used in 5+3 repeat
;       DI - global, 5-byte rotation
;       BP - global, load bit pointer
;       ES - DS=CS
;
;-----------------------------------------------------------------------
        org     100H

        DB      3FH
        MOV     DX,331H
        OUTSB

;flip bits
;       MOV     DI,data_notes
;       MOV     CX,snapshot_start-data_notes
.1:
;       MOV     BL,8
.2:
;       SHL     BYTE [DI],1
;       RCR     AL,1
;       DEC     BX
;       JNZ     .2
;       STOSB
;       LOOP    .1

        MOV     BP,(data_notes-data_start)*8
        MOV     CL,32
        MOV     BL,5

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

        INC     BX              ; next_simple
        MOV     CL,5+16+16
@next:
        CMP     CL,5+16
        JA      @set_delay
        MOV     BL,7            ; next_last
        CMP     CL,5
        JA      @set_delay
        MOV     BL,1            ; next_finish
@set_delay:
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
        SUB     SI,CX            ; SI is from rotate_notes
@three_of_eight:
        LODSB
        call    play_note
        LOOP    @three_of_eight

        POP     CX
        ret
;-----------------------------------------------------------------------
load_play_note:
        MOV     DI,data_start
        MOV     AX,256*DATA_CSUB+32;AH:DATA_CSUB, AL:%xx10'0000: 3 SHL to carry

@read_bit:
        BT      [DI],BP
        INC     BP
        RCL     AL,1
        JNC     @read_bit

;word_read:
        CMP     AL,2            ; check for %010 special value
;       TEST    AL,AL           ; check for %000 special value
        jnz     @adjust_word

;load_uncompressed:
        MOV     AH,DATA_USUB    ;AH:DATA_USUB, AL:%xxxx'xx10: 7 SHL to carry
        JMP     @read_bit

@adjust_word:
        SUB     AL,AH

;rotate_notes:
        add     al,[di]
        lea     si,[di + 1]

        movsw
        movsw
        stosb

        ; fall play_note
;-----------------------------------------------------------------------
play_note:

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

@wait_some:
        mov     ah,2cH
        int     21H
        MOV     SI,DX

@wait_tick:
        int     21H
        CMP     SI,DX
        je      @wait_tick
        DEC     BX
        jne     @wait_some

        popa
        ret
;-----------------------------------------------------------------------
include "data-3.inc"

snapshot_start:
