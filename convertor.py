import numpy
import RC5

def original(pix,width,height):
    # Define the window size
    windowsize_r = height - (height % 2) # height
    windowsize_c = width - (width % 6) # width
    # Crop out the window
    for r in range(0, windowsize_r, windowsize_r): #pix.shape[0]
        for c in range(0,windowsize_c, windowsize_c):
            window = pix[r:r+windowsize_r,c:c+windowsize_c]
    return (window , windowsize_r,windowsize_c)

def encrypt(window,windowsize_r,windowsize_c,pwd, rounds, mode = 'ECB'):
    first_word = ''
    socund_word = ''
    count = 0
    enc = []
    # loop on each pixel in the image and encrypt each 6 pixel in 3-3 block
    for r in range(0, windowsize_r):
        for c in range(0,windowsize_c):
            for i in range(0,3):
                x = str(window[r][c][i])
                if len(x) < 3 :
                    if len(x) < 2:  
                        x=x[:0] + "0" + x[0:]
                    x=x[:0] + "0" + x[0:]
                if  0 <= count <=  2:
                    first_word += x
                    count += 1
                elif 3 <= count <= 5 :
                    socund_word += x
                    count += 1
                    if count == 6:
                        test_origin_char = '{}-{}'.format(first_word, socund_word)
                        # calling RC5 class
                        cryptor = RC5.RC5(pwd)
                        cryptor.mode = mode
                        cryptor.rounds = rounds
                        enc_str = cryptor.encrypt_str(test_origin_char)
                        counter = 0
                        enc.append(enc_str)
                        first_word = ''
                        socund_word = ''
                        count = 0
    return enc

def decrypt(enc,windowsize_r,windowsize_c,pwd,rounds,mode = 'ECB'):
    # calling RC5 class
    cryptor = RC5.RC5(pwd)
    cryptor.mode = mode
    cryptor.rounds = rounds
# loop on each value in the encrypt array that represent 6 pixel and display it into its place
    dec = []
    for x in enc:
        dec_str = cryptor.decrypt_str(x)
        dec.append(dec_str)

    split_txt = []
    for a in dec :
        u = a.split('-')
        for q in u:
            split_txt.append(q) 
    print('spilt text len :', len(split_txt))
    res = []
    for r in range(0,windowsize_r): 
        o = []
        for c in range(0,windowsize_c):
            o.append(split_txt[c + (r * windowsize_c)])
        c_res =[]
        for c in range(0,windowsize_c):
            w = [o[c][i:i+3] for i in range(0, len(o[c]), 3)]
            d = numpy.array([numpy.uint8(int(a)) for a in w])
            c_res.append(d)
        c_res = numpy.array(c_res)
        res.append(c_res)
    res = numpy.array(res)
    return res