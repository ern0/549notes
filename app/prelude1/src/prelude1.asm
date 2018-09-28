;-----------------------------------------------------------------------
; Prelude1 - PC-DOS 256-byte intro by ern0
; Created 2018.09.28, released: N/A
;
; This program plays
;  J.S.Bach: Prelude in C major, BWV 846
;  from the Prelude and Fugue in C major, BWV 846
;  from Book I of The Well-Tempered Clavier
; on the MIDI interface
;
; Target: 80186/80286, assembler: TASM
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

;-----------------------------------------------------------------------
; Register allocation:
;
; 	BP - bit read data pointer
; 	CH - bit read latch counter
;	CL - bit read loop (3 or 5)
; 	AH - bit read latch value
;	AL - bit read result
;	BX - table3 or table5 for xlat
;-----------------------------------------------------------------------
	org 	100H

	mov	ax,13H
	int	10H

	call	init_newline

	lea	bp,[data_notes]
	xor	ch,ch

	call	print_newline
	mov	si,20

@next_note:
	lea	bx,[tab3 - 1]
	mov	cl,3
	call	read_bits
	or	al,al
	jne	@bits_read

	lea	bx,[tab5 - 1]
	mov	cl,5
	call	read_bits
@bits_read:
	xlatb
	call	print_diff

	dec	si
	jne	@next_note

	mov	ax,4c00H
	int	21H

read_bits:

	xor	al,al
@xbit:
	call	read_one_bit
	dec	cl
	jne	@xbit
	ret

read_one_bit:

	or	ch,ch
	jnz	@shift

	mov	ah,[bp]
	inc     bp
	mov	ch,8

@shift:
	dec	ch
	sal	ax,1		; CF << AH MSB and prepare AL by SHL
	adc	al,0		; AL LSB << CF (AL is already shifted)

	ret
;-----------------------------------------------------------------------
include "score.inc"
include "dump.inc"
