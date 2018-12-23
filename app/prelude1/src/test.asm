;-----------------------------------------------------------------------
test_note:
	ret
	pusha

	lea	bx,[test_note_data]
	mov	si,[note_index]
	mov	dl,[bx + si]
	inc	word [note_index]

	cmp	al,dl
	je	.okay

	mov	dl,"#"
	mov	ah,2
	int	21H
	jmp	.finish

.okay:
	mov	dl,"."
	mov	ah,2
	int	21H

.finish:
	popa
	ret
;-----------------------------------------------------------------------
test_diff:
	
	pusha

	lea	bx,[test_diff_data]
	mov	si,[diff_index]
	mov	dl,[bx + si]
	inc	word [diff_index]

	cmp	al,dl
	je	.okay

	mov	dl,"*"
	mov	ah,2
	int	21H
	jmp	.finish

.okay:
	mov	dl,"."
	mov	ah,2
	int	21H

.finish:
	popa
	ret
;-----------------------------------------------------------------------
note_index:
	dw	0

diff_index:
	dw	0

include "test-score.inc"
