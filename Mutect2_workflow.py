import subprocess, glob, re
from ruffus import *

@transform(["*_WEX.bam"],suffix("_WEX.bam"), "_samplename.txt")
def GetSampleName(infile,outfile):
    # Write the sample name contained within the SM tag of the bam files to a text file. The samplename will\
    # provided as an argument to Mutect2
    name_cmds=["java","-Xmx8g", "-jar", "/data4/siobhan/Practicals/gatk-package-4.0.12.0-local.jar", \
               "GetSampleName","-I",infile,"-O", outfile]
    subprocess.Popen(name_cmds,stdout=subprocess.PIPE).communicate()

@follows(GetSampleName)
@collate(["*_WEX.bam"],formatter("([^/]+)_[TN]_WEX.bam"),"{path[0]}/{1[0]}_mutect2.vcf.gz")
def InitialMutect2(infile,outfile):
    #Generate filename for bamfiles output by Mutect2
    bamfile=re.sub("vcf.gz","bam",outfile)
    # Get corresponding name for file containing the sample name for each bam file
    samplenamefile1=re.sub("_WEX.bam","_samplename.txt",infile[0])
    samplenamefile2 =re.sub("_WEX.bam", "_samplename.txt", infile[1])
    with open(samplenamefile1, "r") as samplename1:
        first_line = samplename1.readline()
        if "_T_" in samplenamefile1:
            tumorname=first_line.strip()
        else:
            normalname=first_line.strip()
    with open(samplenamefile2, "r") as samplename2:
        first_line = samplename2.readline()
        if "_T_" in samplenamefile2:
            tumorname=first_line.strip()
        else:
            normalname=first_line.strip()
    #Run Mutect2
    mutect2_cmds=["java","-Xmx8g", "-jar", "/data4/siobhan/Practicals/gatk-package-4.0.12.0-local.jar", "Mutect2", "-R", \ 
		"/data4/siobhan/\Practicals/GRCh37-lite.fa","-I",infile[1], "-I", infile[0], "-tumor",tumorname,"-normal",normalname,"-O", \ 			outfile, "-bamout", bamfile, "--germline-resource","/data4/siobhan/Practicals/1000G_phase3_v4_20130502.chr17_sites.vcf.gz"]
    subprocess.Popen(mutect2_cmds,stdout=subprocess.PIPE).communicate()

@follows(InitialMutect2)
@transform(["*_mutect2.vcf.gz"],suffix("_mutect2.vcf.gz"), "_filtercalls.vcf.gz")
def FilterMutectCalls(infile, outfile):
    # Filter for confident somatic calls
    filter_cmds=["java","-Xmx8g", "-jar", "/data4/siobhan/Practicals/gatk-package-4.0.12.0-local.jar", "FilterMutectCalls","-V",infile, "-O", outfile]
    subprocess.Popen(filter_cmds, stdout=subprocess.PIPE).communicate()



@follows(FilterMutectCalls)
@transform(["*_mutect2.bam"],suffix("_mutect2.bam"), "_summary")
def CollectSequencingArtifactMetrics(infile, outfile):
    CollectSeqMet_cmds=["java","-Xmx8g", "-jar", "/data4/siobhan/Practicals/gatk-package-4.0.12.0-local.jar",
"CollectSequencingArtifactMetrics", "-R", "/data4/siobhan/Practicals/GRCh37-lite.fa", "-I", infile, "-O", outfile]
    subprocess.Popen(CollectSeqMet_cmds, stdout=subprocess.PIPE).communicate()



@follows(CollectSequencingArtifactMetrics)
@transform(["*_filtercalls.vcf.gz"],suffix("_filtercalls.vcf.gz"), "_oxog_filtered.vcf.gz")
def FilterByOrientationBias(infile, outfile):
    preadapterfile = re.sub("_filtercalls.vcf.gz", "_summary.pre_adapter_detail_metrics",infile)
    filterO_cmds=["java","-Xmx8g", "-jar", "/data4/siobhan/Practicals/gatk-package-4.0.12.0-local.jar", "FilterByOrientationBias", "-V", infile, "--artifact-modes", "G/T", "-P", preadapterfile, "-O", outfile]
    subprocess.Popen(filterO_cmds, stdout=subprocess.PIPE).communicate()

    

pipeline_run([GetSampleName, InitialMutect2,FilterMutectCalls,CollectSequencingArtifactMetrics,FilterByOrientationBias], 
multiprocess=2)

