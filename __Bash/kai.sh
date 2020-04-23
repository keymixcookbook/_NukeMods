#! bin/bash
export KP_SHOW=$1
export KP_SHOT=$2

cd /mnt/ku/PROJECTS/Personal/${KP_SHOW}/${KP_SHOT}

echo "== OPEN SHOT =========="
echo "Show: $KP_SHOW"
echo "Shot: $KP_SHOT"
echo "======================="

PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]$KP_SHOW:$KP_SHOT\[\033[00m\]\$ "
