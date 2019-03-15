# Naming Convension at different Studios

### MPC

ENV Variables

- `JOB`= show code (pok)
- `SCENE` = seq code (DIT)
- `SHOT` = seq/shotname (DIT/099_DIT0287)
- `SHOTNAME` = shot name (099_DIT0287)


Dir Structure

- Element/Render Files
  - `/jobs/<show>/<seq>/<shotname>/<type>/<filter>_<shotname>_v#/<resolution>/<filter>_<shotname>_v#.%04d.exr`
  - `/jobs/pok/HTR/087_HTR0293/elements/E_087_HTR0293_v4/2185x1798/E_087_HTR0293_v4.%04d.exr`
- Nuke Scripts
  - `/jobs/<show>/<seq>/<shotname>/nuke/comp/scene/<user>`
  - `/jobs/pok/HTR/087_HTR0293/nuke/comp/scene/tianlun-j`

Elements

- Comp
  - `<filter>_<shotname>_<label>_v#`
  - `E_087_HTR0293_v4`
- LGT
  - ``
