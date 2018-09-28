;-----------------------------------------------------------------------
; dump.asm - dump for notes and diffs


;-----------------------------------------------------------------------
init_newline:

	mov	byte [char_counter],0
	ret

;-----------------------------------------------------------------------
check_newline:

	inc	byte [char_counter]
	cmp	byte [char_counter],5  ; according to score.inc
	je	@newline
	ret

@newline:
	call	init_newline
	call	print_newline
	; fall print_newline

print_newline:
	mov	al,13
	call	print_char
	mov	al,10
	call	print_char
	mov	al,' '
	jmp	print_char

;-----------------------------------------------------------------------
print_diff:

	call	print_sign
	; fall print_note

;-----------------------------------------------------------------------
print_note:

	pusha

	call	print_dec
	mov	al,' '
	call	print_char

	popa

	jmp	check_newline

;-----------------------------------------------------------------------
print_sign:

	pusha

	or	al,al

	jne	@not_eq
	mov	dl,'='
	jmp	@fin

@not_eq:
	jns	@not_neg
	mov	dl,'-'
	jmp	@fin

@not_neg:
	mov	dl,'+'

@fin:
	mov	al,dl
	call	print_char

	popa
	ret

;-----------------------------------------------------------------------
print_dec:

	pusha

	cbw
	mov	dl,10
	idiv	dl

	call	print_num
	mov	al,ah
	call	print_num

	popa
	ret

;-----------------------------------------------------------------------
print_num:

	pusha

	or	al,al
	jns	@pos
	neg	al

@pos:
	lea	bx,[nums]
	xlatb
	call	print_char

	popa
	ret

;-----------------------------------------------------------------------
print_char:

	push	ax
	push	dx

	mov	dl,al
	mov	ah,6
	int	21H

	pop	dx
	pop	ax
	ret

;-----------------------------------------------------------------------
nums:
	db	"0123456789"

char_counter:
	db	0
