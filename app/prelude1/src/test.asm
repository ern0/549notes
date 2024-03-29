;-----------------------------------------------------------------------
        TEST_TESTING = 0
;-----------------------------------------------------------------------
test_summary:
	
	lea	dx,[test_note_count_text]
	mov	ah,9
	int	21H

	mov	ax,word [test_note_index]
	call	test_print_u3
	call	test_print_crlf

	test 	word [test_error_count],-1
	jz	.no_errors

	lea	dx,[test_summary_text]
	mov	ah,9
	int	21H

	mov	ax,[test_error_count]	
	call	test_print_u3
	call	test_print_crlf

	jmp	test_quit

.no_errors:
	lea	dx,[test_no_errors]
	mov	ah,9
	int	21H

test_quit:
	mov	ax,4c00H
	int	21H

test_note_count_text:
	db	"number of notes: $"

test_error_count:
	dw	0

test_summary_text:
	db	"number of wrong notes: $"

test_no_errors:
	db	" -=[  P E R F E C T  ]=-",13,10,'$'

;-----------------------------------------------------------------------
test_print_u3:

	call	test_fill_u3

	mov	byte [test_conv_buffer + 3],'$'
	lea	dx,[test_conv_buffer]
	mov	ah,9
	int	21H
	mov	byte [test_conv_buffer + 3],0

	ret
;-----------------------------------------------------------------------
test_print_crlf:

	lea	dx,[test_print_crlf_text]
	mov	ah,9
	int	21H

	ret

test_print_crlf_text:
	db	13,10,'$'	
;-----------------------------------------------------------------------
test_diff:

	if TEST_TESTING > 0
	jmp	test_test
	end if

	pusha
	pushf
	
	call	test_create_file

	lea	dx,[test_diff_prefix]
	call	test_write_string

	push	ax
	lea	si,[test_diff_index]
	mov	ax,[si]
	call	test_write_u3
	pop	ax
	
	call	test_write_colon

	call	test_write_s2

	cmp	word [test_note_index],548
	jbe	.test_data
	lea	dx,[test_diff_overflow_text]
	call	test_write_string
	jmp	.close_line

.test_data:
	lea	bx,[test_diff_data]
	call	test_check_value
	je	.close_line

	lea	dx,[test_diff_error_text]
	call	test_write_string

	mov	al,ah
	call	test_write_s2

.close_line:
	call	test_write_crlf

	popf
	popa
	ret

test_diff_index:
	dw	0

test_diff_prefix:
	db	"diff #",0

test_diff_error_text:
	db	" <---- ",0

test_diff_overflow_text:
	db	" ..... overflow",0
;-----------------------------------------------------------------------
test_note:
	
	if TEST_TESTING > 0
	jmp	test_test
	end if

	pusha
	pushf

	call	test_create_file

	lea	dx,[test_note_prefix]
	call	test_write_string

	push	ax
	lea	si,[test_note_index]
	mov	ax,[si]
	call	test_write_u3
	pop	ax

	call	test_write_colon

	call	test_write_u3b

	cmp	word [si],548
	jbe	.test_data
	inc	word [si]
	lea	dx,[test_note_overflow_text]

	call	test_write_string
	jmp	.close_line

.test_data:	
	lea	bx,[test_note_data]
	call	test_check_value
	je	.close_line

	inc	word [test_error_count]

	lea	dx,[test_note_error_text]
	call	test_write_string

	mov	al,ah
	call	test_write_u3b

.close_line:
	call	test_write_crlf

	popf
	popa
	ret

test_note_index:
	dw	0

test_note_prefix:
	db	"  note #",0

test_note_error_text:
	db	" <-- ",0

test_note_overflow_text:
	db	" ... overflow",0
;-----------------------------------------------------------------------
test_check_value:

	mov	di,word [si]
	inc	word [si]
	mov	ah,[bx + di]

	cmp	al,ah
	ret
;-----------------------------------------------------------------------
test_create_file:
	
	test	word [test_file_handle],-1
	jz	.creat
	ret

.creat:
	pusha

	lea	dx,[test_file_name]
	xor	cx,cx
	mov	ah,3cH
	int	21H
	jc	.fail

	mov	[test_file_handle],ax

	popa
	ret

.fail:
	push	ax
	lea	dx,[test_creat_fail_text]
	mov	ah,9
	int	21H
	pop	ax

	call	test_print_u3
	call	test_print_crlf

	mov	ax,4c01H
	int	21H

test_creat_fail_text:
	db	"failed to create file, code: $"

test_file_handle:
	dw	0
;-----------------------------------------------------------------------
test_write:

	pusha

	mov	ah,40H
	int	21H
	jc	.fail

	call	test_reopen

	popa
	ret

.fail:
	push	ax
	lea	dx,[test_write_failed_text]
	mov	ah,9
	int	21H
	pop	ax

	call	test_print_u3
	call	test_print_crlf

	mov 	ax,4c02H
	int	21H

test_write_failed_text:
	db	"failed to write file, code: $"
;-----------------------------------------------------------------------
test_reopen:

	mov	bx,[test_file_handle]
	mov	ah,3eH
	int	21H
	lea	dx,[test_close_failed_text]
	jc	.fail

	lea	dx,[test_file_name]
	mov	ax,3d02H
	int	21H
	lea	dx,[test_reopen_failed_text]
	jc	.fail

	mov	[test_file_handle],ax

	xor	cx,cx
	xor	dx,dx
	mov	bx,ax
	mov	ax,4202H
	int	21H
	lea	dx,[test_lseek_failed_text]
	jc	.fail

	ret

.fail:
	push	ax
	mov	ah,9
	int	21H
	pop	ax

	call	test_print_u3
	call	test_print_crlf

	mov 	ax,4c02H
	int	21H

test_close_failed_text:
	db	"failed to close file, code: $"

test_reopen_failed_text:
	db	"failed to reopen file, code: $"

test_lseek_failed_text:
	db	"failed to seek in file, code: $"
;-----------------------------------------------------------------------
test_write_string:
	
	pusha
	pushf

	cld
	mov	si,dx
	xor	cx,cx
.next_char:
	lodsb
	or	al,al
	jz	.quit_char
	inc	cx
	jmp	.next_char

.quit_char:
	mov	bx,[test_file_handle]
	call	test_write	

	popf
	popa
	ret
;-----------------------------------------------------------------------
test_write_crlf:

	pusha

	mov	al,13
	call	test_write_char
	mov	al,10
	call	test_write_char

	popa
	ret
;-----------------------------------------------------------------------
test_write_colon:

	pusha

	mov	al,':'
	call	test_write_char
	mov	al,' '
	call	test_write_char
	
	popa
	ret
;-----------------------------------------------------------------------
test_write_char:

	pusha

	mov	[test_char_buffer],al
	mov	cx,1
	lea	dx,[test_char_buffer]
	mov	bx,[test_file_handle]

	call	test_write

	popa
	ret

test_char_buffer:
	db	0
;-----------------------------------------------------------------------
test_write_u3b:
	xor	ah,ah
	; fall test_write_u3
;-----------------------------------------------------------------------
test_write_u3:

	pusha

	call	test_fill_u3

	lea	dx,[test_conv_buffer]
	call	test_write_string

	popa
	ret	
;-----------------------------------------------------------------------
test_fill_u3:

	mov	cx,100
	xor	dx,dx
	div	cx
	add	al,30H
	mov	byte [test_conv_buffer],al

	mov	ax,dx
	jmp	test_fill_u2
;-----------------------------------------------------------------------
test_write_u2:

	pusha

	call	test_fill_u2

	lea	dx,[test_conv_buffer + 1]
	call	test_write_string

	popa
	ret	
;-----------------------------------------------------------------------
test_fill_u2:

	xor	ah,ah

	mov	cx,10
	xor	dx,dx
	div	cx
	add	al,30H
	mov	byte [test_conv_buffer + 1],al
	add	dl,30H
	mov	byte [test_conv_buffer + 2],dl
	
	ret	
;-----------------------------------------------------------------------
test_write_s2:

	pusha

	call	test_fill_s2

	lea	dx,[test_conv_buffer]
	call	test_write_string

	popa
	ret	
;-----------------------------------------------------------------------
test_fill_s2:

	mov	byte [test_conv_buffer],'='
	or	al,al
	je	test_fill_u2

	mov	byte [test_conv_buffer],'+'
	or	al,al
	jns	test_fill_u2

	mov	byte [test_conv_buffer],'-'
	neg	al
	jmp	test_fill_u2

test_conv_buffer:
	db	"xxx",0
;-----------------------------------------------------------------------
test_test:
	call	test_create_file

	mov	ax,+23
	call	test_write_s2

	mov	ax,4c00H
	int	21H
;-----------------------------------------------------------------------
