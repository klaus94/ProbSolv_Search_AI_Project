import random as rand

# IN: (machine_count, [job1, job2, job3, ...])
#	->	job... [(machineNr, time), (machineNr, time), ...]
#
# OUT: [jobs_on_machine1, jobs_on_machine2, jobs_on_machine3, ...]
#	->	job_on_machine... [(begin, length, jobNr), (begin, length, jobNr), (begin, length, jobNr)]

# representation of a solution:
# [subjobNr1 length1 subjobNr2 length2 subjobNr3 lenth3, ...]
# there must be a maximum time for tasks on one machine 
# -> when the sum of the subjobs lengths reach this maximum time this tells us
# that now the jobs of the next machine are starting
# jobNr "-1" means: no job in this time
# [(4 1) (-1 2) (2 2) (3 1)] (max-time = 3)... would mean: on machine 0: job4(1), noJob(2); machine 1: job2(2), job3(1) 

# hyper-parameters
POPULATION_SIZE = 10
EPOCHS = 1000
MaximumTime = 100		# will be later replaced by a better approximation of the max length
JobDict = {}			# holds the dicionary {job1: [subjob1, subjob2, ..], job2: [..]}

def solve(machine_count, jobs):
	population = init(machine_count, jobs, POPULATION_SIZE)			# list of solutions
	print population[0]
	print get_moving_range(population[0], 6)
	# evaluation = eval_all(population)

	# time = 0
	# while time < EPOCHS:
	# 	time += 1
	# 	(mum, dad) = selectParents(evaluation, population)
	# 	offspring = recombine(mum, dad)
	# 	offspring += mutate(mum, dad)
	# 	evaluation = eval_all(offspring)
	# 	population = select_population(evaluation, offspring)

	# return population



# helper methods

def init(machine_count, jobs, population_size):
	global JobDict

	# produce basline solution by executing all jobs sequentially
	currentJobNr = 0
	currentSubjobNr = 1
	for j in range(len(jobs)):
		JobDict[j] = []

	seqSolution = [[] for m in range(machine_count)]
	for job in jobs:
		for subjob in job:
			for i in range(machine_count):
				if (i == subjob[0]):
					seqSolution[i].append((currentSubjobNr, subjob[1]))		# [[(subjobNr1, length1), (subjobNr2, length2), ...], [..]]
				else:
					seqSolution[i].append((-1, subjob[1]))			# append -1 for all other machines

			JobDict[currentJobNr].append(currentSubjobNr)		# job: [subjobNr1, subjobNr2, ..]
			currentSubjobNr += 1
		currentJobNr += 1

	seqSolution = summarize_null_jobs(seqSolution)

	# generate population from sequential solution
	solutions = []
	solutions.append(seqSolution)
	for i in range(POPULATION_SIZE-1):
		solutions.append(mutate(seqSolution))

	return solutions

def selectParents(evaluation, population):
	pass

def recombine(solution1, solution2):
	pass

# generate new solution from given solution (indeterministic)
def mutate(solution):


	return solution

def eval_all(evaluation, offspring):
	pass

def select_population(offspring):
	pass


########## HELPER METHODS ###########

# return a tuple (left, right) that indicates, how much the subjob can move along the time-axis back and forth
def get_moving_range(solution, subjobNr):
	# get range on machine (other subjobs on same machine)
	range1 = (0, 0)
	memNullJobLength = 0						# counts the "-1"-jobs - length
	foundSubjobOfInterest = False
	for machineJobs in solution:
		if (foundSubjobOfInterest):
			break

		for i in range(len(machineJobs)):
			if (machineJobs[i][0] == subjobNr):
				foundSubjobOfInterest = True
				left = memNullJobLength
				right = 0													# right = right edge of interesting subjob
				i += 1														# go to next subjob
				while i < len(machineJobs) and machineJobs[i][0] == -1:		# sum up all "-1"-jobs right of interesting subjob
					right += machineJobs[i][1]
					i += 1
				if (i >= len(machineJobs)):
					right = 1000000							# free space on the right side
				range1 = (left, right)
				break

			if (machineJobs[i][0] == -1):									# here is a "-1"-job
				memNullJobLength += machineJobs[i][1]
			else:															# here is a normal subjob
				memNullJobLength = 0

	# get range within global job (other subjobs in same job)
	range2 = (0, 0)
	foundSubjobOfInterest = False
	for jobNr in JobDict.keys():
		if (foundSubjobOfInterest):
			break

		for i in range(len(JobDict[jobNr])):
			if (JobDict[jobNr][i] == subjobNr):
				left = 0
				right = 10000000			# not important -> big number
				beginInterestingJob = get_begin(solution, subjobNr)
				if (i > 0):
					left = beginInterestingJob - (get_begin(solution, JobDict[jobNr][i-1]) + get_subjob(solution, JobDict[jobNr][i-1])[1])
				if (i < len(JobDict[jobNr])-1):
					endInteresingJob = beginInterestingJob + get_subjob(solution, subjobNr)[1]
					right = get_begin(solution, JobDict[jobNr][i+1]) - endInteresingJob

				range2 = (left, right)
				foundSubjobOfInterest = True
				break

	print "within machine", range1
	print "within job", range2
	return (min(range1[0], range2[0]), min(range1[1], range2[1]))

def get_begin(solution, subjobNr):
	for machineJobs in solution:
		time = 0
		for subjob in machineJobs:
			if (subjob[0] == subjobNr):
				return time
			time += subjob[1]

def get_subjob(solution, subjobNr):
	for machineJobs in solution:
		for subjob in machineJobs:
			if (subjob[0] == subjobNr):
				return subjob


def summarize_null_jobs(solution):
	niceSolution = [[] for i in range(len(solution))]

	for m in range(len(solution)):
		memNullJobLength = 0
		for subjob in solution[m]:
			if (subjob[0] == -1):
				memNullJobLength += subjob[1]
			else:
				if (memNullJobLength > 0):
					niceSolution[m].append((-1, memNullJobLength))
					memNullJobLength = 0
				niceSolution[m].append(subjob)

	return niceSolution

