; 8086, fasm

	org 100H

init:
	xor bp,bp
	lea si,[song]

	mov al,0b6H
	out 43H,al

	in al,61H
	or al,3
	out 61H,al

next_round:

	lodsw
	or al,al
	jz init

	push ax
	call play
	call delay

	pop ax
	mov al,ah
	call play
	call delay
	call delay
	call delay
	call delay
	call delay

	jmp short next_round
; ----------------------------------------------------
play:
	xor ah,ah
	shl ax,4

	out 42H,al
	mov al,ah
	out 42H,al

	; fall thru
; ----------------------------------------------------
delay:

	in al,60H
	cmp al,1
	je silence
	
	xor ah,ah
	int 1aH
	cmp dx,bp
	mov bp,dx
	jz delay

return:
	retn
; ----------------------------------------------------
silence:

 	in al,61H
 	and al,0fcH
 	out 61H,al

 	int 20H
; ----------------------------------------------------

	c2 equ 142
	h1 equ 151
	a1 equ 169
	g1 equ 190
	f1 equ 214
	e1 equ 226
	d1 equ 254
	xx equ 1

; ----------------------------------------------------
song:

	db c2,d1, c2,e1, c2,f1, c2,a1
	db 0

	;include "dump.asm"
