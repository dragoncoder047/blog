.PHONY: build clean filenames

build: clean
	./build.py
	cp banner_image.js docs/banner_image.js

clean:
	rm -rf docs/

filenames:
	python3 normalize_filenames.py
