
def aspParse2ASP(machine_count, jobs):
	allJobs = {}		# key: subjob-index, value: (length, machine, job-index)

	prog = ""
	prog += "machine(0.." + str(machine_count-1) + ").\n"
	prog += "time(0.." + "200).\n"

	currentJob = 0
	currentSubjob = 0
	for job in jobs:
		currentJob += 1
		for subjob in job:
			currentSubjob += 1
			prog += "subjob({0}, {1}, {2}, {3}).\n".format(str(currentSubjob), str(subjob[1]), str(subjob[0]), currentJob)
			allJobs[currentSubjob] = (subjob[1], subjob[0], currentJob)

	prog += "{exec(M, T, J) : time(T), subjob(J, _, M, _)}.\n"

	for i in range(currentSubjob):
		prog += "1{exec(M, T, " + str(i+1) + "):machine(M), time(T), subjob(" + str(i+1) + ", _, M, _)}1.\n"

	prog += ":- exec(M, T1, I1), exec(M, T2, I2), subjob(I1, L, M, _), subjob(I2, _, M, _), I1 < I2, T1 + L > T2.\n"
	prog += ":- exec(_, T2, J2), exec(_, T1, J1), subjob(J1, L, _, N), subjob(J2, _, _, N), J1 < J2, T1+L > T2.\n"
	prog += "#minimize { T, L : exec(_, T, J), subjob(J, L, _, _), time(T)}.\n"
	prog += "#show exec/3.\n"

	return prog, allJobs


# IN: (machine_count, [job1, job2, job3, ...])
#	->	job... [(machineNr, time), (machineNr, time), ...]
#
# OUT: [jobs_on_machine1, jobs_on_machine2, jobs_on_machine3, ...]
#	->	job_on_machine... [(begin, length, jobNr), (begin, length, jobNr), (begin, length, jobNr)]


# return jobs = [(subjob1, time), (subjob2, time), (subjob3, time), ....]
def aspParseFromASP(machineCount, allJobs, log):
	jobs = []
	lines = log.split("\n")

	lineOfInterest = ""
	for i in range(len(lines)):
		if ("OPTIMUM FOUND" in lines[i]):
			lineOfInterest = lines[i-2]
	
	if (lineOfInterest == ""):
		return []

	for job in lineOfInterest.split(" "):
		# job has the form: "exec(1,1,1)"
		jobEdited = job.replace("exec(", "").replace(")", "").split(",")

		# jobEdited has the form: ["1","1","1"]
		jobs.append((int(jobEdited[2]), int(jobEdited[1])))

	# jobs has form: [(subjob1, time), (subjob2, time), (subjob3, time), ...]

	solution = [[] for m in range(machineCount)]
	for job in jobs:
		for key in allJobs.keys():
			if (job[0] == key):				# match with subjob-key
				currentJob = allJobs[key]
				print currentJob[1]
				print solution[currentJob[1]]
				solution[currentJob[1]].append((job[1], currentJob[0], currentJob[2]))

	return solution
