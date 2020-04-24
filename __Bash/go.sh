#! bin/bash
export KP_SHOW=$1
export KP_SCENE=${2::-4}
export KP_SHOT=$2


SHOTPATH="/mnt/ku/PROJECTS/Personal/${KP_SHOW}/${KP_SHOT}"
WINPATH="K:/${SHOTPATH:8}"


if [[ -d "${SHOTPATH}" ]]
then
    cd $SHOTPATH
    echo "== GO TO SHOT ========="
    echo "WinDir: $WINPATH"
    echo "Show:   $KP_SHOW"
    echo "Scene:  $KP_SCENE"
    echo "Shot:   $KP_SHOT"
    echo "======================="
    ls

    PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]$KP_SHOW:$KP_SHOT\[\033[00m\]@\[\033[01;32m\]\W\[\033[00m\]: "

    alias cdnuke="cd ${SHOTPATH}/workbench/nuke/"
    alias cdmaya="cd ${SHOTPATH}/workbench/maya/scenes/"
else
    echo "SHOW or SHOT does not exist"
fi
