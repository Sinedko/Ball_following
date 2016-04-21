CC=gcc
CFLAGS=-Ofast -Wall-Werror

All :
	$(CC) -o backprop backprop-1H.c
	python -m py_compile Classes.py
	$(CC) -o Train/backprop Train/backprop-1H.c
	python -m py_compile Train/Classes.py

clean:
	rm backprop
	rm Train/backprop
	rm Classes.pyc
	rm Train/Classes.pyc