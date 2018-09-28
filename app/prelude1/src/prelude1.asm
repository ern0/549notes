;#######################################################################
; Prelude1 - PC-DOS 256-byte intro by ern0
; Created 2018.09.28, released: N/A
;
; This program plays
;  J.S.Bach: Prelude in C major, BWV 846
;  from the Prelude and Fugue in C major, BWV 846
;  from Book I of The Well-Tempered Clavier
; on the MIDI interface
;
; Target: 80386 real mode, assembler: TASM
;
;-----------------------------------------------------------------------
; Data decoding example (only some bytes from the start)
;
;   line 1: encoded data bytes ($2A, $4A...)
;   line 2: ruler for converting hexadecimal values to binary
;   line 3: encoded data binary values
;     - byte boundary: "|"
;     - word (3-bit/5-bit) boundary: "/"
;     - 3-bit special marker and 5-bit word separator: "*"
;   line 4:
;     - index: value of the word (3-bit/5-bit)
;       if the 3-bit word is 0, the value of the index is the
;       next 5-bit word, and tab5 shold be used instead of tab3
;       (5-bit index values are marked with "*")
;     - separator: ":"
;     - diff: lookup value from tab3/tab5 using index value
;       - note that tab3's first element is missing (index is never 0)
;         so first element of tab3 (at offset 0) belongs to index=1
;       - note that tab5's first element is never used (index is never 0)
;         in order to re-enter bit reader routine with CL=5

;
;   $2A               $4A               $CA
;   8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 |
; % 0 0 1/0 1 0/1 0 | 0/1 0 0/1 0 1/0 | 1 1/0 0 1/0 1 0/|
;   1:=0  2:-2   4:+2   4:+2  5:+1   3:-1   1:=0  2:-2
;
;   $26               $C2               $99
;   8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 |
; % 0 0 1/0 0 1/1 0 | 1/1 0 0/0 0 1/0 | 1 0/0 1 1/0 0 1/|
;   1:=0  1:=0   5:+1   4:+2  1:=0   2:-2   3:-1  1:=0
;
;   $30               $10               $04
;   8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 |
; % 0 0 1/1 0 0/0 0 | 0*0 0 1 0 0/0 0 | 0*0 0 0 0 1/0 0 |(1)/
;   1:=0  4:+2  [5-bit]  *4:+04   [5-bit]  *1:+05      1:0
;
;   $AF               $B3               $34
;   8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 |
; % 1/0 1 0/1 1 1/1 | 1 0/1 1 0/0 1 1/| 0 0 1/1 0 1/0 0 |(0)*
;     2:-2  7:-3   6:-7   6:-7  3:-1    1:=0  5:+1  [5-bit]
;
;   $04               $04               $85               $7D
;   8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8 4 2 1 8 4 2 1 | 8...
; % 0*0 0 0 0 1/0 0 | 0*0 0 0 0 1/0 0 | 1/0 0 0/0 1 0 1 | 0/...
;      *1:+05   [5-bit]   *1:+05   1:=0  [5-bit]  *10:+10 ...
;
;-----------------------------------------------------------------------
; Register allocation:
;
;	SI - note counter
; 	BP - load data pointer
; 	CH - latch counter
;	CL - word length loop (3 or 5)
; 	AH - latch value
;	AL - result word (on LSBs)
;	BX - table3 or table5 for xlat
;#######################################################################
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
	xor	si,si

@next_note:
	
	call	load_note
	
	mov	cl,al
	call	play_note

	mov	al,6
	call	delay

	inc	si
	cmp	si,202 - 5
	jne	@next_note

	int	20H

;#######################################################################
load_note:

	lea	bx,[tab3 - 1]
	mov	cl,3
;-----------------------------------------------------------------------
@read_word_cl:		; read CL-bit (3 or 5) word
	xor	al,al
@next_bit:
	or	ch,ch
	jnz	@shift_from_latch

	mov	ah,[bp]	; load byte to latch
	inc	bp
	mov	ch,8

@shift_from_latch:
	dec	ch
	sal	ax,1		; CF << AH MSB and shift left AL by 1
	adc	al,0		; AL LSB << CF (AL is already shifted)

	dec	cl
	jne	@next_bit

	or	al,al		; check for %000 special value
	jnz	@read_word_done

	add	bl,(tab5 - tab3) ; lea bx,[tab5 - 1]
	mov	cl,5
	jmp	@read_word_cl

;-----------------------------------------------------------------------
@read_word_done:

	xlatb

;-----------------------------------------------------------------------

	lea	di,[data_start]
	add	al,[di]

	mov	edx,[di + 1]
	mov	[di],edx

	mov	[di + 4],al

	ret

;#######################################################################
play_note:
	pusha

	mov	ah,90H		; Note On, Channel 1 
	call	play_byte

	mov	ah,cl		; Pitch
	call	play_byte

	mov	ah,7fH		; Velocity
	call	play_byte

	popa
	ret
;-----------------------------------------------------------------------
play_byte:

	mov	dx,331H
	in	al,dx
	test	al,40H
	jnz	play_byte

	dec	dx
	mov	al,ah
	out	dx,al

	ret
;#######################################################################
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
include "score.inc"
include "dump.inc"
