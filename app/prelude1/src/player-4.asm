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
;       CL - 
;       CH - 
;       SI - 
;       DI - 
;       BP - global, load data pointer
;       ES - (free)
;
;-----------------------------------------------------------------------
        org     100H

        aas
        mov     dx,331H
        outsb
        xor     dx,dx

        mov     bp,data_notes

;-------------------------------------------
        mov     cx,32*5
part1:
        call    load_note

;rotate_notes:
        mov     di,data_start
        add     al,[di]
        lea     si,[di + 1]
        movsw
        movsw
        stosb

        call    play_note

        loop    part1
;-------------------------------------------
        mov     cx,5+16+16
part2:
        call    load_note

;rotate_notes:
        mov     di,data_start
        add     al,[di]
        lea     si,[di + 1]
        movsw
        movsw
        stosb

        call    play_note

        loop    part2
;-------------------------------------------
        ret
;-----------------------------------------------------------------------
load_note:
        mov     bl,DATA_CSUB
        mov     ax,2000H        ; AL:=0, AH:=%xx10'0000: 3 SHL from zero

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
        test    DL,DL
        jnz     @shift_latch

;load_latch:
        inc     dx              ; INC DX for DL:=1, %xxxx'xxx1: 8 SHL from zero
        mov     dh,[bp]
        inc     bp

@shift_latch:
        sal     ax,1
        sal     dx,1
        adc     al,0

        jmp     @next_bit

@adjust_word:
        sub     al,bl

        ret        
;-----------------------------------------------------------------------
play_note:

        ;call   print_note ;;;;;;;;;;;;;

@ply:
        pusha

        push   ax
        mov    dx,330h
        mov    al,90h           ; MIDI note on cmd
        out    dx,al

        pop    ax               ; MIDI pitch
        out    dx,al

        mov    al,7fh           ; MIDI velocity (127, max)
        out    dx,al

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
include "dump.asm"
include "data-3.inc"
data_cont:
