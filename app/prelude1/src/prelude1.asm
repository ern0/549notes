;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Created 2018.09.28, released: n.a.
;
; This program plays
;  J.S.Bach: Prelude in C major, BWV 846
;  from the Prelude and Fugue in C major, BWV 846
;  from Book I of The Well-Tempered Clavier
; on the MIDI interface
;
; Assembler: TASM
;
;-----------------------------------------------------------------------
	org 	100H
;-----------------------------------------------------------------------

	mov	ax,13H
	int	10H

	call	init_newline

	lea	bp,[data_notes]
	xor	ch,ch

	call	print_newline
	mov	si,10

@next:
	lea	bx,[tab3]
	mov	cl,3
	call	read_bits
	cmp	al,7
	jne	@data

	lea	bx,[tab5]
	mov	cl,5
	call	read_bits
@data:
	call	print_note
	xlatb
	call	print_diff

	dec	si
	jnz	@next

	mov	ax,4c00H
	int	21H

; $05              $b8               $81               $02
; 8 4 2 1 8 4 2 1| 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1
; 0 0 0/0 0 1/0 1| 1/0 1 1/8 0 0/0 | 1 0/0 0 0/0 0 1/| 0 0 0/0 0 0/1 0
; 0     1     3      3     4     2       0     1       0     0
;
;
; $30,$50,$0f,$8f


;-----------------------------------------------------------------------
; BP: data pointer
; CH: latch counter
; AH: latch value
;-----------------------------------------------------------------------
read_bits:

	xor	al,al
@xbit:
	call	read_one_bit
	dec	cl
	jne	@xbit
	ret

;-----------------------------------------------------------------------
read_one_bit:

	or	ch,ch
	jnz	@shift

	mov	ah,[bp]
	inc     bp
	mov	ch,8

@shift:
	dec	ch
	sal	ax,1		; CF << AH MSB and prepare AL by SHL
	adc	al,0		; AL LSB << CF (AL is already shifted)

	ret
;-----------------------------------------------------------------------
include "score.inc"
include "dump.inc"
