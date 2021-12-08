# Mumax/pcss/post-processing Workflow

# PCSS and Linux ( or wsl )

# Setting up an ssh key 
Ressource : [This website](https://www.ssh.com/academy/ssh/key) has a lot of info about SSH in general

Using a key is faster and more safe than using a password
`ssh-keygen` to create a key, it's better to just leave the default parameters and press Enter a bunch of times

`ssh-copy-id username@eagle.man.poznan.pl` (change `username`) used to transfer your public key to pcss ( if everything goes right this should be the last time you use your password to access pcss)

`ssh username@eagle.man.poznan.pl` you should be able to connect to pcss without any credential ( the default key path is `~/.ssh/id_rsa` and you don't need to specify it if you didn't change the name)

I'm lazy, so I add this line in my .bashrc:
`alias sp='ssh -t mathieum@eagle.man.poznan.pl'`

I can log into pcss just typing `sp`

# Mounting a PCSS folder locally

`sshfs username@eagle.man.poznan.pl:/home/users/username/my_pcss_folder /home/local_username/my_local_folder`

`sshfs` will mount any folder through ssh. Both folders, local and remote will be kept in sync. You can mount any folder you want, anywhere, but I advise you only mount in your home directory to avoid permission issues. You also can add many arguments to this command, for example :

`sshfs -o allow_other -o kernel_cache -o auto_cache -o reconnect -o compression=no -o cache_timeout=600 -o no_readahead -o big_writes -o ServerAliveInterval=15 username@eagle.man.poznan.pl:/home/users/username/my_pcss_folder /home/local_username/my_local_folder`

# Setting up mumax on PCSS

Mumax is hardly supported anymore, I forked and modified the source code. My version can be found on [github](https://github.com/MathieuMoalic/amumax) 

Contact me if you find any bugs or want something implemented.

Make your life easier, set up simple scripts to automate your workflow
## Examples :
```bash
export SLURM_TIME_FORMAT="%H:%M:%S"
alias rl='source ~/.bashrc'
alias sq='sacct -X --format=JobID,JobName%22,State,Elapsed,Submit%10,Start%10,End%10,Nodelist%8,Timelimit -S $(date -d "3 days ago" +%D-%R)'
alias q='bash ~/scripts/autostart.sh'
alias q1='bash ~/scripts/autostart1.sh'
```
Note: My full configuration and these scripts are available in this repository.


`rl` will reload your .bashrc if you made changes

`sq` will show all jobs submitted by you in the last 3 days using the time formating `"%H:%M:%S"`

`q` and `q1` are the following scripts :

```bash
#!/bin/bash
for file in *.mx3; do 
    echo $file
    sbatch --job-name="${file/.mx3/}" --output="${file/.mx3/}.logs" $HOME/scripts/mumax_job.sh $file
done
```
and 
```bash
#!/bin/bash
file=$1
sbatch --job-name="${file/.mx3/}" --output="${file/.mx3/}.logs" $HOME/scripts/mumax_job.sh $file
```
They just queue all .mx3 files in the folder ( or just a single 1 with `q1`) using this batch script :

```bash
#!/bin/bash -l
#SBATCH --nodes=1
#SBATCH --mem=4G
#SBATCH --time=15:00:00
#SBATCH --partition=tesla 
#SBATCH --gres=gpu:1
#SBATCH --exclude=gpu09

module load cuda/10.2.89_440.33.01
TMPDIR="/mnt/storage_2/scratch/grant_398/mumax_kernels/"
file=$1
$HOME/go/bin/amumax -http=":$2" -cache="/mnt/storage_2/scratch/grant_398/mumax_kernels/" $file
mv "${file/.mx3/}.logs" "${file/.mx3/.out}/slurm.logs"
mv "$file.zarr" "$file.zarr"
```

`TMPDIR` is necessary to cache the mumax kernels in a global folder so they can be reused, this folder is shared by the whole group so we can use eachother's kernels.

`~go/bin/mumax3`: path my compiled mumax

`mv "${file/.mx3/}.logs" "${file/.mx3/.out}/slurm.logs"`: it just moves the batch logs inside my output folder so it's easier to keep everything clean.



# virtualenv
You need to use a virtualenv, [miniconda](https://repo.anaconda.com/miniconda) is good but feel free to use any of them.

To install it in pcss, you can use these commands :

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh
```
```
bash ./Miniconda3-py39_4.10.3-Linux-x86_64.sh
```
if you take the recommanded default option during the installation, the base virtualenv should be activated everytime you open a shell session.
With miniconda, you can use `conda` instead of `pip` i.e:

`conda install -c conda-forge jupyterlab`
In 99% of the cases, it's the same as using `pip` but sometimes it's better at packaging additional binaries and prevent some obscure platform dependant bugs.

# Jupyter
You need Jupyter to post-process your data quickly and efficiently, it's the default tool for data scientists all over the world.
Install jupyter `conda install -c conda-forge jupyterlab` 

You can also use the `Jupyter` extension in VSCode, it's the same thing, just a different UI.

For small amounts of data, it's okay to just process it locally, but if it gets large, it will take time to transfer locally.

The solution: Run the jupyter server on a pcss node with (almost) infinite resources. But then you need to create an ssh tunnel between the node on pcss and your pc, for example, I would use:

`ssh -N -L 8888:e0123:8888 mathieum@eagle.man.poznan.pl`

More examples [here](https://www.ssh.com/academy/ssh/tunneling/example)

`8888` is the default port for Jupyter
`e0123` is the name of a CPU node on PCSS, **it changes every time**
