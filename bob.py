from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import time

def AES_decipher():
    # pad and unpad functions
    def unpad_data(data):
        pad_size = data[-1]
        if pad_size < 1 or pad_size > AES.block_size:
            raise ValueError("Invalid padding")
        return data[:-pad_size]

    # Bob reads the ciphertext
    with open("AESciph.txt", "rb") as file:
        iv = file.read(AES.block_size)
        ciphertext = file.read()
    
    #init. cipher and decrypt and unpad
    #print("Message to decrypt: ", ciphertext)
    file_in = open("AESkey.txt", "rb")
    key = file_in.read()
    file_in.close()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(ciphertext)
    original_message = unpad_data(decrypted_message)
    print("Decrypted message:", original_message.decode())

def RSA_decipher():
    #bob decrypts the ciphertext
    file_in = open("private.txt", "rb")
    private_key = RSA.import_key(file_in.read())
    file_in.close()

    file_in = open("RSAciph.txt", "rb")
    ciphertext = file_in.read()
    file_in.close()

    cipher_rsa = PKCS1_OAEP.new(private_key)
    message = cipher_rsa.decrypt(ciphertext)
    print("Decrypted: ", message.decode())
    pass

def menu():
    print("Hello, Bob! Looks like Alice sent you a message. What would you like to do?")
    print("1. Decrypt AES")
    print("2. Decrypt RSA")
    print("3. Timing")
    choice = input("Enter your choice: ")

    if choice == "1":
        print("You have chosen AES decipher.")
        AES_decipher()
        pass
    elif choice == "2":
        print("You have chosen RSA decipher.")
        RSA_decipher()
        pass

    elif choice == "3":
        print("You have chosen Timing.")

        print("How many times would you like to run the timing test?")
        num = int(input())

        print("AES or RSA?")
        algo = input("Enter your choice: ")

        if algo == "AES":
            sum = 0
            for i in range(num):
                start = time.time()
                AES_decipher()
                end = time.time()
                sum += end - start
            print("Average time: ", sum/num)
            pass

        elif algo == "RSA":
            sum = 0
            for i in range(num):
                start = time.time()
                RSA_decipher()
                end = time.time()
                sum += end - start
            print("Average time: ", sum/num)
        pass

    else:
        print("Goodbye!")
        exit()

menu()
