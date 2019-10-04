# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

import os
import nuke

def __concat_result_string(name, label):
  if label is None or label == "":
    return name
  return str(name + "\n" + label).strip()


def _stripDefaultStrings(colorspace):
  if colorspace.startswith("default") :
    if colorspace == "default" :
      colorspace = "" # this should not happen, this is the final fallback is all else has gone wrong
    else:
      colorspace = colorspace[9:-1] # strip off "default (" and ")"
      if colorspace == "custom" :
        colorspace = ""
  return colorspace


def _getAutoLableColorspace():
  """
  returns the colorspace-name string to use on auto-labels
  handles defaults, NUKE vs OCIO modes and NUKE UI.
  """
  csKnob = nuke.thisNode().knob("colorspace")
  if not csKnob :
    return ""
  csId = int(csKnob.getValue())
  if not nuke.usingOcio():
    isDefault = (0 == csId)
    if isDefault :
      # maintaining old behaviour, don't show the colorspace in the autolabel
      # in NUKE colorspace mode
      return ""

  # always show non-empty colorspaces
  colorspace = _stripDefaultStrings( csKnob.values()[csId] )

  if not colorspace:
     # fall back to tcl if we don't have a colorspace
     colorspace = _stripDefaultStrings( nuke.value("colorspace") )

  # strip cascading menus prefix
  colorspace = os.path.basename(colorspace)
  assert colorspace != "."
  return colorspace


def autolabel():
  """This function is run automatically by Nuke during idle, and the return
  text is drawn on the box of the node. It can also have side effects by
  setting knobs. Currently two knobs are provided that are useful:

  indicators = integer bit flags to turn icons on/off. The icons
  named indicator1, indicator2, indicator4, indicator8, etc are
  drawn if the corresponding bit is on. By default these are loaded
  from the path as indicator1.xpm, etc, but you can use the load_icon
  command to load other files.

  icon = name of a whole extra image you can draw, but it replaces
  any previous one."""

  # do the icons:
  ind = nuke.expression("(keys?1:0)+(has_expression?2:0)+(clones?8:0)+(viewsplit?32:0)")

  if int(nuke.numvalue("maskChannelInput", 0)) :
    ind += 4
  if int(nuke.numvalue("this.mix", 1)) < 1:
    ind += 16
  nuke.knob("this.indicators", str(ind))

  this = nuke.toNode("this")

  # do stuff that works even if autolabel is turned off:
  name = nuke.value("name")
  _class = this.Class()

  label = nuke.value("label")
  if not label:
    label = ""
  else:
    try:
      label = nuke.tcl("subst", label)
    except:
      pass

  if _class == "Dot" or _class == "BackdropNode" or _class == "StickyNote":
    return label
  elif _class.startswith("Read") or _class.startswith("Write") or _class.startswith( "Precomp" ):
    reading = int(nuke.numvalue("this.reading", 0 ))

    if reading and _class.startswith( "Precomp" ):
      filename = nuke.filename( node = this.output().input(0), replace = nuke.REPLACE )
    else:
      filename = nuke.filename(replace = nuke.REPLACE)
    if filename is not None:
      name = __concat_result_string(name, os.path.basename(filename))

    if reading:
      checkHashOnRead = False
      if _class.startswith( "Precomp" ):
        if this.output() != None and this.output().input(0) != None:
          checkHashOnReadKnob = this.output().input(0).knob( "checkHashOnRead" )
          if checkHashOnReadKnob:
            checkHashOnRead = checkHashOnReadKnob.value()
      else:
        checkHashOnRead = this.knob("checkHashOnRead").value()

      if checkHashOnRead == True and ( this.proxy() != True ):
        name = name + "\n(Read)"
      else:
        name = name + "\n(Read - unchecked)"
  elif _class == 'DeepRead':
    filename = nuke.filename(replace = nuke.REPLACE)
    if filename is not None:
      name =  __concat_result_string(name, os.path.basename(filename))
  elif _class.startswith("ParticleCache" ):
    rendering = int(nuke.numvalue("this.particle_cache_render_in_progress", 0 ))
    if rendering:
      name = name + "\n(Rendering)"
    else:
      reading = int(nuke.numvalue("this.particle_cache_read_from_file", 0 ))
      if reading:
        name = name + "\n(Read)"

  if nuke.numvalue("preferences.autolabel") == 0 or _class.find("OFX", 0) != -1:
    return __concat_result_string(name, label)

  # build the autolabel:
  operation = nuke.value('this.operation', '')
  if operation != '' and _class != 'ChannelMerge' and _class != 'Precomp':
    name = name + ' (' + operation + ')'

  layer = nuke.value("this.output", nuke.value("this.channels", "-"))
  mask = nuke.value("this.maskChannelInput", "none")
  unpremult = nuke.value("this.unpremult", "none")

  if _class.startswith("Read") or _class.startswith("Write"):
    # do colorspace labeling for reads and writes
    if int(nuke.numvalue("this.raw", 0)):
      layer = "RAW"
    else:
      colorspace = _getAutoLableColorspace()

      # additional to NUKE-mode default colorspaces not being shown, if the
      # colorspace is set to "custom" (aka unintialised) in the UI the name
      # comes through as empty, so ignore it.
      if colorspace:
        layer = colorspace

    if _class.startswith("Write"):
      order = nuke.numvalue("this.render_order", 1)
      mask = str(order)
      if int(order) == 1:
        mask = "none"
  elif _class == "Reformat":
    if nuke.expression("!type"):
      format = nuke.value("format")
      rootformat = nuke.value("root.format")
      if format is not None and format != rootformat:
        format_list = format.split()
        layer = " ".join(format_list[7:])
  elif _class == "ChannelMerge":
    if operation == "union":
      operation = "U"
    elif operation == "intersect":
      operation = "I"
    elif operation == "stencil":
      operation = "S"
    elif operation == "absminus":
      operation = "abs-"
    elif operation == "plus":
      operation = "+"
    elif operation == "minus":
      operation = "-"
    elif operation == "multiply":
      operation = "*"
    layer = nuke.value("A") + " " + operation + " " + nuke.value("B") + " =\n" + nuke.value("output")
  elif _class == "Premult" or _class == "Unpremult":
    unpremult = nuke.value("alpha")
    if unpremult == "alpha":
      unpremult = "none"
  elif _class == "Copy":
    layer = ""
    if nuke.value("to0") != "none":
      layer += nuke.value("from0") + " -> " + nuke.value("to0")
    if nuke.value("to1") != "none":
      layer += "\n" + nuke.value("from1") + " -> " + nuke.value("to1")
    if nuke.value("to2") != "none":
      layer += "\n" + nuke.value("from2") + " -> " + nuke.value("to2")
    if nuke.value("to3") != "none":
      layer += "\n" + nuke.value("from3") + " -> " + nuke.value("to3")
    if nuke.value("channels") != "none":
      layer += ("\n" + nuke.value("channels") + "->" + nuke.value("channels"))
  elif _class == "FrameHold":
    value_inc = nuke.value("increment")
    if int(value_inc):
      layer = "frame "+nuke.value("knob.first_frame")+"+n*"+value_inc
    else:
      layer = "frame "+nuke.value("knob.first_frame")
  elif _class == "Precomp":
    layer = '-'

  if mask != "none":
    if int(nuke.numvalue("invert_mask", 0)):
      layer += (" / ~" + mask)
    else:
      layer += (" / " + mask)

  if unpremult != "none" and unpremult != mask and _class.find("Deep", 0) == -1:
    layer += ( " / " + unpremult)

  if layer != "rgba" and layer != "rgb" and layer != "-":
    result = __concat_result_string(name, "(" + layer + ")" + "\n" + str(label))
  else:
    result = __concat_result_string(name, label)

  return result

