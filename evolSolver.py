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
EPOCHS =100
PROP_CHANGE_VS_MOVE = 0.9

MaximumTime = 100		# will be later replaced by a better approximation of the max length
JobDict = {}			# holds the dicionary {job1: [subjob1, subjob2, ..], job2: [..]}


def solve(machine_count, jobs):
	population = init(machine_count, jobs, POPULATION_SIZE)			# list of solutions
	evaluation = eval_all(population)

	time = 0
	while time < EPOCHS:
		print "Epoch: " + str(time)
		time += 1
		(mum, dad) = selectParents(evaluation, population)

		# offspring = recombine(mum, dad)
		offspring = []
		for i in range(POPULATION_SIZE):		# generate twice as meny solutions as needed for a population
			offspring.append(mutate(dad))
			offspring.append(mutate(mum))

		evaluation = eval_all(offspring)
		population = select_population(evaluation, offspring)


	evaluation = eval_all(population)
	bestSolutionIdx = evaluation.index(min(evaluation))
	bestSolution = population[bestSolutionIdx]

	return out(bestSolution)



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
		solutions.append(summarize_null_jobs(mutate(seqSolution)))

	return solutions

def selectParents(evaluation, population):
	# first take two random parents
	solution1 = rand.choice(population)
	solution2 = rand.choice(population)

	return (solution1, solution2)

def recombine(solution1, solution2):
	pass

# generate new solution from given solution (indeterministic)
def mutate(solution):
	foundMutation = False
	while not foundMutation:
		randMachineJobs = rand.choice(solution)
		randSubjob = rand.choice(randMachineJobs)
		resultSolution = None
		if (rand.random() > PROP_CHANGE_VS_MOVE):
			resultSolution = changeSubjobs(solution, randMachineJobs, randSubjob[0])
		else:
			resultSolution = move(solution, randSubjob[0])
		if resultSolution != None:
			foundMutation = True
			solution = resultSolution

	return solution

def eval_all(offspring):
	evaluation = []

	for solution in offspring:
		evaluation.append(eval_single2(solution))

	return evaluation

def eval_single(solution):
	timeMax = 0
	for machineJobs in solution:
		currentTime = 0
		memNullJobLength = 0						# -> do not count "-1" at the end
		for subjob in machineJobs:
			if (subjob[0] == -1):
				memNullJobLength += subjob[1]
			else:
				currentTime += memNullJobLength + subjob[1]
				memNullJobLength = 0
		if currentTime > timeMax:
			timeMax = currentTime

	return timeMax

def eval_single2(solution):
	count = 0.0
	for machineJobs in solution:
		time = 0.0
		for subjob in machineJobs:
			if subjob[0] != -1:
				count += time/1000
			time += subjob[1]
	return count

# idea: select k at random -> select 2 fittest of the selection
def select_population(evaluation, offspring):
	population = []
	for i in range(POPULATION_SIZE):
		idxMin = evaluation.index(min(evaluation))
		population.append(offspring[idxMin])
		evaluation[idxMin] = 999999999999		# some big number -> this entry should not be in population again
	return population

########## HELPER METHODS ###########

# try to move subjob to the left (as far as possible)
def move(solution, subjobNr):
	(left, right) = get_moving_range(solution, subjobNr)
	if (left == 0):
		return None

	subjobBegin = get_begin(solution, subjobNr)

	for machineJobs in solution:
		for i in range(len(machineJobs)):
			if (machineJobs[i][0] == subjobNr):
				if (i == 0 or machineJobs[i-1] != -1):		# double check, that pre job is empty (-1)
					return None
				if (machineJobs[i-1][1] < left):
					machineJobs[i-1][1] -= left
				elif (machineJobs[i-1][1] == left):
					del machineJobs[i-1]
	return solution




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

	# print "within machine", range1
	# print "within job", range2
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

# compareToPrev: True -> yes, False -> compare to following job
def changeSubjobs(solution, machineJobs, subjobNr):
	for i in range(len(machineJobs)):
		if (machineJobs[i][0] == subjobNr):
			currentJob = machineJobs[i]
			compareJob = ()
			if i > 0:
				compareJob = machineJobs[i-1] 

			if compareJob == ():
				return None

			# check if jobs have direct dependecies
			if (haveSubjobsSameJob(currentJob, compareJob)):
				return None

			# check dependency within job...
			newMachineJobs = list(machineJobs)
			newMachineJobs[i-1] = currentJob
			newMachineJobs[i] = compareJob

			solutionCopy = list(solution)
			idx = solution.index(machineJobs)
			solutionCopy[idx] = newMachineJobs
			if isValidSolution(solutionCopy):
				return solutionCopy

			break
	return None

def haveSubjobsSameJob(subjob1, subjob2):
	foundJobsCount = 0
	for machineJobNr in JobDict.keys():
		count = 0				# count: 1 if subjob1 or subjob2 are in job. 2 if subjob1 and subjob2 are in job
		for subjob in JobDict[machineJobNr]:
			if (subjob == subjob1):
				count += 1
				foundJobsCount += 1
			if (subjob == subjob2):
				count += 1
				foundJobsCount += 1
		if (count == 2):
			return True
		if (foundJobsCount == 2):
			return False
	return False

def isValidSolution(solution):
	for jobNr in JobDict.keys():
		endLastJob = 0
		for subjob in JobDict[jobNr]:
			beginCurrentJob = get_begin(solution, subjob)
			if (beginCurrentJob < endLastJob):
				return False
			endLastJob = beginCurrentJob + get_subjob(solution, subjob)[1]
	return True

# transform format
def out(solution):
	output = []
	for machineJobs in solution:
		time = 0
		currentMachineJobs = []
		for subjob in machineJobs:
			if (subjob[0] != -1):
				currentMachineJobs.append((time, subjob[1], getJobFromSubjob(subjob[0])))
			time += subjob[1]
		output.append(currentMachineJobs)
	return output

def getJobFromSubjob(subjobNr):
	for key in JobDict.keys():
		for subjob in JobDict[key]:
			if (subjob == subjobNr):
				return key
	return -1