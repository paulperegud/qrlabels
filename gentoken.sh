#!/bin/bash
hexdump -vn12 -e'4/4 "%08X" 1 "\n"' /dev/urandom
