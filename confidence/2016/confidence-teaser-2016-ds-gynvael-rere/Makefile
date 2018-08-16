.PHONY = test distfiles build

build:
	# Note: There is a lot of randomness when building the 
	# crackme - expect output file to have a different size
	# each time.
	python src/build_st1.py > src/st1.py
	python src/build_st2.py > src/st2.py
	mkdir -p crackme
	# cp src/st2.py crackme/rere.py
	# Copy this file only if you really need it.

distfiles:
	mkdir -p distfiles	

test:
	# I have an idea how to test this, but it will require
	# writting a small terminal emulator. Maybe later.
	true
