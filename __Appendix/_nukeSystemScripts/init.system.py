# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

# Not to be confused with __init__.py, this file is sourced by Nuke whenever it
# is run, either interactively or in order to run a script. The main purpose is
# to setup the plugin_path and to set variables used to generate filenames.

# During startup the nuke lib loads this module, and a couple others, in the following order:
#   _pathsetup.py
#   init.py
#   menu.py
# _pathsetup has to be first since it sets up the paths to be able to 'import nuke'.

import sys
import os.path
import nuke
import threading

# FIXME: import nuke does not yet support OCIO which is required by the
#        default ViewerProcesses
ocioSupported = not nuke.env["ExternalPython"]
if ocioSupported :
  import nukescripts.ViewerProcess

# always use utf-8 for all strings
if hasattr(sys, "setdefaultencoding"):
  sys.setdefaultencoding("utf_8")

def threadendcallback():
  return nuke.waitForThreadsToFinish()

threading.currentThread().waitForThreadsOnExitFunc = threadendcallback

# NUKE_TEMP_DIR is initialized in _pathsetup.py
try:
  nuke_temp_dir = os.environ["NUKE_TEMP_DIR"]
except:
  nuke_temp_dir = ""
  assert False, "$NUKE_TEMP_DIR should have been set in _pathsetup.py nuke package has been successfully imported but it didn't set the variable"

# Stuff the NUKE_TEMP_DIR setting into the tcl environment.
# For some reason this isn't necessary on windows, the tcl environment
# gets it from the same place python has poked it back into, but on
# OSX tcl thinks NUKE_TEMP_DIR hasn't been set.
# But we'll do it all the time for consistency and 'just in case'.
# It certainly shouldn't do any harm or we've got another problem...
nuke.tcl('setenv','NUKE_TEMP_DIR',nuke_temp_dir)

for location in nuke.pluginInstallLocation():
  nuke.pluginAddPath(location, addToSysPath=False)
  for root, dirs, files in os.walk(location):
    if root != location:
      nuke.pluginAddPath(root, addToSysPath=False)

nuke.pluginAddPath("./user", addToSysPath=False)

execdir = os.path.dirname(sys.executable)
sys.path.append(execdir + "/plugins/modules")

# Knob defaults
#
# Set default values for knobs. This must be done in cases where the
# desired initial value is different than the compiled-in default.
# The compiled-in default cannot be changed because Nuke will not
# correctly load old scripts that have been set to the old default value.
nuke.knobDefault("Read.r3d.r3d_gamma_curve", "Half Float Linear")
nuke.knobDefault("Read.r3d.r3d_colorspace", "REDcolor3")
#nuke.knobDefault("Read.label", '[if {[exists r3d_gamma_curve] && [exists r3d_colorspace]} {return "[value r3d_gamma_curve] / [value r3d_colorspace]"}]')
nuke.knobDefault("ReadGeo2.abc.read_on_each_frame", "true")
nuke.knobDefault("ReadGeo2.fbx.read_on_each_frame", "true")
nuke.knobDefault("AppendClip.meta_from_first", "false")
nuke.knobDefault("Assert.expression", "{{true}}")
nuke.knobDefault("Assert.message", "[knob expression] is not true")
nuke.knobDefault("PostageStamp.postage_stamp", "true")
nuke.knobDefault("Keyer.keyer", "luminance")
nuke.knobDefault("Copy.from0", "rgba.alpha")
nuke.knobDefault("Copy.to0", "rgba.alpha")
nuke.knobDefault("Constant.channels", "rgb")
nuke.knobDefault("ColorWheel.gamma", ".45")
nuke.knobDefault("Truelight.label", "Truelight v2.1")
nuke.knobDefault("Truelight3.label", "Truelight v3.0")
#nuke.knobDefault("ScannedGrain.fullGrain", "[file dir $program_name]/FilmGrain/")
nuke.knobDefault("SphericalTransform.fix", "True");
nuke.knobDefault("Environment.mirror", "True");
nuke.knobDefault("TimeBlur.shutteroffset", "start")
nuke.knobDefault("TimeBlur.shuttercustomoffset", "0")
nuke.knobDefault("TimeClip.mask_metadata", "1")
nuke.knobDefault("Truelight.output_raw", "true")
nuke.knobDefault("Truelight3.output_raw", "true")
nuke.knobDefault("Root.proxy_type", "scale")
nuke.knobDefault("Text.font",nuke.defaultFontPathname())
nuke.knobDefault("Text2.font", "{ Utopia : Regular : UtopiaRegular.pfa : 0 }")
nuke.knobDefault("Text.yjustify", "center")
nuke.knobDefault("Text2.yjustify", "top")
nuke.knobDefault("ScanlineRender.output_motion_vectors_type", "distance")
nuke.knobDefault("ScanlineRender.conservative_shader_sampling", "false")
nuke.knobDefault("Median.ignore_top_line", "false");
nuke.knobDefault("PrmanRender.jitter", "false")
nuke.knobDefault("PrmanRender.shading_rate", "4")
nuke.knobDefault("PrmanRender.pixel_samples", "1")
nuke.knobDefault("PrmanRender.output_motion_vectors_type", "2")
nuke.knobDefault("DeepRead.dtex.discrete", "0")
nuke.knobDefault("Vectorfield.output_bitdepth_id", "auto")
nuke.knobDefault("Vectorfield.format_3dl_id", "auto")
nuke.knobDefault("Vectorfield.normalize_output", "false")
nuke.knobDefault("Primatte.bg_color_selected", "false")
nuke.knobDefault("Primatte3.bg_color_selected", "false")
nuke.knobDefault("Roto.output", "alpha")
nuke.knobDefault("Light.depthmap_slope_bias", "0.01")
nuke.knobDefault("Light2.depthmap_slope_bias", "0.01")
nuke.knobDefault("DirectLight.depthmap_slope_bias", "0.01")
nuke.knobDefault("Spotlight.depthmap_slope_bias", "0.01")
nuke.knobDefault("PositionToPoints.display", "textured")
nuke.knobDefault("PositionToPoints.render_mode", "textured")
nuke.knobDefault("ReadGeo2.abc.use_geometry_colors", "false")
nuke.knobDefault("Kronos.motionEstimation", "Regularized")
nuke.knobDefault("Kronos.legacyModeNuke9", "false")
nuke.knobDefault("Kronos.showLegacyMode", "false")
nuke.knobDefault("Kronos.retimedChannels", "all")
nuke.knobDefault("VectorGenerator.motionEstimation", "Regularized")
nuke.knobDefault("MotionBlur.motionEstimation", "Regularized")
nuke.knobDefault("Write.mov.mov64_bitrate", "20000")
nuke.knobDefault("Write.mov.codec", "ap4h")
nuke.knobDefault("Write.mov.mov64_codec", "ap4h")
nuke.knobDefault("ZDefocus.legacy_resize_mode", "false")
nuke.knobDefault("ZDefocus.show_legacy_resize_mode", "false")


# Register default ViewerProcess LUTs.
if ocioSupported :
  nukescripts.ViewerProcess.register_default_viewer_processes()

# Here are some more examples of ViewerProcess setup.
#
# nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT", "current Cineon"))
#
# Note that in most cases you will want to create a gizmo with the appropriate
# node inside and only expose parameters that you want the user to be able
# to modify when they open the Viewer Process node's control panel.
#
# The "apply LUT to color channels only" option will only work with ViewerProcess LUTs if they have
# a "rgb_only" knob set to 1.
#
# The VectorField node can be used to apply a 3D LUT.
# VectorField features both software (CPU) and GPU implementations.
#
# nuke.ViewerProcess.register("3D LUT", nuke.createNode, ("Vectorfield", "vfield_file /var/tmp/test.3dl"))
#
# You can also use the Truelight node.
#
# nuke.ViewerProcess.register("Truelight", nuke.createNode, ("Truelight", "profile /Applications/Nuke5.2v1/Nuke5.2v1.app/Contents/MacOS/plugins/truelight3/profiles/KodakVisionPremier display sRGB enable_display true"))

# register some file extensions to show up in the file browser as sequences
nuke.addSequenceFileExtension("ari");
nuke.addSequenceFileExtension("arri");
nuke.addSequenceFileExtension("bmp");
nuke.addSequenceFileExtension("cin");
nuke.addSequenceFileExtension("crw");
nuke.addSequenceFileExtension("cr2");
nuke.addSequenceFileExtension("dpx");
nuke.addSequenceFileExtension("dng");
nuke.addSequenceFileExtension("deepshad");
nuke.addSequenceFileExtension("dshd");
nuke.addSequenceFileExtension("dtex");
nuke.addSequenceFileExtension("exr");
nuke.addSequenceFileExtension("fpi");
nuke.addSequenceFileExtension("ftif");
nuke.addSequenceFileExtension("ftiff");
nuke.addSequenceFileExtension("gif");
nuke.addSequenceFileExtension("hdr");
nuke.addSequenceFileExtension("hdri");
nuke.addSequenceFileExtension("iff");
nuke.addSequenceFileExtension("iff16");
nuke.addSequenceFileExtension("it8");
nuke.addSequenceFileExtension("jpeg");
nuke.addSequenceFileExtension("jpg");
nuke.addSequenceFileExtension("nkpc"); # Nuke particle cache
nuke.addSequenceFileExtension("obj");
nuke.addSequenceFileExtension("pic");
nuke.addSequenceFileExtension("png");
nuke.addSequenceFileExtension("png16");
nuke.addSequenceFileExtension("psd");
nuke.addSequenceFileExtension("rgb");
nuke.addSequenceFileExtension("rgba");
nuke.addSequenceFileExtension("rgbe");
nuke.addSequenceFileExtension("rgbea");
nuke.addSequenceFileExtension("rla");
nuke.addSequenceFileExtension("sgi");
nuke.addSequenceFileExtension("sgi16");
nuke.addSequenceFileExtension("sxr");
nuke.addSequenceFileExtension("targa");
nuke.addSequenceFileExtension("tga");
nuke.addSequenceFileExtension("tif");
nuke.addSequenceFileExtension("tiff");
nuke.addSequenceFileExtension("tif16");
nuke.addSequenceFileExtension("tiff16");
nuke.addSequenceFileExtension("yuv");
nuke.addSequenceFileExtension("xpm");
nuke.addSequenceFileExtension("");

# Pickle support

class __node__reduce__():
  def __call__(s, className, script):
    n = nuke.createNode(className, knobs = script, inpanel = False)
    for i in range(n.inputs()): n.setInput(0, None)
    n.autoplace()
__node__reduce = __node__reduce__()

class __group__reduce__():
  def __call__(self, script):
    g = nuke.nodes.Group()
    with g:
      nuke.tcl(script)
    for i in range(g.inputs()): g.setInput(0, None)
    g.autoplace()
__group__reduce = __group__reduce__()


# Define image formats:
nuke.load("formats.tcl")
# back-compatibility for users setting root format in formats.tcl:
if nuke.knobDefault("Root.format")==None:
  nuke.knobDefault("Root.format", nuke.value("root.format"))
  nuke.knobDefault("Root.proxy_format", nuke.value("root.proxy_format"))

def addProfileOutput(filename):
  print "TIMING ENABLED: profile will be saved to " + filename
  import nukescripts
  nukeProfiler = nukescripts.NukeProfiler()
  nukeProfiler.setPathToFile(filename)
  nuke.addBeforeRender(nukeProfiler.resetTimersAndStartProfile)
  nuke.addAfterFrameRender(nukeProfiler.addFrameProfileAndResetTimers)
  nuke.addOnScriptClose(nukeProfiler.endProfile)

if nuke.usingPerformanceTimers():
  profileFile = nuke.performanceProfileFilename()
  if profileFile != None:
    addProfileOutput(profileFile)


