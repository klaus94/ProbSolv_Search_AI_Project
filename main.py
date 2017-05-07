import sys 						# evaluate program parameter
import imp 						# evaluate installed packages
import numpy as np 				# math
import algorithms				# our own module
try:							# import matplotlib, if it is installed
	imp.find_module('matplotlib')
	isMatplotlibInstalled = True
except ImportError:
	isMatplotlibInstalled = False
if isMatplotlibInstalled:
	import matplotlib.pyplot as plt 	# library for plotting


# parses single-test-data into a tuple (machine-count, job-list)
def parse_single(single_data):
	machine_count = 0
	jobs = []

	for line in single_data.split("\n"):
		line = line.strip(" ")							# remove spaces at the beginning
		splitted_line = line.split(" ")
		
		splitted_line = [x for x in splitted_line if x != ""]		# clean line (remove empty elements)

		if machine_count == 0:							# try to read machine-count, if not set yet
			try:
				job_count = int(splitted_line[0])		# dont know if needed
				machine_count = int(splitted_line[1])
			except Exception as e:
				pass
		else:											# read in job-data
			job = []
			for i in range(len(splitted_line)//2):
				try:
					machine_nr = int(splitted_line[i*2])
					time = int(splitted_line[i*2+1])
					job.append((machine_nr, time))
				except Exception as e:
					pass
			if len(job) > 0:							# remove last empty element []
				jobs.append(job)
	return (machine_count, jobs)


# returns a list of training_data
# a trainingdata contains the amount of machines and a list of jobs (mach_count, jobs)
# a job contains tuples of sub_jobs (machine, time)
def parse():
	data_file = open("data.txt", "r")
	data_string = data_file.read()
	training_data = {}
	data_split = data_string.split(" +++++++++++++++++++++++++++++")
	next_test_data_name = ""			# indicates name of test-data-set
	for splitted in data_split:
		# print splitted

		if next_test_data_name != "":
			single_test_data = parse_single(splitted)							# get next single-data-set
			training_data[next_test_data_name] = parse_single(splitted)
			next_test_data_name = ""

		if "\n instance" in splitted:
			next_test_data_name = splitted.split(" ")[3].strip("\n")			# extract next data-set-name
	
	return training_data

# plot solution in nice bar-chart
# solution is a 2d-array: 
# [ [(0, 2, 0), (2, 2, 1)],			-> jobs in machine 1
#   [(0, 2, 0), (2, 2, 1)] ]		-> jobs in machine 2
# (0, 2, 0).. (begin, length, job-nr)
def plot_solution(solution):
	machine_count = len(solution)
	y_pos = np.arange(machine_count)
	machine_names = ["M" + str(x) for x in range(machine_count)]

	fig = plt.figure(figsize=(10,8))
	ax = fig.add_subplot(111)

	# colors ='rgbwmc'

	colors = ['#0048BA','#B0BF1A','#7CB9E8', '#84DE02', '#E32636', '#C46210', '#EFDECD', '#E52B50', 
	'#F19CBB', '#FFBF00', '#00C4B0', '#9966CC', '#A4C639', '#CD9575', '#665D1E', '#915C83', '#841B2D',
	'#00FFFF', '#D0FF14', '#E9D66B', '#B2BEB5', '#FF9966', '#A52A2A', '#FF2052']

	for machine in range(machine_count):
		for task in solution[machine]:
			color = colors[task[2]-1]		
			ax.barh([machine], [task[1]], color=color, align='center', left=[task[0]])

	# mabe later: label tasks
	# go through all of the bar segments and annotate
	# for j in xrange(len(patch_handles)):
	# 	for i, patch in enumerate(patch_handles[j].get_children()):
	# 		bl = patch.get_xy()
	# 		x = 0.5*patch.get_width() + bl[0]
	# 		y = 0.5*patch.get_height() + bl[1]
	# 		ax.text(x,y, "%d%%" % (percentages[i,j]), ha='center')

	ax.set_yticks(y_pos)
	ax.set_yticklabels(machine_names)
	ax.set_xlabel('time')

	plt.show()


def main():
	# parse test data
	test_data_name = "abz5"
	if len(sys.argv) > 1:
		test_data_name = sys.argv[1]
	task_dict = parse()
	(machine_count, jobs) = task_dict[test_data_name]

	# call our algorithm
	print jobs
	solution = algorithms.baseLineAlg(machine_count, jobs)

	# todo: output our solution into a file

	# plot the solution
	if isMatplotlibInstalled:
		plot_solution(solution)




# start main, if this is the main-program
if __name__ == '__main__':
	main()