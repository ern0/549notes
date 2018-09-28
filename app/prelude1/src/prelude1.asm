	org 	100H
;------------------------------------------------------

	mov	ax,5
	int	10H

	call	init_newline

	lea	bp,[data_notes]
	xor	ch,ch

	call	print_newline
	mov	cx,8

@next:
	push	cx

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

	pop	cx
	loop	@next

	mov	ax,4c00H
	int	21H


;------------------------------------------------------
; BP: data pointer
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
