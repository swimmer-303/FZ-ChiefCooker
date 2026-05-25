import os
import sys
import pathlib
import lief

try:
    import certifi
    os.environ.setdefault("SSL_CERT_FILE", certifi.where())
except ImportError:
    pass

UFBT_PATH = pathlib.Path.home() / ".ufbt"

FAP_LOCATION_AFTER_BUILD = "dist/chief_cooker.fap"
FAP_LOCATION_ON_FLIPPER = "/ext/apps/Sub-GHz/chief_cooker.fap"
OBJCOPY_PATH = UFBT_PATH / "toolchain/current/bin/arm-none-eabi-objcopy"
RUNFAP_PATH = UFBT_PATH / "current/scripts/runfap.py"


def clearSections():
    binary = lief.parse(FAP_LOCATION_AFTER_BUILD)

    for i, sect in enumerate(binary.sections):
        if sect.name.find("_Z") >= 0:
            newSectName = "_s%d" % i
            cmd = '%s "%s" --rename-section %s=%s' % (
                OBJCOPY_PATH,
                FAP_LOCATION_AFTER_BUILD,
                sect.name,
                newSectName,
            )
            print("Renaming to %s from %s" % (newSectName, sect.name))
            os.system(cmd)


rc = os.system("%s -m ufbt" % sys.executable)
if rc != 0:
    sys.exit(rc)

clearSections()

os.system(
    '%s "%s" -p auto -s %s -t %s'
    % (sys.executable, RUNFAP_PATH, FAP_LOCATION_AFTER_BUILD, FAP_LOCATION_ON_FLIPPER)
)
