from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb4dlJaiZukB_7Xya8XgE3dzH_8Ii5H8D9F1BPjYwL5S5fjMiSwXySFtW3NOsTZcCYo69lT2Se-qqn3OOgwUaSFGR74aUsKQur3xR_pbF6yMHMxypo785Y4j_cbd9w8wil6cjKVpKvYD5twvtp0T1t0gcG-bMoKp0N2PKac_igX4fmdMAdX2cLcoT2JX_d4id6oNxk'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()