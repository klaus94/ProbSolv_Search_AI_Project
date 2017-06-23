

def aspParse(machine_count, jobs):
	prog = ""
	prog += "machine(0.." + str(machine_count-1) + ").\n"
	prog += "time(0.." + "100).\n"

	currentJob = 0
	currentSubjob = 0
	for job in jobs:
		currentJob += 1
		for subjob in job:
			currentSubjob += 1
			prog += "subjob({0}, {1}, {2}, {3}).\n".format(str(currentSubjob), str(subjob[1]), str(subjob[0]), currentJob)

	prog += "{exec(M, T, J) : time(T), subjob(J, _, M, _)}.\n"

	for i in range(currentSubjob):
		prog += "1{exec(M, T, " + str(i+1) + "):machine(M), time(T), subjob(" + str(i+1) + ", _, M, _)}1.\n"

	prog += ":- exec(M, T1, I1), exec(M, T2, I2), subjob(I1, L, M, _), subjob(I2, _, M, _), I1 < I2, T1 + L > T2.\n"
	prog += ":- exec(_, T2, J2), exec(_, T1, J1), subjob(J1, L, _, N), subjob(J2, _, _, N), J1 < J2, T1+L > T2.\n"
	prog += "#minimize { T, L : exec(_, T, J), subjob(J, L, _, _), time(T)}.\n"
	prog += "#show exec/3.\n"

	return prog