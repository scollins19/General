import os

#Define directory to get input and place output
seq_dir='trimmed_out'
fastqc_dir='fastqc_trimmed_out'

#Make output directory
os.mkdir(fastqc_dir)

file_list = os.listdir(seq_dir) #List files in input directory

#For each file in input directory, apply fastqc <given path name of file>:
for seq in file_list:
   command='fastqc ' + seq_dir + '/' + seq
   print(command)
   os.system(command)#command to execute fastqc command

#Move every HTML file to the output directory
command1 = 'mv ' + seq_dir + '/' + '*.html ' + fastqc_dir
print(command1)
os.system(command1)
#Move every HTML file to the output directory
command2 = 'mv ' + seq_dir + '/' + '*.zip ' + fastqc_dir
print(command2)
os.system(command2)

print('done')


