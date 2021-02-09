#!/bin/sh
nc -l -u 12345 | redsea -x -p | nc -u 127.0.0.1 52005
#socat udp-listen:12345 - | redsea -x -p | socat STDIN udp:127.0.0.1:52005
#while :
#do
#	timeout 5s socat udp-listen:12345 - | redsea -x -p | socat STDIN udp:127.0.0.1:52005
#done
