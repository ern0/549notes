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
;	  AL - param, result: loaded word on LSBs
; 	  AH - param, word length loop counter (SHL until zero)
;         BL - local, play_note
;         BH - local, data sub correction
;	  CL - global, latch counter (SHL until zero)
;   	  CH - global, latch value
;         DX - (free)
;         SI - local, 5-byte rotation
;         DI - local, 5-byte rotation
;	  BP - global, load data pointer
;	  ES - (free)
;
;-----------------------------------------------------------------------
	org 	100H

	mov 	al,3fH
	mov 	dx,331H
	out 	dx,al

	call	init_newline

	lea	bp,[data_notes]
	xor	cl,cl

	call	print_newline

@next_note:

	call	load_note
	call	print_note
 jmp @nplay
	call	play_note

@nplay:
	inc	byte [counter]
	cmp	byte [counter],10
	jne	@next_note

	int	20H

counter:
	db 0
delay:
	dw 5
;#######################################################################
load_note:
	mov	bl,DATA_CSUB
	mov	ax,$2000 	; AL:=0, AH:=%xx10'0000: 3 SHL from zero

@next_bit:
	or	ah,ah
	jnz	@read_bit

;word_read:
	or	al,al		; check for %000 special value
	jnz	@adjust_word

;load_uncompressed:
	mov	bl,DATA_USUB	; 42, also a good value for bit counter
	mov	ah,bl		; %xxxx'xx10: 7 SHL from zero
	jmp	@next_bit

@read_bit:
	or	cl,cl
	jnz	@shift_latch

;load_latch:
	inc	cx		; 1-byte CL:=1 instr, %xxxx'xxx1: 8 SHL from zero
	mov	ch,[bp]
	inc	bp

@shift_latch:
	sal	ax,1
	sal	cx,1
	adc	al,0

	jmp	@next_bit

@adjust_word:
	sub	al,bl

;rotate_notes:
	lea	di,[data_start]
	add	al,[di]
	lea	si,[di + 1]

	movsw
	movsw
	stosb

	ret
;-----------------------------------------------------------------------
play_byte:
	mov	dx,331H
	in	al,dx
	test	al,40H
	jnz	play_byte

	dec	dx
	mov	al,bl
	out	dx,al

	ret
;-----------------------------------------------------------------------
play_note: ; parm: AL, local: AL, BL, DX

	pusha

	push	ax
	mov	bl,90H		; Note On, Channel 1
	call	play_byte

	pop	bx		; Pitch
	call	play_byte

	mov	bl,7fH		; Velocity
	call	play_byte

	; fall delay

;-----------------------------------------------------------------------
;delay:
	mov	si,[delay]

@wait_some:
	mov	ah,2cH
	int	21H
	mov	bl,dl

@wait_tick:
	int	21H
	cmp	bl,dl
	je	@wait_tick
	dec	si
	jne	@wait_some

	popa
	ret
;-----------------------------------------------------------------------
include "dump.asm"
include "data-2.inc"
