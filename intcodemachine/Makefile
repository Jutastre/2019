define .RECIPEPREFIX
 
endef
CC=gcc-14
CFLAGS= -std=c23 -shared -fPIC -I /usr/include/python3.13 -Wall -Wno-unused-result

all: intcodemachine.so deploy

intcodemachine.so: intcodemachine.c
    $(CC) $(CFLAGS) intcodemachine.c -o intcodemachine.so

test:
    python3 test.py

deploy:
    cp intcodemachine.so ./../2
    cp intcodemachine.so ./../5
    cp intcodemachine.so ./../7
    cp intcodemachine.so ./../9
    cp intcodemachine.so ./../11

install:
    pip install --editable .

clean:
    -rm -rf *.so
