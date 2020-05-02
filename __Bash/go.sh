#! /bin/bash
export KP_SHOW=$1
export KP_SCENE=${2::-4}
export KP_SHOT=$2

export WSLENV=$KP_SHOW:$KP_SCENE:$KP_SHOT


SHOTPATH="/mnt/ku/PROJECTS/Personal/${KP_SHOW}/${KP_SHOT}"
WINPATH="K:/${SHOTPATH:8}"

if [[ $# -eq 2 ]]
then
    if [[ -d "${SHOTPATH}" ]]
    then
        cd $SHOTPATH
        echo "== GO TO SHOT ========="
        echo "WinDir: $WINPATH"
        echo "Show:   $KP_SHOW"
        echo "Scene:  $KP_SCENE"
        echo "Shot:   $KP_SHOT"
        echo "======================="
        ls --color=never
        echo "======================="
        echo "- cdnuke: nuke workbench dir"
        echo "- cdmaya: maya workbench dir"
        echo "- cdlgt:  lighting renders dir"

        PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]$KP_SHOW:$KP_SHOT\[\033[00m\]@\[\033[01;32m\]\W\[\033[00m\]: "

        alias cdnuke="cd ${SHOTPATH}/workbench/nuke/"
        alias cdmaya="cd ${SHOTPATH}/workbench/maya/scenes/"
        alias cdlgt="cd ${SHOTPATH}/assets/lighting/"

    elif [[ -d "/mnt/ku/PROJECTS" ]]
    then
        echo "SHOW or SHOT does not exist"
        echo "...Change dir to ku/PROJECTS" && cd "/mnt/ku/PROJECTS/"
        read -p "...[Personal or Clients] " type
        cd $type && echo "--------------------"
        ls --color=never && echo "--------------------"
    else
        echo "ku server not mounted"
        echo "mounting ku server..."
        mountku
        echo "...done"
    fi
else
    echo "insufficient argument"
    echo "go <show> <shot>"
fi
