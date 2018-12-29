; note data and diff data for test

test_note_data:
	db 60,64,67,72,76,67,72,76
	db 60,64,67,72,76,67,72,76
	db 60,62,69,74,77,69,74,77
	db 60,62,69,74,77,69,74,77
	db 59,62,67,74,77,67,74,77
	db 59,62,67,74,77,67,74,77
	db 60,64,67,72,76,67,72,76
	db 60,64,67,72,76,67,72,76
	db 60,64,69,76,81,69,76,81
	db 60,64,69,76,81,69,76,81
	db 60,62,66,69,74,66,69,74
	db 60,62,66,69,74,66,69,74
	db 59,62,67,74,79,67,74,79
	db 59,62,67,74,79,67,74,79
	db 59,60,64,67,72,64,67,72
	db 59,60,64,67,72,64,67,72
	db 57,60,64,67,72,64,67,72
	db 57,60,64,67,72,64,67,72
	db 50,57,62,66,72,62,66,72
	db 50,57,62,66,72,62,66,72
	db 55,59,62,67,71,62,67,71
	db 55,59,62,67,71,62,67,71
	db 55,58,64,67,73,64,67,73
	db 55,58,64,67,73,64,67,73
	db 53,57,62,69,74,62,69,74
	db 53,57,62,69,74,62,69,74
	db 53,56,62,65,71,62,65,71
	db 53,56,62,65,71,62,65,71
	db 52,55,60,67,72,60,67,72
	db 52,55,60,67,72,60,67,72
	db 52,53,57,60,65,57,60,65
	db 52,53,57,60,65,57,60,65
	db 50,53,57,60,65,57,60,65
	db 50,53,57,60,65,57,60,65
	db 43,50,55,59,65,55,59,65
	db 43,50,55,59,65,55,59,65
	db 48,52,55,60,64,55,60,64
	db 48,52,55,60,64,55,60,64
	db 48,55,58,60,64,58,60,64
	db 48,55,58,60,64,58,60,64
	db 41,53,57,60,64,57,60,64
	db 41,53,57,60,64,57,60,64
	db 42,48,57,60,64,57,60,64
	db 42,48,57,60,64,57,60,64
	db 44,53,59,60,62,59,60,62
	db 44,53,59,60,62,59,60,62
	db 43,53,55,59,62,55,59,62
	db 43,53,55,59,62,55,59,62
	db 43,52,55,60,64,55,60,64
	db 43,52,55,60,64,55,60,64
	db 43,50,55,60,65,55,60,65
	db 43,50,55,60,65,55,60,65
	db 43,50,55,59,65,55,59,65
	db 43,50,55,59,65,55,59,65
	db 43,51,57,60,66,57,60,66
	db 43,51,57,60,66,57,60,66
	db 43,52,55,60,67,55,60,67
	db 43,52,55,60,67,55,60,67
	db 43,50,55,60,65,55,60,65
	db 43,50,55,60,65,55,60,65
	db 43,50,55,59,65,55,59,65
	db 43,50,55,59,65,55,59,65
	db 36,48,55,58,64,55,58,64
	db 36,48,55,58,64,55,58,64
	db 36,48,53,57,60,65,60,57
	db 60,57,53,57,53,50,53,50
	db 36,47,67,71,74,77,74,71
	db 74,71,67,71,62,65,64,62
	db 36,48,64,67,72

test_diff_data:
	db 0,0,0,0,0
	db 0,0,0,0,0
	db 0,-2,2,2,1
	db 0,-2,2,2,1
	db -1,0,-2,0,0
	db -1,0,-2,0,0
	db 1,2,0,-2,-1
	db 1,2,0,-2,-1
	db 0,0,2,4,5
	db 0,0,2,4,5
	db 0,-2,-3,-7,-7
	db 0,-2,-3,-7,-7
	db -1,0,1,5,5
	db -1,0,1,5,5
	db 0,-2,-3,-7,-7
	db 0,-2,-3,-7,-7
	db -2,0,0,0,0
	db -2,0,0,0,0
	db -7,-3,-2,-1,0
	db -7,-3,-2,-1,0
	db 5,2,0,1,-1
	db 5,2,0,1,-1
	db 0,-1,2,0,2
	db 0,-1,2,0,2
	db -2,-1,-2,2,1
	db -2,-1,-2,2,1
	db 0,-1,0,-4,-3
	db 0,-1,0,-4,-3
	db -1,-1,-2,2,1
	db -1,-1,-2,2,1
	db 0,-2,-3,-7,-7
	db 0,-2,-3,-7,-7
	db -2,0,0,0,0
	db -2,0,0,0,0
	db -7,-3,-2,-1,0
	db -7,-3,-2,-1,0
	db 5,2,0,1,-1
	db 5,2,0,1,-1
	db 0,3,3,0,0
	db 0,3,3,0,0
	db -7,-2,-1,0,0
	db -7,-2,-1,0,0
	db 1,-5,0,0,0
	db 1,-5,0,0,0
	db 2,5,2,0,-2
	db 2,5,2,0,-2
	db -1,0,-4,-1,0
	db -1,0,-4,-1,0
	db 0,-1,0,1,2
	db 0,-1,0,1,2
	db 0,-2,0,0,1
	db 0,-2,0,0,1
	db 0,0,0,-1,0
	db 0,0,0,-1,0
	db 0,1,2,1,1
	db 0,1,2,1,1
	db 0,1,-2,0,1
	db 0,1,-2,0,1
	db 0,-2,0,0,-2
	db 0,-2,0,0,-2
	db 0,0,0,-1,0
	db 0,0,0,-1,0
	db -7,-2,0,-1,-1
	db -7,-2,0,-1,-1
	db 0,0,-2,-1,-4,29,12,4
	db 3,-3,-12,-3,-4,-10,-4,-3
	db -21,-6,17,18,24,41,27,4
	db 3,-3,-10,-3,-9,-9,-7,-5
	db -35,-14,-1,3,10