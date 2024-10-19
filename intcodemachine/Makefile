define .RECIPEPREFIX
 
endef
CC=gcc-14
CFLAGS= -std=c23 -shared -fPIC -I /usr/include/python3.13 -Wall -Wno-unused-result

all: ./icm/intcodemachine.so ./../fft/fft.so deploy

./icm/intcodemachine.so: ./src/intcodemachine.c
    $(CC) $(CFLAGS) ./src/intcodemachine.c -o ./icm/intcodemachine.so

./../fft/fft.so: ./../fft/fft.c
    $(CC) $(CFLAGS) ./../fft/fft.c -o ./../fft/fft.so

test:
    python3 test.py

deploy:
    cp ./src/__init__.py ./icm/
    cp ./icm/intcodemachine.so ./../2
    cp ./icm/intcodemachine.so ./../5
    cp ./icm/intcodemachine.so ./../7
    cp ./icm/intcodemachine.so ./../9
    cp ./icm/intcodemachine.so ./../11
    cp ./icm/intcodemachine.so ./../13
    cp ./icm/intcodemachine.so ./../15
    cp ./../fft/fft.so ./../16
    cp -r ./icm ./../17/

install:
    pip install --editable .

clean:
    -rm -rf *.so
