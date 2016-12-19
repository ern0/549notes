; 8086, fasm

	org 100H

next_round:

	in al,60H
	cmp al,1
	je quit_app

	call is_tick
	jnc next_round

	call player

	jmp short next_round


quit_app:
	; just fall through

; ----------------------------------------------------
is_tick:

	xor ah,ah
	int 1aH
	cmp dx,[last_time_value]
	mov [last_time_value],dx
	jz .ret_false

	mov al,[tempo_mul_count]
	inc al
	mov [tempo_mul_count],al
	cmp al,3
	jne .ret_false

	mov byte [tempo_mul_count],0
	stc
	retn

.ret_false:
	clc
	retn

last_time_value:
	dw 0
tempo_mul_count:
	db 0

; ----------------------------------------------------
reset_player:
	mov word [player_ptr],0

player:

	mov al,0b6H
	out 43H,al

	lea si,[song]
	mov bx,[player_ptr]
	mov al,[si+bx]
	inc bx
	mov [player_ptr],bx

	cmp al,-1
	je reset_player

	;;;; call dump

	or al,al
	jz .pause

	xor ah,ah
	shl ax,4

	out 42H,al
	mov al,ah
	out 42H,al

	in al,61H
	or al,3
	out 61H,al

	retn

.pause:
	in al,61H
	and al,0fcH
	out 61H,al

	retn

; ----------------------------------------------------
; notes

	__ equ 0

	; c2 equ 2280
	; h1 equ 2415
	; a1 equ 2711
	; g1 equ 3043
	; f1 equ 3416
	; e1 equ 3619
	; d1 equ 4063


	c2 equ 142
	h1 equ 151
	a1 equ 169
	g1 equ 190
	f1 equ 214
	e1 equ 226
	d1 equ 254

; ----------------------------------------------------
song:

	db c2,c2 , h1,h1
	db a1,a1 , __,__
	db __,__ , e1,e1
	;
	db f1,f1 , __,__
	db f1,f1 , g1,d1
	db d1,__ , __,__ 
	db __,__ , __,__

	db __,__ , __,__

	db 0


player_ptr:
	dw 0

	include "dump.asm"
