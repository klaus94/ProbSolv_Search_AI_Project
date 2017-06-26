
# IN: (machine_count, [job1, job2, job3, ...])
#	->	job... [(machineNr, time), (machineNr, time), ...]
#
# OUT: [jobs_on_machine1, jobs_on_machine2, jobs_on_machine3, ...]
#	->	job_on_machine... [(begin, length, jobNr), (begin, length, jobNr), (begin, length, jobNr)]

# hyper-parameters
POPULATION_SIZE = 10
EPOCHS = 1000

def solve(machine_count, jobs):
	population = init(machine_count, jobs, POPULATION_SIZE)			# list of solutions
	evaluation = eval_all(population)

	time = 0
	while time < EPOCHS:
		time += 1
		(mum, dad) = selectParents(evaluation, population)
		offspring = recombine(mum, dad)
		offspring += mutate(mum, dad)
		evaluation = eval_all(offspring)
		population = select_population(evaluation, offspring)

	return population



# helper methods

def init(machine_count, jobs, population_size):
	t = 0
	currentJobNr = 0
	machine_jobs = [[] for x in range(machine_count)]

	for job in jobs:
		for task in job:
			machine_jobs[task[0]].append((t, task[1], currentJobNr))
			t += task[1]

		currentJobNr += 1



	return machine_jobs

def selectParents(evaluation, population):
	pass

def recombine(solution1, solution2):
	pass

def mutate(solution1, solution2):
	pass

def eval_all(evaluation, offspring):
	pass

def select_population(offspring):
	pass




