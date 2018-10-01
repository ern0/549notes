;#######################################################################
load_note:

	mov	cl,3
;-----------------------------------------------------------------------
@read_word_cl:		; read CL-bit (3 or 5) word
	xor	al,al
@next_bit:
	or	ch,ch
	jnz	@shift_from_latch

	mov	ah,[bp]	; load byte to latch
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

	mov	cl,7
	jmp	@read_word_cl

;-----------------------------------------------------------------------
@read_word_done:

	lea	di,[data_start]
	add	al,[di]
	lea	si,[di + 1]

	movsw
	movsw
	stosb

	ret

