import sys


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
					# print splitted_line[i*2]
					# print splitted_line[i*2+1]
					# print "\n\n"
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



def main():
	test_data_name = sys.argv[1]
	task_dict = parse()

	if test_data_name == "":
		test_data_name = "abz5"
		
	print task_dict[test_data_name]



# start main, if this is the main-program
if __name__ == '__main__':
	main()