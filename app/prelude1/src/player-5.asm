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
        org     100H

        DB      3FH
        MOV     DX,331H
        OUTSB
        DEC     DX
        SUB     CX,CX
.1:
        XOR     AL,13H
        INT     10H
        MOV     AX,CX
        MUL     AH
        AND     AL,15
        MOV     AH,0CH
        LOOP    .1

        SUB     BP,BP
        MOV     BH,5+1

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
        ADC     BL,DH           ; ADD BL,4
        JNS     @next_line      ; LOOP 32x (BP:26CH)

        MOV     CL,5+16+16-1
@next:
        MOV     BH,6+1          ; next_simple
        CMP     CL,5+16-1
        JA      @set_delay
        MOV     BH,7+1          ; next_last
        CMP     CL,5-1
        JA      @set_delay
        MOV     BH,1+1          ; next_finish
@set_delay:
        call    load_play_note
        LOOP    @next

;       RETN

;-----------------------------------------------------------------------
load_play_note:
        MOV     SI,data_start
        MOV     AX,256*DATA_CSUB+32;AH:DATA_CSUB, AL:%xx10'0000: 3 SHL to carry
        DB      38H                ;CMP ?,BH - to skip the next instruction
@load_uncompressed:
        MOV     AX,256*DATA_USUB+2 ;AH:DATA_USUB, AL:%xxxx'xx10: 7 SHL to carry
@read_bit:
        BT      [SI-data_start+data_notes],BP
        INC     BP
        RCL     AL,1
        JNC     @read_bit

;word_read:
        TEST    AL,AL           ; check for %000 special value
        JZ      @load_uncompressed

;adjust_word:
        SUB     AL,AH

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
        PUSHA
        MOV     AX,0E90H
        OUT     DX,AL
        LODSB
        OUT     DX,AL
        MOV     BL,AL
        INT     10H             ; dump note
        MOV     AX,7FH;2C7FH
        OUT     DX,AL

        ; fall wait
;-----------------------------------------------------------------------

@wait_tick:
        INT     1AH;21H
        CMP     BP,DX
        je      @wait_tick
        MOV     BP,DX
        DEC     BH
        jne     @wait_tick

        POPA
        MOVSB
        ret

;-----------------------------------------------------------------------
include "data-5.inc"
