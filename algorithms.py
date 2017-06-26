import aspParser
import evolSolver
import sys
import os

# IN: (machine_count, [job1, job2, job3, ...])
#	->	job... [(machineNr, time), (machineNr, time), ...]
#
# OUT: [jobs_on_machine1, jobs_on_machine2, jobs_on_machine3, ...]
#	->	job_on_machine... [(begin, length, jobNr), (begin, length, jobNr), (begin, length, jobNr)]


# work sequentially on jobs
# -> complete all tasks of job1, before beginning job2 and so on...
def baseLineAlg(machine_count, jobs):
	t = 0
	currentJobNr = 0
	machine_jobs = [[] for x in range(machine_count)]

	for job in jobs:
		for task in job:
			machine_jobs[task[0]].append((t, task[1], currentJobNr))
			t += task[1]

		currentJobNr += 1

	return machine_jobs


def asp(machine_count, jobs):
	prog, allJobs = aspParser.aspParse2ASP(machine_count, jobs)
	# print prog
	prog_file = open("genProg.lp", "w")
	prog_file.write(prog)
	prog_file.close()


	LOG_FILE_NAME = "log"
	# todo: execute gringo
	os.system("gringo genProg.lp | clasp > " + LOG_FILE_NAME)

	# todo: evaluage output and parse solution back into solution object
	log_file = open(LOG_FILE_NAME, "r")
	log = log_file.read()
	print log
	log_file.close()

	solution = aspParser.aspParseFromASP(machine_count, allJobs, log)
	
	return solution

def evol(machine_count, jobs):
	return evolSolver.solve(machine_count, jobs)