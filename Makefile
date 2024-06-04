.PHONY: build clean

build: clean
	./build.py
	cp banner_image.js docs/banner_image.js

clean:
	rm -rf docs/
