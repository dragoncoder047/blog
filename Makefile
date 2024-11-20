.PHONY: build clean filenames

build: clean
	./build.py
	cp banner_image.js docs/banner_image.js
	cp kdemo.html docs/2024/boy-have-i-been/kdemo.html
# that was a KLUDGE!! why

clean:
	rm -rf docs/

filenames:
	python3 normalize_filenames.py
