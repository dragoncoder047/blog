.PHONY: build clean filenames

build: clean
	./build.py


clean:
	rm -rf docs/

filenames:
	python3 normalize_filenames.py
