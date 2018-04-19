import parser_linux
from sys import platform

if __name__ == '__main__':
	if platform == "linux" or platform == "linux2":
		videos = parser_linux.get_movies_list()
		csd    = parser_linux.considerMovies(videos)
		parser_linux.create_table(videos,csd)
		print("Done!")
	elif platform == "darwin":
	    print("not implemented yet for this OS")
	elif platform == "win32":
	    print("not implemented yet for this OS~~~~~")