;-----------------------------------------------------------------------
test_note:
	pusha
	
	call	test_create_file
	
	lea	bx,[test_note_data]
	lea	si,[test_note_index]
	call	test_check_value

	popa
	ret
;-----------------------------------------------------------------------
test_diff:
	pusha
	
	call	test_create_file
	
	lea	bx,[test_diff_data]
	lea	si,[test_diff_index]
	call	test_check_value

	popa
	ret
;-----------------------------------------------------------------------
test_check_value:

	mov	di,word [si]
	inc	word [si]
	mov	dl,[bx + di]

	cmp	al,dl
	je	.equals

	mov	dl,"#"
	mov	ah,2
	int	21H
	jmp	.finish

.equals:
	mov	dl,"."
	mov	ah,2
	int	21H

.finish:
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
	lea	dx,[test_creat_fail_text]
	mov	ah,9
	int	21H

	mov	ax,4c01H
	int	21H

test_file_name:
	db	"TEST.TXT",0

test_creat_fail_text:
	db	"failed to create file",13,10,'$'
;-----------------------------------------------------------------------
test_file_handle:
	dw	0

test_note_index:
	dw	0

test_diff_index:
	dw	0

include "test-score.inc"
