CC = gcc
CFLAGS = -Wall -Wextra -std=c11
LDFLAGS =
TARGET = data-manipulator.exe
SRC = data-manipulator.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC) $(LDFLAGS)

clean:
	del $(TARGET)

run: $(TARGET)
	$(TARGET) age 1990-05-15
	$(TARGET) weight_lost 200 190
	$(TARGET) percentage_lost 10 200

.PHONY: all clean run
