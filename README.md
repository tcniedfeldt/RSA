# RSA

Basic RSA implementation that produces 512-bit `p` and `q` prime numbers with `PHI(n) = (p-1)*(q-1)` and where `gcd(e, PHI(n)) == 1`.

# Usage

- Make sure that python3 is installed.
- To run: `python3 rsa.py`
- If you want to keep `p` and `q` the same, comment the blocks that generate `p` and `q` and uncomment the lines that hard-code their values.
- To encrypt a message, hard-code the message and uncomment the encryption block
    - The same method applies for the decryption block.
