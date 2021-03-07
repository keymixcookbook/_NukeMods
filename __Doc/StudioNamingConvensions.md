# Naming Convension per Studio
- [MPC](#MPC)

### MPC

###### ENV Variables

- `JOB`= show code (pok)
- `SCENE` = seq code (DIT)
- `SHOT` = seq/shotname (DIT/099_DIT0287)
- `SHOTNAME` = shot name (099_DIT0287)
- `DEFAULT_DISCIPLINE` = department (compositing)


###### Dir Structure

- Root
  - `/jobs/<show>/<seq>/<shotname>`
  - `/jobs/pok/HTR/087_HTR0293`

- Element/Render Files (`~` as Root)
  - `~/<type>/<filter>_<shotname>_v#/<resolution>/<filter>_<shotname>_v#.%04d.exr`
  - `~/elements/E_087_HTR0293_v4/2185x1798/E_087_HTR0293_v4.%04d.exr`
- Nuke Scripts (`~` as Root)
  - `~/nuke/comp/scene/<user>`
  - `~/nuke/comp/scene/tianlun-j`

###### Elements

- Comp
  - `<filter>_<shotname>_<label>_v#`
  - `E_087_HTR0293_v4`
- LGT/FX
  - `<discipline>_<shotname>_<type>__<label>_<pass>`
  - `LGT_087_HTR0293_char__mewtwo_010_beauty`
- AOVs
  - `<LGT/FX>_<pass>_mono.%04d.exr`
  - `LGT_087_HTR0293_char__mewtwo_010_beauty_v20_diffuseDirect_mono.%04d.exr`
- Plate
  - `<shotname>_<type>_v##`
  - `087_HTR0293_MP01_v01`

###### Appendix

- AOVs (Renderman)
  - **Shading:** diffCol, diffDir, diffInd, emission, subsurface, specDir, specInd, leftovers
  - **MultiLights:** diffMulti[0-9], specMulti[0-9], emissiondiff, emissionspec
  - **Data:** depth2, norm, position2, refPosition2, uv2, id[0-]
- Types
  - **LGT:** fx, char, prop...
  - **Elements:** I, IDN, IC, IG, E, O, EMATTE...
  - **Plate(I/O):** MP, CP...

###### Nodes (Class names)

- ImagePlane
- HubCamera2



### SPI

###### ENV Variables

- `SHOW`= show code (tag)
- `SHOT` = shot code (pit1200)
- `SHOT_SEQUENCE` = sequence of the shot (pit)
- `show` = show dir (/shots/tag/)
- `shot` = dir of the shot (/shots/tag/pit1200/)
- `show_home` = home dir of show (099_DIT0287)


###### Naming Convension
- prefix
    - `maya_`: layout or animation play blast
    - `rnd_`: renders from katana or maya, lighting fx, hair, cloth
    - `tex_`: rendered(procedural) or painted textures
    - `raw_`: scans or painted fixes, not colour corrected
    - `out_`: comps, precomps
    - `fx_`: simulation files or renders of simulation
- suffix
    - `.katana`: katana files
    - `.pix`: image files
    - `.anim`: animation maya scene files
    - `.cmpt`: component geo files
    - `.asmb`: assembles of `.cmpt`
    - `.asmod`: modifier file of `.asmb`
    - `.depth`: lighting depth files
    - `.rlo`: rough layout maya scene
    - `.flo`: final layout maya scene
    - `.cloth`: cloth setup maya file
    - `.rig`: character maya file
    - `.cloth`: cloth setup maya file
    - `.txasn`: texture assignment file
    - `.nk`: nuke file
    - `.s3d_cam`: stereo camera source file
    - `.xml`: shot xml file
    - `.view`: view description file
    - `.maya`: maya file
- shots
    - prefix: `char`, `dev`, `env`, `trn`, `lib`, `seq`
    - suffix/extensions:
        - `.mpcap`
        - char: `.anim`, `.dyn`, `.hair`, `.model`, `.mtl`, `.rig`, `.cloth`, `.tex`
        - env: `.fx`, `.hair`, `.model`, `.mtl`, `.tex`
        - seq: `.layout`, `.lgt`
        - lib: `.bg`, `.rig`
- images
    - `<base>/<resolution>/<base>_<resolution>_<colourspace>.<ext>`
    - `<base>/<aov>_<resolution>_<colourspace>_<ext>/<base>_<aov>_<resolution>_<colourspace>.<ext>`
    - aovs: `aov_<type>_<pass_name>`
- modeling
    - product: `<product_type>_<product_name>` (`prop_ball`)
    - the hierarchy
        - `<product>`
            - `lod_<level>`: `hi`, `lo`
                - `<product>_<lod>_<position>_<child_geo_name>_<iterating_letters>`
    - lod level: `hi`, `lo`
    - position: `cn`, `lf`, `rt`
    - iterating letters: `top`, `bot`, `a`, `b`...


###### Dir Structure

**General dir**

`<product>/<version>/<representation>/`

- `<show>/`
    - `home/`
    - `char.<char_name>.model`
        - `maya/projects/`
        - `geometry/`
        - `pix/maya/`: display thumbneil
    - `char.<char_name>.tex`
        - `mayapnt`
        - `pix/maya/`
        - `pix/ptex/`: publish textures
    - `char.<char_name>.rig`
    - `char.<char_name>.hair`
    - `env.<env_name>.model`
    - `env.<env_name>.tex`
    - `env.<env_name>.rig`
    - `mocap.<seq_name>`
    - `seq.<seq_name>`: seq home dir
    - `seq.<seq_name>.layout`: seq home dir for rough layout
    - `<seq><shot###$>`
        - `cue/`
        - `log/`: cue log
        - `etc/`: to store shotenv variables
        - `comp/`
        - `kat/`
        - `hfs/<user>/`: houdini files
        - `maya/<user>/scenes/`: maya scene dirs
        - `geometry/`: geometry for acman
        - `data/`: particle and sim data
        - `pix/`: image files
            - `rnd/`: rendered elements
            - `out/`: final output
            - `plates/`: colour corrected plates
            - `raw/`: scans
            - `rtex/`: procedural textures
            - `ptex/`: painted textures
            - `mattes/`: rgba mattes or any mattes
            - `maya/`: maya playblast
            - `avi/`: movs or quicktimes
            - `pnt/`: paint plates or elements


###### Appendix

- AOVs (Arnold)

- Types


###### Nodes (Class names)

- SpRead2
- SpCamera2
