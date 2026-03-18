import heapq

import json
import struct


def code (input_path: str, output_path: str):
                
    with open ('input.txt', 'r') as f: # считали входную строку
        msg = f.read()
        

    encoded_bits, table = encode(msg) # применили код хаффмана. теперь наша задача это дело закодировать.
    print(encoded_bits, len(encoded_bits), len(table),table)

    with open ('output_path.bin', 'wb') as f:
        
        f.write(struct.pack('I', len(encoded_bits))) # количество бит
        f.write(struct.pack('I', len(table)))  # количество Бит

        nbytes = (len(encoded_bits) - 1) // 8 + 1
        for x in range ((((len(encoded_bits)-1) //8) + 1)):
            a = encoded_bits[x*8: (x+1)*8]
            f.write(struct.pack('B', int(a.ljust(8, '0'), 2))) # добавляем нужные нолики


        for x in table: # записали словарь
            f.write(bytes(x,  "ascii")) # символ
            f.write(struct.pack('I', len(table[x]))) #длина  символа
            
            for y in range ((((len(table[x])-1) //8) + 1)): 
                a = table[x][y*8: (y+1)*8]
                f.write(struct.pack('B', int(a.ljust(8, '0'), 2)))



    with open('output_path.bin', 'rb') as f:
        encoded_bits_len = struct.unpack('I', f.read(4))[0] # узнали количество бит  под encoded_bit
        table_len = struct.unpack('I', f.read(4))[0] # узнали количество ключей в словаре
        
        a = ''
        
        for x in range (0, (encoded_bits_len - 1) // 8 + 1):
            if x!= (encoded_bits_len-1)//8 :
                a += bin(struct.unpack('B', f.read(1))[0])[2:].zfill(8)
            else:
                # В последнем байте берем только нужные биты 
                if encoded_bits_len % 8 != 0:
                    rem = encoded_bits_len % 8
                else:
                    rem = 8
                a += bin(struct.unpack('B', f.read(1))[0])[2:].zfill(8)[:rem]

        # теперь расшифровываем словарь  
        dictt = {}
        for x in range (0, table_len):
            q = f.read(1).decode('ascii')
            bit_len = struct.unpack('I', f.read(4))[0]
            len_byte = (bit_len-1 )//8 + 1

            strr = ""
            for y in range (0, len_byte):
                if y != len_byte - 1:
                    strr += bin(struct.unpack('B', f.read(1))[0])[2:].zfill(8)

                else:
                    if bit_len % 8 != 0:
                        rem = bit_len % 8
                    else:
                        rem = 8
                    strr += bin(struct.unpack('B', f.read(1))[0])[2:].zfill(8)[:rem]
            
            dictt[q] = strr

    
    return [encoded_bits_len,table_len, a, encoded_bits, dictt]


def encode(msg: str) -> tuple[str, dict[str, str]]:

    class Node: # класс хронящий узел
        def __init__(self, left, right):
            self.left = left
            self.right = right
        def walk(self, code, acc): # рекурсивный обход дерева
            self.left.walk(code, acc + "0")
            self.right.walk(code, acc + "1")

        def __repr__(self):# f - строка для удобного дебага
            return f"Node(left = {self.left}, right = {self.right})"

    class Leaf: # класс хранящий лист, а лист = буква 
        def __init__(self, char):
            self.char = char
        def walk (self, code, acc):
            code[self.char] = acc or "0"

        def __repr__(self): # f - строка для удобного дебага
            return f"Leaf(char='{self.char}')"
    
    alph = {}
    for x in msg: # создаем словарь с упорядоченными по убыванию частотами. 
        alph[x] = alph.get(x, 0) + 1
    alph = dict(sorted(alph.items(), key = lambda item:item[1], reverse=True))

    h = []
    for ch, freq in alph.items(): # каждую букву помещаем в кучу с тремя параметрами freq, id, Leaf 
        h.append((freq, len(h), Leaf(ch))) # len(h) - id помогающий не упереться в ошибку когда происходит heappush()
    heapq.heapify(h)

    count = len(h)
    
    while len(h) > 1: # реализуем сам код хаффмана. убрали два минимума, добавили один узел с суммой их частот 
        freq1, count1, left = heapq.heappop(h)
        freq2, count2, right = heapq.heappop(h)
        heapq.heappush(h, (freq1 + freq2, count, Node(left, right))) # добавляем пару частота + узел 
        count += 1
        
    root = h[0][2] #корень
    code = {}
    root.walk(code, "")
    encoded_msg = ''.join(code[char] for char in msg)
    return encoded_msg, code 

def decode(encoded: str, table: dict[str, str]) -> str:
    stroke = ""
    msg = ""

    print(table, encoded)
    while len(encoded) > 0:
        stroke += encoded[0]
        if stroke in table.values(): # ну тут вроде все понятно. проверели. есть ли в словаре. если есть то вставили. 
            for x in table:
                if table[x] == stroke:
                    msg += x
                    stroke = ""
                    break 
        encoded = encoded[1:]
    return msg
print (code("input.txt", "output.txt"))
