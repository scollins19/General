import os
#Define directory to get input and place output
seq_dir='test_dataset'
fastqc_dir='trimmed_out'

#Make output directory
os.mkdir(fastqc_dir)

file_list = os.listdir(seq_dir)#List files in input directory

#For each file in input directory, apply Trimmomatic
#<need to insert path to Trimmomatic> <need to include input file>
#<need to include output file which I just called 'trimmed-seq', for each seq>:
for seq in file_list:
   command= ('java -jar /home/scollins/Downloads/Trimmomatic-0.38/trimmomatic-0.38.jar SE -phred33 ' + seq_dir + '/' + seq + ' trimmed-' + seq + ' ILLUMINACLIP:/home/scollins/Downloads/Trimmomatic-0.38/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
   print(command)
   os.system(command)#command to execute trimmed command

#Move every trimmed file to the output directory
command1 = 'mv ' + 'trimmed-* ' + fastqc_dir
print(command1)
os.system(command1)

print('done')

