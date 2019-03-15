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
