#!/usr/bin/python

Usage = """
creates a job file for desired number of commands per job
Usage:
  makePBSp.py <number of jobs per PBS file> <commands file>
eg:
  
  makePBSp.py 10 bowtie2.cmds
will create bowtie2_N.sub files, where N equals to number of lines in bowtie2.cmds divided by 10
If you have large number of commands that you would like to package (a set number) in a single
PBS script file, you can run this script along with desired number of commands per job.
Note that all commands will run in parallel with this script (p suffix). If you want to run one command
at a time then use the s suffix script 
Arun Seetharam
arnstrm@iastate.edu
11/08/2016
"""
import sys
import os
if len(sys.argv)<3:
    print Usage
else:
   cmdargs = str(sys.argv)
   cmds = open(sys.argv[2],'r')
   jobname = str(os.path.splitext(sys.argv[2])[0])
   filecount = 0
   numcmds = int(sys.argv[1])
   line = cmds.readline()
   while line:
        cmd = []
        while len(cmd) != int(sys.argv[1]):
                cmd.append(line)
                line = cmds.readline()
        w = open(jobname+'_'+str(filecount)+'.sub','w')
        w.write("#!/bin/bash\n")
        w.write("#SBATCH -N 1\n")
        w.write("#SBATCH -n 4\n")
        w.write("#SBATCH -t 80:00:00\n")
	w.write("#SBATCH --mem=100gb\n")
	w.write("#SBATCH --tmp=300gb\n")
        w.write("#SBATCH -J "+jobname+"_"+str(filecount)+"\n")
        w.write("#SBATCH -o "+jobname+"_"+str(filecount)+".o%j\n")
        w.write("#SBATCH -e "+jobname+"_"+str(filecount)+".e%j\n")
        w.write("#SBATCH --mail-user=qiuxx221@umn.edu\n")
        w.write("#SBATCH --mail-type=ALL\n")
	w.write("conda_envir_replace\n")
	w.write("source ~/anaconda2/etc/profile.d/conda.sh\n")
	w.write("conda activate Widiv_SV_py3\n")
	w.write("module load bcftools\n")
        w.write("cd /scratch.global/qiuxx221/bam_picard_xaef/picard_xaef_bam/\n")
        w.write("module load samtools\n")
        w.write("parallel -j 1 --joblog "+jobname+"_progress_"+str(filecount)+".log --workdir $PWD <<FIL\n")
        count = 0
        while (count < numcmds):
           w.write(cmd[count])
           count = count + 1
        w.write("FIL\n")
        w.write("scontrol show job $SLURM_JOB_ID\n")
        w.close()
        filecount += 1
