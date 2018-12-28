;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Prototype-2: raw-diff-5 nctab nutab
;
; Target: 80386 real mode, assembler: FASM
;
;-----------------------------------------------------------------------
; Register allocation:
;
;	AL - param, result: loaded word on LSBs
;	AH - param, word length loop counter (SHL until zero)
;	BL - local, play_note
;	BH - local, data sub correction
;	CL - global, latch counter (SHL until zero)
;	CH - global, latch value
;	DX - (free)
;	SI - local, 5-byte rotation
;	DI - global, 5-byte rotation, used in 5+3 repeat
;	BP - global, load data pointer
;	ES - (free)
;
;-----------------------------------------------------------------------
        TEST_MODE = 1

        if TEST_MODE > 0
        display "----[ Test mode, result will be written to TEST-2.TXT ]--------"
        end if
;-----------------------------------------------------------------------
	org 	100H

	mov 	al,3fH
	mov 	dx,331H
	out 	dx,al

	lea	bp,[data_notes]
	xor	cl,cl

@next_line:
	
	pusha
	push	cx
	lea	si,[data_start]
	lea	di,[snapshot_start]
	mov	cx,5
	rep	movsb
	pop	cx

	call	eight_of_eight

	lea	si,[snapshot_start]
	lea	di,[data_start]
	mov	cx,5
	rep	movsb
	popa

	call	eight_of_eight

	cmp	byte [line],2
	jne	@not1
	mov	byte [delay],5
@not1:
	dec	byte [line]
	jne	@next_line

	mov	byte [delay],6
	mov	byte [line],16
@next_simple:
	call	load_play_note
	dec	byte [line]
	jne	@next_simple

	mov	byte [delay],7
	mov	byte [line],16
@next_last:
	call	load_play_note
	dec	byte [line]
	jne	@next_last

	mov	byte [delay],1
	mov	byte [line],5
@next_finish:
	call	load_play_note
	dec	byte [line]
	jne	@next_finish

	if TEST_MODE > 0
	call    test_summary
	end if

	int	20H

line:
	db 32
delay:
	dw 5
snapshot_start:
	db 0,0,0,0,0
;-----------------------------------------------------------------------
eight_of_eight:

	mov	dx,5
@five_of_eight:
	call	load_play_note
	dec	dx
	jnz	@five_of_eight

	mov	bx,-3
@three_of_eight:
	mov	al,[di + bx]		; DI is from rotate_notes
	call	play_note
	inc	bx
	jnz	@three_of_eight

	ret
;-----------------------------------------------------------------------
load_play_note:
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
	inc	cx		; INC CX for CL:=1, %xxxx'xxx1: 8 SHL from zero
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

	if TEST_MODE > 0
	call	test_diff
	end if

	lea	di,[data_start]
	add	al,[di]
	lea	si,[di + 1]

	movsw
	movsw
	stosb

	; fall play_note
;-----------------------------------------------------------------------
play_note:

	if TEST_MODE > 0
	jmp	test_note
	end if
	
@ply:
	pusha

	push	ax
	mov	bl,90H		; Note On, Channel 1
	call	play_byte

	pop	bx		; Pitch
	call	play_byte

	mov	bl,7fH		; Velocity
	call	play_byte

	; fall wait
;-----------------------------------------------------------------------
;wait:
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
include "data-2.inc"

if TEST_MODE > 0
include "test.asm"
include "test-2.inc"
test_file_name:
	db	"TEST-2.TXT",0
end if
