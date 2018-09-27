	org 	100H

	call	init_newline

	lea	bp,[data_notes]
	mov	cx,3
	call	read_bits

	mov	al,23
	call	print_diff
	mov	al,0
	call	print_diff
	mov	al,-54
	call	print_diff


	mov	ax,4c00H
	int	21H


read_bits:
	mov	al,0
	ret


include "score.inc"
include "dump.inc"
