#!/bin/sh
set -x

VER=$1
FNS=scala-$VER

rm -rf scala/
git clone git://github.com/scala/scala.git
cd scala
git checkout v$VER
./pull-binary-libs.sh
cd ..
rm -rf $FNS $FMS.tgz
mv scala $FNS
tar -zcf $FNS.tgz --exclude $FNS/.git $FNS/
rm -rf $FNS/
fedpkg new-sources $FNS
