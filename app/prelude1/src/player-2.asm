;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Prototype-2: raw-diff-5 nctab nutab
;
; Target: 80386 real mode, assembler: FASM
;
;-----------------------------------------------------------------------
; Register allocation:
;
;       Common:
;	  AL - param, result diff word (on LSBs)
; 	  AH - param, word length loop counter
;	  CL - global, latch counter
;   	  CH - global, latch value
;         DX - (free)
;         SI - local, 5-byte rotation
;         DI - local, 5-byte rotation
;	  BP - global, load data pointer
;	  ES - (free)
;
;       Method 1:
;	  BX - local, xlat table
;       Method 2:
;         BH - local, data sub correction
;-----------------------------------------------------------------------
	org 	100H

	mov 	al,3fH
	mov 	dx,331H
	out 	dx,al
	mov	ax,13H
	int	10H

	call	init_newline

	lea	bp,[data_notes]
	xor	ch,ch

	call	print_newline

@next_note:

	call	load_note

	call	print_note
	jmp	@nplay

	call	play_note
	mov	al,6
	call	delay

@nplay:
	inc	byte [counter]
	cmp	byte [counter],20
	jne	@next_note

	int	20H

counter:
	db 0
;-----------------------------------------------------------------------
load_note:
	xor	al,al
	mov	cl,$20	 	; %00100000: 3 shift-left from zero
	mov	bl,DATA_CSUB

@next_bit:
	or	cl,cl
	jnz	@shift_latch

	mov	ch,[bp]
	inc	bp

@shift_latch:
	sal	cx,1
	sal	al,1
	adc	al,0

	or	cl,cl
	jnz	@shift_latch

	or	al,al		; check for %000 special value
	jnz	@shift_done

	mov	cl,$03		; %00000010: 7 shift-left from zero
	mov	bl,DATA_USUB
	jmp	@next_bit

@shift_done:
	add	al,bl

@rotate:
	lea	di,[data_start]
	add	al,[di]
	lea	si,[di + 1]

	movsw
	movsw
	stosb

	ret
;-----------------------------------------------------------------------
play_note: ; parm: AH, local: AL, BH, DX

	mov	bh,90H		; Note On, Channel 1
	call	play_byte

	mov	bh,ah		; Pitch
	call	play_byte

	mov	bh,7fH		; Velocity
	call	play_byte

	ret
;-----------------------------------------------------------------------
play_byte:

	mov	dx,331H
	in	al,dx
	test	al,40H
	jnz	play_byte

	dec	dx
	mov	al,bh
	out	dx,al

	ret
;-----------------------------------------------------------------------
delay:
	pusha

	xor	ch,ch
	mov	cl,al

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

	popa
	ret
;-----------------------------------------------------------------------
include "dump.asm"
include "data-2.inc"
