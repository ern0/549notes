;#######################################################################
; Prelude1 - PC-DOS 256-byte intro by ern0
; Created 2018.09.28, released: N/A
;
; This program plays
;  J.S.Bach: Prelude in C major, BWV 846
;  from the Prelude and Fugue in C major, BWV 846
;  from Book I of The Well-Tempered Clavier
; on the MIDI interface
;
; Target: 80386 real mode, assembler: FASM
;

;-----------------------------------------------------------------------
; Register allocation:
;
;	SI - note counter
; 	BP - load data pointer
; 	CH - latch counter
;	CL - word length loop (3 or 5)
; 	AH - latch value
;	AL - result word (on LSBs)
;	BX - table3 or table5 for xlat
;#######################################################################
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
	xor	si,si

@next_note:
	
	call	load_note
	
	mov	cl,al
	call	play_note

	mov	al,6
	call	delay

	inc	si
	cmp	si,202 - 5
	jne	@next_note

	int	20H
;#######################################################################
include "dump.asm"	
;#######################################################################
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
;#######################################################################
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
