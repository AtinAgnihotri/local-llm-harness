uname -a >> localPCSpec.log
cat /etc/os-release >> localPCSpec.log
lscpu >> localPCSpec.log
free -h >> localPCSpec.log
df -h / >> localPCSpec.log
lspci | grep -Ei 'vga|3d|display' >> localPCSpec.log
nvidia-smi >> localPCSpec.log
which docker >> localPCSpec.log
which podman >> localPCSpec.log
which uv >> localPCSpec.log
which python3 >> localPCSpec.log
which git >> localPCSpec.log


df -h / >> localPCSpec.log
du -sh ~ >> localPCSpec.log
du -sh /home/atinagnihotri/work_repos/localLLM >> localPCSpec.log
