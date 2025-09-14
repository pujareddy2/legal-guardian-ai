import tenseal as ts

def tenseal_demo():
    # Create a TenSEAL context with default parameters
    context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])
    context.generate_galois_keys()
    context.global_scale = 2**40

    # Encrypt two numbers
    enc_a = ts.ckks_vector(context, [10.0])
    enc_b = ts.ckks_vector(context, [20.0])

    # Perform addition on encrypted vectors
    enc_result = enc_a + enc_b

    # Decrypt and print result
    result = enc_result.decrypt()
    print("Decrypted Result (10 + 20):", result[0])

if __name__ == "__main__":
    tenseal_demo()
