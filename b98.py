import time
import math
import sys, os

def chaotic_map(b,x0):
	return b*x0*(1-x0)

file_extension = "b98"
file_header = b"B98 File Container v1.0 (https://doi.org/10.1016/S0375-9601(98)00086-3)"

def crypt(input_file_name, e, xmin, x0, mu_param, byte_len=8):
	n = 250
	s = 256
	# crypted_text = ""

	input = ""
	with open(input_file_name,"rb") as f:
		input = f.read()
		f.close()

	crypted_text_byte_arr = b""
	for character in input:
		gap = (xmin + (character -1)*e, xmin + character*e)

		for i in range(1,65535):
			x0 = chaotic_map(mu_param, x0)
			if(x0 >= gap[0] and x0 < gap[1] and i >= n):
				crypted_text_byte_arr +=(i.to_bytes(byte_len,'little'))
				break
	
	with open(f"{input_file_name}.{file_extension}","wb") as f:
		f.write(file_header)
		f.write(crypted_text_byte_arr)
		f.close()
	# return crypted_text


def decrypt(input_file, e, xmin, b, x0, byte_len=8):
	output_file_name = input_file[:-(len(file_extension)+1)]
	input = ""
	decrypted_text_byte_arr = b""
	file = open(input_file, 'rb')
	file.seek(len(file_header))

	header_count = 0
	while 1:
		byte = file.read(byte_len)
		if(byte == b''):
			break

		input = int.from_bytes(byte, "little")
		for i in range(0,(input)):
			x0 = chaotic_map(b, x0)

		val = (math.ceil((x0-xmin)/e))
		decrypted_text_byte_arr += (val.to_bytes(1,'little'))
	
	with open(output_file_name,"wb") as f:
		f.write(decrypted_text_byte_arr)


def gen_secret_params(secret_file_path):
	xmin = 0.2
	x0 = 0.23224323
	e = 0.00234375000
	mu_param = 3.8
	return xmin, x0, e, mu_param

def gen_secret_file(secret_file_name):
	xmin, x0, e, mu_param = gen_secret_params("default")
	try:
		with open(secret_file_name, "w") as f:
			f.write(f"{xmin}|{x0}|{e}|{mu_param}")
			f.close()
		print("Successfully created secret file.\n", os.path.abspath(secret_file_name))
	except Exception as e :
		print("Error when generating secret file.",e)
	pass

def read_secret_file():
	pass


if __name__ == "__main__":

	if(len(sys.argv) < 3):
		print("""Argument error. 
			1) Encryption : b98.py encrpyt secret_key_file.txt plain_file.pdf
			2) Decryption : b98.py decrypt secret_key_file.txt encrypted_file.b98
			3) Generate secret key file : b98.py secret my_secret_file.txt
			""")
		exit(0)

	"""
	arg 0 -> b98.py
	arg 1 -> cmd (encrpyt/decrypt/secret)
	arg 2 -> secret file path
	arg 3 -> plain file path / encrypted file path

	"""
	byte_len = 2

	if("enc" in sys.argv[1]):
		xmin, x0, e, mu_param = gen_secret_params(sys.argv[2])

		input_file_name = sys.argv[3]

		start_t = time.time()
		crypt(input_file_name, e, xmin, x0, mu_param, byte_len=byte_len)
		print("Enc time msec:", (time.time()-start_t)*1000)
		
	if("dec" in sys.argv[1]):
		xmin, x0, e, mu_param = gen_secret_params(sys.argv[2])
		input_file_name = sys.argv[3]

		start_t = time.time()
		decrypt(f"{input_file_name}", e, xmin, mu_param,x0, byte_len=byte_len)
		print("Dec time msec:", (time.time()-start_t)*1000)

	if(sys.argv[1] == "secret"):
		print(f"Generating secret file as {sys.argv[2]}")
		gen_secret_file(sys.argv[2])
		pass





