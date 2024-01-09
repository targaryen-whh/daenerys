
import time

# Constants
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
infinity = (None, None)

# Functions
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    result_modinv = x1 + m0 if x1 < 0 else x1
    return result_modinv

def point_add(p1, p2):
    if p1 == infinity:
        return p2
    if p2 == infinity:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if p1 != p2:
        m = ((y2 - y1) * modinv(x2 - x1, p)) % p
    else:
        m = ((3 * x1**2 + a) * modinv(2 * y1, p)) % p

    x3_result = (m**2 - x1 - x2) % p
    y3_result = (m * (x1 - x3_result) - y1) % p
    return x3_result, y3_result

def point_double(p):
    return point_add(p, p)

def scalar_multiply(k, point):
    result_scalar_mult = infinity
    counter = 0
    while k > 0:
        if k % 2 == 1:
            result_scalar_mult = point_add(result_scalar_mult, point)
            counter += 1
        k //= 2
        point = point_double(point)
    return result_scalar_mult

def decompress_public_key(compressed_key):
    prefix = compressed_key[0]
    x_bytes = compressed_key[1:]
    x = int.from_bytes(x_bytes, 'big')
    y_squared = (x**3 + a*x + b) % p
    y = pow(y_squared, (p + 1) // 4, p)

    if (y % 2 == 0 and prefix == 0x02) or (y % 2 == 1 and prefix == 0x03):
        return x, y
    else:
        return x, p - y

# Get user input for compressed public key
user_compressed_key_hex = input("Enter the compressed public key in hexadecimal format: ")
user_compressed_key = bytes.fromhex(user_compressed_key_hex)

# Example usage
compressed_key = user_compressed_key
public_key_point = decompress_public_key(compressed_key)

# Display the decompressed public key
print("\nDecompressed Public Key:")
print("X-coordinate:", public_key_point[0])
print("Y-coordinate:", public_key_point[1])

# Now, you can derive the private key within a specific range
start_key_hex = input("Enter the start key in hexadecimal format: ")
end_key_hex = input("Enter the end key in hexadecimal format: ")

start_key = int(start_key_hex, 16)
end_key = int(end_key_hex, 16)

calculated_private_key = None
counter_scalar_mult = 0

# Start measuring time
start_time = time.time()

for k in range(start_key, end_key + 1):
    candidate_public_key = scalar_multiply(k, (Gx, Gy))
    counter_scalar_mult += 1
    print("Calculation . . . {}".format(counter_scalar_mult), end='\r')

    # Compare x-coordinates of candidate and target public keys
    if candidate_public_key[0] == public_key_point[0]:
        calculated_private_key = format(k, 'x')  # Convert to hexadecimal
        break

# Stop measuring time
end_time = time.time()

# Display the calculated private key and total running time
print("\nCalculated Private Key:", calculated_private_key)
print("Total Scalar Multiplication Steps:", counter_scalar_mult)
print("Total Running Time: {:.6f} seconds".format(end_time - start_time))
