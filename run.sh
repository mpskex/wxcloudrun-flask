#!/bin/sh
# setup vpn
python3 gen_profile.py && wg-quick up wg0
# run
python3 run.py 0.0.0.0 80