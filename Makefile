CXX      = g++
CXXFLAGS = -fPIC -Wall -O2 -I/usr/include/crypto++ -I/usr/include/cryptopp
LDFLAGS  = -shared -lcrypto++
TARGET   = libempcrypt.so

all: $(TARGET)

$(TARGET): core.cpp
	$(CXX) $(CXXFLAGS) -o $@ $< $(LDFLAGS)

clean:
	rm -f $(TARGET)

.PHONY: all clean
