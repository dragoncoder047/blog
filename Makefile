.PHONY: build clean

build: clean
	./build.py

clean:
	rm -f *.html
	rm -rf category
	rm -rf draft
	rm -rf images
	rm -rf post
