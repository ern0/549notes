;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Prototype-1: raw-diff-5 (with tables)
;
; Target: 80386 real mode, assembler: FASM
;
;-----------------------------------------------------------------------
; Register allocation:
;
; 	BP - load data pointer
; 	CH - latch counter
;	CL - word length loop (3 or 5)
; 	AH - latch value
;	AL - result word (on LSBs)
;	BX - table3 or table5 for xlat
;-----------------------------------------------------------------------
	org 	100H

	mov 	al,3fH
	mov 	dx,331H
	out 	dx,al
	mov	ax,13H
	int	10H

	call	init_newline

	lea	bp,[data_notes]
	xor	ch,ch

	call	print_newline

@next_note:
	call	load_note

	call	print_note
	jmp	@nplay

	mov	cl,al
	call	play_note
	mov	al,6
	call	delay

@nplay:
	inc	byte [counter]
	cmp	byte [counter],20
	jne	@next_note

	int	20H
;-----------------------------------------------------------------------
counter:
	db 0
;-----------------------------------------------------------------------
load_note:

	lea	bx,[tab3 - 1]
	mov	cl,3

@read_word_cl: 			; read CL-bit (3 or 5) word
	xor	al,al
@next_bit:
	or	ch,ch
	jnz	@shift_from_latch

	mov	ah,[bp]		; load byte to latch
	inc	bp
	mov	ch,8

@shift_from_latch:
	dec	ch
	sal	ax,1		; CF << AH MSB and shift left AL by 1
	adc	al,0		; AL LSB << CF (AL is already shifted)

	dec	cl
	jne	@next_bit

	or	al,al		; check for %000 special value
	jnz	@read_word_done

	add	bl,(tab5 - tab3) ; lea bx,[tab5 - 1]
	mov	cl,5
	jmp	@read_word_cl

@read_word_done:
	xlatb

; rotate
	lea	di,[data_start]
	add	al,[di]
	lea	si,[di + 1]

	movsw
	movsw
	stosb

	ret
;-----------------------------------------------------------------------
play_note:

	pusha

	mov	ah,90H		; Note On, Channel 1
	call	play_byte

	mov	ah,cl		; Pitch
	call	play_byte

	mov	ah,7fH		; Velocity
	call	play_byte

	popa
	ret
;-----------------------------------------------------------------------
play_byte:

	mov	dx,331H
	in	al,dx
	test	al,40H
	jnz	play_byte

	dec	dx
	mov	al,ah
	out	dx,al

	ret
;-----------------------------------------------------------------------
delay:
	pusha

	xor	ch,ch
	mov	cl,al

wait_some:
	push	cx

	mov	ah,2cH
	int	21H
	mov	bl,dl

wait_tick:
	mov	ah,2cH
	int	21H
	cmp	bl,dl
	je	wait_tick
	pop	cx
	loop	wait_some

	popa
	ret
;#######################################################################
include "dump.asm"
include "data-1.inc"
;#######################################################################
