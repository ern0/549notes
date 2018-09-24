;%define		C2		0x30
;%define		C2x		0x31
;%define		D2		0x32
;%define		D2x		0x33
;%define		E2		0x34
;%define		F2		0x35
;%define		F2x		0x36
;%define		G2		0x37
;%define		G2x		0x38
;%define		A2		0x39
%define		A2x		(0x3A-0x39)
;%define		B2		0x3B

%define		C3		(0x3C-0x39)
%define		C3x		(0x3D-0x39)
;%define		D3		0x3E
%define		D3x		(0x3F-0x39)
;%define		E3		0x40
%define		F3		(0x41-0x39)
;%define		F3x		0x42
;%define		G3		0x43
%define		G3x		(0x44-0x39)
;%define		A3		0x45
;%define		A3x		0x46
;%define		B3		0x47

org 0x100
	xor bp,bp
	
	xchg cx,ax
	mov dx,music			
	mov ax,0x251C
	int 0x21
	
	mov	ax,13h
	int	10h
	push 0a000h
	pop	es

	mov si,data
;	mov [si+8],word 0
mainloop:
	mov ch,0xfa
tunnelloop:		
		xor dx,dx
		mov bx,320
		mov ax,di
		div bx
		sub ax,100
		sub dx,160
		
		mov	[si],dx
		fild	word [si]
		mov	[si],ax
		fild	word [si]
		fpatan
		mov	word [si],256
		fimul	word [si]
		fldpi
		fdivp	st1,st0

		fistp	word [si+4]
		
		mov [si],word 32*256
		fild	word [si]			;[si+1]
		mov	[si],ax
		fild	word [si]
		fmul	st0,st0
		mov	[si],dx
		fild	word [si]
		fmul	st0,st0
		faddp	st1,st0
		fsqrt
		fdivp	st1,st0
		fistp	word [si]

		mov		ax,[si]
		add		ax,bp
		mov		dx,[si+4]

		test	bp,256
		jz		r1
		add		dx,bp		;counter
r1:
		xor		ax,dx
	
		;and		al,128+64+4
		;and		al,64+32+8		;ok
		;and		al,8			;checkerboard

		and		al,128+32+8+1
		test	bp,512
		jnz		t1
		and		al,128+32+1
	
t1:		
		test	bp,1024
		jz		t2
		and		al,32+1
;		mov		byte [sample+1], 36
t2:
		stosb
		loop tunnelloop

		cmp bp,1024+128
		ja q
		
		in	al,60h
		dec	al
		jnz	mainloop

q:		
		mov	ax,3
		int	10h

off:
;	mov si,midi_off
;	mov dx,330h
;	outsb
;	outsb
;	outsb
	ret

music:
;	pusha
	inc bp
	test bp,word 00000011b
	jnz nomusic

	mov 	dx,0x331		; MIDI Control Port
	mov	al,3fh
	out dx,al
	dec 	dx				; switch to MIDI data port

;%ifdef drum
	test bp,word 256
	jna nodrum
	test bp,word 00000111b
	jz nodrum

	mov al,99h
	out dx,al
	mov	al,35			;35=bass, 42=cin
	out	dx,al			; send the drum
	mov	al,127			; set volume to maximum
	out	dx,al			; send volume
;%endif

nodrum:
	mov		al,0c0h
	out		dx,al

sample:	
	mov		al,39		;38
	out		dx,al
	mov		al,90h
	out		dx,al

	push	bp
	shr		bp,2
	and		bp,63
	shr		bp,1
	mov		al,[lead+bp]
	pop		bp

	test	bp,word 00111b
	jz		jj
	shr		al,4
jj:
	and		al,15
	jz		jjj
	add		al,0x39
jjj:
	out		dx,al
	mov		al,127
	out		dx,al
	
;	inc 	dx				; switch to control port
;	outsb					; change to mode "UART"

;mov 	al,	3Fh		;	set UART mode - command
;mov 	dx,	331h	;	MIDI Control Port
;out 	dx,	al 		;	send !

nomusic:
;	inc bp
;	popa
	iret

	
lead:
;db	 F3,  0, F3,  0,G3x,  0,G3x, C3,
;db	  0, C3, C3,  0, C3,  0, C3,  0,
;db	C3x,  0,C3x,  0,C3x,  0,C3x,D3x,
;db	  0,D3x,D3x,  0,D3x,  0,D3x,  0,
;db	 F3,  0, F3,  0,G3x,  0,G3x, C3,
;db	  0, C3, C3,  0, C3,  0, C3,  0,
;db	C3x,  0,C3x,  0,C3x,  0,C3x,A2x,
;db	  0,A2x,A2x,  0,D3x,  0,D3x,  0,

db	 F3+  0*16, F3+  0,G3x+  0,G3x+ C3*16,
db	  0+ C3*16, C3+  0, C3+  0, C3+  0*16,
db	C3x+  0*16,C3x+  0,C3x+  0,C3x+D3x*16,
db	  0+D3x*16,D3x+  0,D3x+  0,D3x+  0*16,
db	 F3+  0*16, F3+  0,G3x+  0,G3x+ C3*16,
db	  0+ C3*16, C3+  0, C3+  0, C3+  0*16,
db	C3x+  0*16,C3x+  0,C3x+  0,C3x+A2x*16,
db	  0+A2x*16,A2x+  0,D3x+  0,D3x+  0*16,

midi_off:
;db		3fh				; change mode to "UART"
;db		0b0h			; control change on channel 3
;db		123				; Channel Mode Message "All Notes Off"

data:
;			dw 0,0,0,0,0,0,0,0