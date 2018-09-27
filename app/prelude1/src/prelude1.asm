	org 	100H
;------------------------------------------------------

	mov	ax,5
	int	10H

	call	init_newline

	lea	bp,[test_data]
	xor	ch,ch

	call	print_newline

	mov	cl,3
	call	read_bits
	call	print_note

	mov	cl,2
	call	read_bits
	call	print_note

	mov	cl,4
	call	read_bits
	call	print_note

	call	print_newline

	mov	ax,4c00H
	int	21H

test_data:
	db	00011100B, 10001111B
	;	11122333...3

	mov	al,23
	call	print_diff
	mov	al,0
	call	print_diff
	mov	al,-54
	call	print_diff

	mov	ax,4c00H
	int	21H

;------------------------------------------------------
; CH: latch counter
; AH: latch value
;------------------------------------------------------

read_bits:

	xor	al,al
@xbit:
	call	read_one_bit
	dec	cl
	jne	@xbit
	ret

;------------------------------------------------------
read_one_bit:

	or	ch,ch
	jnz	@shift

	mov	ah,[bp]
	inc	bp
	mov	ch,8

@shift:
	dec	ch
	sal	ax,1		; AH MSB -> CF, SHL AL
	adc	al,0		; CF -> AL LSB

	ret	
;------------------------------------------------------
include "score.inc"
include "dump.inc"
