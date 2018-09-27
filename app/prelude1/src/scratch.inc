	mov 	al,3fH
	mov 	dx,331H
	out 	dx,al

	mov	ah,2cH
	mov	cx,5

next_note:
	push	ax
	push	cx
	call	play_note
	mov	cx,4
	call	wait_some
	pop	cx
	pop	ax

	add	ah,2
	loop	next_note

	mov	ax,4c00H
	int	21H

play_note:
	push	ax
	
	push	ax
	mov	ah,90H
	call	play_byte

	pop	ax
	call	play_byte

	mov	ah,7fH
	call	play_byte

	pop	ax
	ret

play_byte:
	mov	dx,331H
	in	al,dx
	test	al,40H
	jnz	play_byte

	dec	dx
	mov	al,ah
	out	dx,al

	ret

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

	ret
