# # coding = utf-8
# def clearBlankLine():
#     file1 = open('xjt4.txt', 'r', encoding='gbk', errors = "ignore") # 要去掉空行的文件 
#     file2 = open('xjt.txt', 'a', encoding='gbk', errors = "ignore") # 生成没有空行的文件
#     file3 = open('xjt2.txt', 'r', encoding='gbk', errors = "ignore") # 生成没有空行的文件
#     try:
#         for line in file1.readlines():
#             # line = line.strip('"')
#             # if line == '\n':
#             # line = line.rstrip(",")
#             if line in file3.readlines():
#                 print('重复跳过')
#                 continue
#             file2.write(line)           
#     finally:
#         file1.close()
#         file2.close()


# if __name__ == '__main__':
#     clearBlankLine()


#coding:utf-8
# ---------------------------- -----------去重复行------------------------------
readDir = "xjt.txt"
writeDir = "xjt1.txt"
outfile=open(writeDir,"w")
f = open(readDir,"r")
 
lines_seen = set()  # Build an unordered collection of unique elements.
 
for line in f:
    line = line.strip('\n')
    if line not in lines_seen:
        outfile.write(line+ '\n')
        lines_seen.add(line)

# -----------------------------------------------------------------------------------------------------
# csv to txt 
# import csv,shutil
 
 
# a=open('data2.csv','r')
# reader = csv.reader(a)
 
# with open('xjt1.txt','a',encoding='gbk', errors = "ignore") as f:
    
#     for i in reader:
#         for x in i:
#             f.write(x)
#             f.write('\t')
#         f.write('\n')
# a.close()
 
# shutil.copy('xjt1.txt','xjt2.txt')
 
# with open('xjt2.txt','r') as f:
#     print(f.read())
#  --------------------------------------------------------------------------------------------------------

# import json
# file = open('xjt1.txt', 'r', encoding='gbk', errors = "ignore") # 生成没有空行的文件
# with open("jt.json", 'r', encoding = "utf-8") as z:
#     try:
#         for b in z:
#             print(b)
#             if b in file.readlines():
#                 print('重复跳过')
#                 continue
#             file.write(b)       
#     finally:
#         file.close()


# from binascii import a2b_base64
# import json
# file = open('xjt4.txt', 'w+', encoding='gbk', errors = "ignore") # 生成没有空行的文件
# with open("djt.json", 'r', encoding = "utf-8") as z:
#     b = [x["content"] for x in json.load(z)]
#     values = b
#     for a in values:
#         file.write(a+"\n")

