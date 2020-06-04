@echo off
set KP_SHOW=%1
set KP_SHOT=%2
set KP_SCENE=%KP_SHOT:~0,3%
set KP_SHOWDIR=k:/PROJECTS/Personal/%KP_SHOW%/
set KP_SHOTDIR=k:/PROJECTS/Personal/%KP_SHOW%/%KP_SHOT%/
set KP_SHELL="CMD"

set argC=0
for %%x in (%*) do Set /A argC+=1

if %argC% == 2 (

    if exist %KP_SHOWDIR% (
        if exist %KP_SHOTDIR% (

            k:
            cd %KP_SHOTDIR%
            echo == GO TO SHOT =========
            echo Show:   %KP_SHOW%
            echo Scene:  %KP_SCENE%
            echo Shot:   %KP_SHOT%
            echo Dir:    %KP_SHOTDIR%
            echo =======================
            dir /ad /b
            echo =======================
            echo "- cdnuke: nuke workbench dir"
            echo "- cdmaya: maya workbench dir"
            echo "- cdlgt:  lighting renders dir"
            echo "- cddelivery:  delivery renders dir"
            title %KP_SHOW%:%KP_SCENE%:%KP_SHOT%

            doskey cdnuke=cd "%KP_SHOTDIR%workbench/nuke/"
            doskey cdmaya=cd "%KP_SHOTDIR%workbench/maya/scenes/"
            doskey cdlgt=cd "%KP_SHOTDIR%assets/lighting/"
            doskey cddelivery=cd "%KP_SHOWDIR%_delivery/"
            doskey ls=dir /a /b /od

        ) else (
            echo.
            echo %KP_SHOT% does not exist
        )
    ) else (
        echo.
        echo %KP_SHOW% does not exist
    )

) else (
    echo insufficient arguments
    echo "go <show_codename> <shot_name>"
)
