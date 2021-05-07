from subprocess import run, PIPE
import glob


def check():
	all_files = [f for f in glob.glob("**/**/*.py", recursive=True)]
	errors = []
	for file in all_files:
		arguments = "--first " + file + " --ignore=W191"
		result = run(
			["pycodestyle", "--first", file, "--ignore=W191"],
			stdout=PIPE, stderr=PIPE, universal_newlines=True)
		errors.append(result.stdout)

	return_code = 0
	for error in errors:
		if error != "":
			print(error)
			return_code = 1
	exit(return_code)


if __name__ == '__main__':
	check()
