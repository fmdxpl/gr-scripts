#!/bin/sh
( nc -l -u 12345 | redsea -x -p | nc -u 127.0.0.1 52005 )
