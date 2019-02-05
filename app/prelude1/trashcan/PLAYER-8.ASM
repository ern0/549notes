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
;       BL - global, line counter
;       BH - global, delay
;       DX - global, constant, 330H - the midi data port
;       CX - local, line counter, note counter
;       SI - local, 5-byte rotation
;       DI - global, used in 5+3 repeat
;       BP - global, load bit pointer
;       ES - global, =DS
;
;-----------------------------------------------------------------------
        TEST_MODE = 0
;
; TEST_MODE #0: compo version
; TEST_MODE #1: instant play (GoD mode)
; TEST_MODE #2: dump notes
;-----------------------------------------------------------------------
        org     100H

        DB      3FH
        MOV     DX,331H
        OUTSB
        DEC     DX

        MOV     AL,13H
        INT     10H

        SUB     BP,BP
        MOV     BL,5+1

@next_line:
        MOV     DI,data_start+5

        MOV     CL,5
@five_of_eight:
        call    load_play_note
        LOOP    @five_of_eight

        SUB     SI,3            ; SI is from rotate_notes
        MOV     CL,3+8
@three_of_eight:
        call    play_note
        LOOP    @three_of_eight
        ADD     AH,4
        JNS     @next_line      ; LOOP 32x (BP:26CH)

        MOV     CL,5+16+16-1
@next:
        CMP     CL,16-1         ; tempo: slow down
        JA      @set_delay
        MOV     BL,6+1          
        CMP     CL,5-1          ; tempo: final 5 notes
        JA      @set_delay
        MOV     BL,1+1          
@set_delay:
        call    load_play_note
        LOOP    @next

        ; fall load_play_note
;-----------------------------------------------------------------------
load_play_note:
        MOV     SI,data_start
        MOV     AL,16                  ; AL:%xxx1'0000: 4 SHL to carry
@load_uncompressed:
        SUB     BYTE [SI],DL           ; DL = DATA_USUB - DATA_CSUB
@read_bit:
        BT      [SI-data_start+data_notes],BP
        INC     BP
        RCL     AL,1
        JNC     @read_bit

;word_read:
        CMP     AL,2            ; check for special value, AL:%xxxx'xx10: 7 SHL to carry
        JE      @load_uncompressed

;adjust_word:
        ADD     AL,DATA_USUB - 2*DATA_CSUB

;rotate_notes:

        ADD     AL,[SI]
        PUSH    DI
        MOV     DI,SI
        INC     SI
        MOVSW
        MOVSW
        STOSB
        DEC     SI
        POP     DI

        ; fall play_note
;-----------------------------------------------------------------------
play_note:

        PUSH    0A000H
        POP     ES
        PUSHA
        MOV     AX,90H
        OUT     DX,AL
        LODSB
        OUT     DX,AL
        PUSH    AX
        MOV     AX,2C7FH
        OUT     DX,AL

        ; fall wait
;-----------------------------------------------------------------------
@wait_tick:
        INT     21H
        CMP     BP,DX
        je      @wait_tick
        MOV     BP,DX
        SUB     DI,DI
        MOV     SI,320
        MOV     CX,32000
if TEST_MODE < 2
        ES
        REP     MOVSW
end if
        DEC     BX
if TEST_MODE < 1
        jne     @wait_tick
end if
        POP     BX
        ADD     BX,BX
        ADD     [ES:DI+BX],BL
        POPA
        PUSH    CS
        POP     ES
        MOVSB
if TEST_MODE > 1
        MOV     AL,[SI-1]
        INT     29H
end if
        ret
;-----------------------------------------------------------------------
include "data-6.inc"
