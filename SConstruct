# -*- python -*-
#
# Setup our environment
#
import glob, os.path, sys
import lsst.SConsUtils as scons

dependencies = ["utils", "pex_exceptions"]

env = scons.makeEnv("obs_lsstSim",
                    r"$HeadURL$",
                    [
                    ])
env.Help("""
LSST Observatory configuration for LSST Simulations
""")

###############################################################################
# Boilerplate below here

pkg = env["eups_product"]
env.libs[pkg] += env.getlibs(" ".join(dependencies))

#
# Build/install things
#
for d in (
    ".",
    # "doc",
    # "examples",
    # "tests",
):
    if d != ".":
        try:
            SConscript(os.path.join(d, "SConscript"))
        except Exception, e:
            print >> sys.stderr, "In processing file %s:" % (os.path.join(d, "SConscript"))
            print >> sys.stderr, traceback.format_exc()
    Clean(d, Glob(os.path.join(d, "*~")))
    Clean(d, Glob(os.path.join(d, "*.pyc")))

env['IgnoreFiles'] = r"(~$|\.pyc$|^\.svn$|\.o$)"

Alias("install", [
    # env.Install(env['prefix'], "doc"),
    # env.Install(env['prefix'], "examples"),
    # env.Install(env['prefix'], "include"),
    # env.Install(env['prefix'], "lib"),
    env.Install(env['prefix'], "description"),
    env.Install(env['prefix'], "policy"),
    env.Install(env['prefix'], "python"),
    # env.Install(env['prefix'], "src"),
    # env.Install(env['prefix'], "tests"),
    env.InstallEups(os.path.join(env['prefix'], "ups")),
])

scons.CleanTree(r"*~ core *.so *.os *.o")

#
# Build TAGS files
#
files = scons.filesToTag()
if files:
    env.Command("TAGS", files, "etags -o $TARGET $SOURCES")

env.Declare()
