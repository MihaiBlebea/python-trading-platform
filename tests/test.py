import os
import unittest

class UnitTestLauncher:

	def runTests(self):
		#logging.INFO("Running unit tests...")
		lsPaths = []

		#Find all relevant subdirectories that contain unit tests
		#Exclude "unittest" directory, but include subdirectories, with code `path != "unittest"`
		for path, subdirs, files in os.walk("tests"):
			if "pycache" not in path and path != "tests":
				lsPaths.append(path)

		#loop through subdirectories and run individually
		for path in lsPaths:
			loader = unittest.TestLoader()
			suite = unittest.TestSuite()
			suite = loader.discover(path)
			unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
	utl = UnitTestLauncher()
	utl.runTests()