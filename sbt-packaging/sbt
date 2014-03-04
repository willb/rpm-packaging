#!/bin/sh

if \[ $(rpm -q --queryformat '%{version}' fedora-release) -ge 21 \] ; then
export JLINE=jline
else
export JLINE=jline2
fi

export SBT_BOOT_DIR=${SBT_BOOT_DIR:-/usr/share/sbt/boot}
export SBT_IVY_DIR=${SBT_IVY_DIR:-/usr/share/sbt/ivy-local}

if \[ "x$RPM_PACKAGE_NAME" != x \] && \[ -f /etc/sbt/rpmbuild-sbt.boot.properties \] ; then
    export SBT_BOOT_PROPERTIES=${SBT_BOOT_PROPERTIES:-/etc/sbt/rpmbuild-sbt.boot.properties}
else
    export SBT_BOOT_PROPERTIES=${SBT_BOOT_PROPERTIES:-/etc/sbt/sbt.boot.properties}
fi

export BASE_CLASSPATH=$(build-classpath scala ivy sbt ${JLINE} jansi test-interface sbinary)
export JAVA_OPTS="-Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled"

java -Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled -Dfedora.sbt.boot.dir=${SBT_BOOT_DIR} -Dfedora.sbt.ivy.dir=${SBT_IVY_DIR} -Dsbt.boot.properties=${SBT_BOOT_PROPERTIES} -cp ${BASE_CLASSPATH} xsbt.boot.Boot "$@"
