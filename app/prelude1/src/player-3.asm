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

        MOV     BP,(data_notes-data_start)*8
        MOV     BL,2

@next_line:

        MOV     SI,data_start
        MOV     DI,snapshot_start

        pusha
        call    eight_of_eight
        popa

        XCHG    SI,DI

        call    eight_of_eight

        SUB     DX,331H/32+1
        JNC     @next_line

        INC     BX              ; next_simple
        MOV     CL,5+16+16-1
@next:
        CMP     CL,5+16-1
        JA      @set_delay
        MOV     BL,7            ; next_last
        CMP     CL,5-1
        JA      @set_delay
        MOV     BL,1            ; next_finish
@set_delay:
        call    load_play_note
        LOOP    @next

;       RETN

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
        SUB     AL,AH           ; adjust_word
        CMP     AL,3            ; check for %011 special value
        JNE     @rotate_notes

;load_uncompressed:
        MOV     AH,128+DATA_USUB;AH:DATA_USUB, AL:%xxxx'xx11: 7 SHL to carry
        JMP     @read_bit

@rotate_notes:
        call    test_diff

        add     al,[di]
        lea     si,[di + 1]

        movsw
        movsw
        stosb

        ; fall play_note
;-----------------------------------------------------------------------
play_note:

        jmp    test_note

        pusha

        PUSH    AX
        INT     29H
        MOV     DX,330H
        MOV     AL,90H
        OUT     DX,AL
        POP     AX
        OUT     DX,AL
        MOV     AL,7FH
        OUT     DX,AL

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
eight_of_eight:

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

        ret
;-----------------------------------------------------------------------
include "data-3.inc"
include "test.asm"

snapshot_start:
