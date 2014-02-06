#!/bin/sh

export SBT_BOOT_DIR=${SBT_BOOT_DIR:-/usr/share/sbt/boot}
export SBT_IVY_DIR=${SBT_IVY_DIR:-/usr/share/sbt/ivy-local}
export SBT_BOOT_PROPERTIES=${SBT_BOOT_PROPERTIES:-/etc/sbt/sbt.boot.properties}
export BASE_CLASSPATH=$(build-classpath scala ivy sbt jline2 jansi test-interface sbinary)
export JAVA_OPTS="-Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled"

java -Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled -Dfedora.sbt.boot.dir=${SBT_BOOT_DIR} -Dfedora.sbt.ivy.dir=${SBT_IVY_DIR} -Dsbt.boot.properties=${SBT_BOOT_PROPERTIES} -cp ${BASE_CLASSPATH} xsbt.boot.Boot "$@"
