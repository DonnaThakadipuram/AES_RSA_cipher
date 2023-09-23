from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import PKCS1_OAEP
import time

timing = False

def AES_cipher(key_size, message):
    # pad and unpad functions
    def pad_data(data):
        block_size = AES.block_size
        pad_size = block_size - (len(data) % block_size)
        padding = bytes([pad_size]) * pad_size
        return data + padding

    def unpad_data(data):
        pad_size = data[-1]
        if pad_size < 1 or pad_size > AES.block_size:
            raise ValueError("Invalid padding")
        return data[:-pad_size]

    # generate key and make cipher
    key = get_random_bytes(key_size // 8)
    #key gets printed into a text file so bob can use it
    file_out = open("AESkey.txt", "wb")
    file_out.write(key)
    file_out.close()

    cipher = AES.new(key, AES.MODE_CBC)

    # input message, pad message, and encrypt message
    #message = input("Enter the message: ")
    padded_message = pad_data(message.encode())
    ciphertext = cipher.encrypt(padded_message)

    #Alice writes the ciphertext to a file along with the IV
    with open("AESciph.txt", "wb") as file:
        file.write(cipher.iv)
        file.write(ciphertext)

    if(timing == False):
        pass
        #print("Encrypted and saved to file")
    #print("Encrypted and saved to file")
    # print("Encrypted: ", ciphertext)

#RSA function
def RSA_cipher(key_size, message):
    #generate key pair for Bob
    key = RSA.generate((key_size))
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    #save key pair to text files
    file_out = open("private.txt", "wb")
    file_out.write(private_key)
    file_out.close()

    file_out = open("public.txt", "wb")
    file_out.write(public_key)
    file_out.close()

    #alice uses bob's public key to encrypt a message
    file_in = open("public.txt", "rb")
    public_key = RSA.import_key(file_in.read())
    file_in.close()

    #message = input("Enter the message to encrypt: ")
    message = message.encode()

    cipher_rsa = PKCS1_OAEP.new(public_key)
    ciphertext = cipher_rsa.encrypt(message)
    # print("Encrypted: ", ciphertext)

    #alice sends the ciphertext to bob
    file_out = open("RSAciph.txt", "wb")
    file_out.write(ciphertext)
    file_out.close()
    if(timing == False):
        pass
        #print("Encrypted and saved to file")
    #print("Encrypted and saved to file")

def menu():
    print("Hello, Alice! What would you like to do?")
    print("1. Encrypt a message with AES")
    print("2. Encrypt a message with RSA")
    print("3. Timing")
    choice = input("Enter your choice: ")
    if choice == "1":
        print("You have chosen AES cipher. Enter key size (128, 192, or 256): ")
        key_size = int(input())
        print("Enter the message to encrypt: ")
        message = input()
        AES_cipher(key_size, message)
        pass
    elif choice == "2":
        print("You have chosen RSA cipher. Enter key size(1024, 2048, or 4096): ")
        key_size = int(input())
        print("Enter the message to encrypt: ")
        message = input()
        RSA_cipher(key_size, message)
        pass

    elif choice == "3":
        sum = 0

        print("You have chosen Timing.")
        timing = True
        print("Enter the message to encrypt: ")
        message = input()
        print("How many times would you like to run the timing test?")
        num = int(input())
        print("AES or RSA?")
        algo = input()

        if algo == "AES":
            print("What key size? (128, 192, 256)")
            key_size = int(input())
            for i in range(num):
                start = time.time()
                AES_cipher(key_size, message)
                end = time.time()
                sum += end - start
                pass
            avg = sum / num
            print("Average encryption time: ", avg)

        elif algo == "RSA":
            print("What key size? (1024, 2048, 4096)")
            key_size = int(input())
            for i in range(num):
                start = time.time()
                RSA_cipher(key_size, message)
                end = time.time()
                sum += end - start
                pass
            avg = sum / num
            print("Average encryption time: ", avg)

        # #file_out.close()
        print("TIMING TEST COMPLETE")
    else:
        print("Goodbye!")
        exit()

menu()
