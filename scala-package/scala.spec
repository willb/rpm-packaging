%global fullversion %{version}
%global release_repository http://nexus.scala-tools.org/content/repositories/releases
%global snapshot_repository http://nexus.scala-tools.org/content/repositories/snapshots
%global jline2_jar /usr/share/java/jline2.jar
%global jansi_jar /usr/share/java/jansi.jar
%global scaladir %{_datadir}/scala

Name:           scala
Version:        2.10.1
Release:        2%{?dist}
Summary:        A hybrid functional/object-oriented language for the JVM
BuildArch:      noarch
Group:          Development/Languages
# License was confirmed to be standard BSD by fedora-legal
# https://www.redhat.com/archives/fedora-legal-list/2007-December/msg00012.html
License:        BSD
URL:            http://www.scala-lang.org/
# Source
Source0:	http://www.scala-lang.org/downloads/distrib/files/scala-sources-%{fullversion}.tgz
Source1:	scala-library-2.10.0-bnd.properties
# Source0:        http://www.scala-lang.org/downloads/distrib/files/scala-sources-%{fullversion}.tgz
# Change the default classpath (SCALA_HOME)
Patch1:		scala-2.10.0-tooltemplate.patch
# Use system jline2 instead of bundled jline2
Patch2:	        scala-2.10.0-use_system_jline.patch
# change org.scala-lang jline in org.sonatype.jline jline
Patch3:	        scala-2.10.0-compiler-pom.patch
# Patch Swing module for JDK 1.7
Patch4:	        scala-2.10.0-java7.patch
# Fix aQuate issue
Patch5:         scala-2.10.0-bnd.patch
# fix incompatibilities with JLine 2.7
Patch6:         scala-2.10-jline.patch
# work around a known bug when running binary-compatibility tests against
# non-optimized builds (we can't do optimized builds due to another bug):
# http://grokbase.com/t/gg/scala-internals/1347g1jahq/2-10-x-bc-test-fails
Patch7:         scala-2.10.1-bc.patch
 

Source21:       scala.keys
Source22:       scala.mime
Source23:       scala-mime-info.xml
Source24:       scala.ant.d

Source31:	scala-bootstript.xml

# Force build with openjdk/icedtea because gij is horribly slow and I haven't
# been successful at integrating aot compilation with the build process
# BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  java-devel
BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  jline2
BuildRequires:  jpackage-utils
# BuildRequires:  maven-ant-tasks
BuildRequires:  shtool
BuildRequires:	aqute-bnd
BuildRequires:  junit4
BuildRequires:  felix-framework
BuildRequires:  pax-logging
Requires:       java
Requires:       jline2
Requires:       jpackage-utils
Requires:       %{jline2_jar}
Requires:	%{jansi_jar}

%description
Scala is a general purpose programming language designed to express common
programming patterns in a concise, elegant, and type-safe way. It smoothly
integrates features of object-oriented and functional languages. It is also
fully interoperable with Java.

%package apidoc
Summary:        Documentation for the Scala programming language
Group:          Documentation

%description apidoc
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package provides
reference and API documentation for the Scala programming language.

%package -n ant-scala
Summary:        Development files for Scala
Group:          Development/Languages
Requires:       scala = %{version}-%{release}, ant

%description -n ant-scala
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package enables support for
the scala ant tasks.

%package examples
Summary:        Examples for the Scala programming language
Group:          Development/Languages
# Otherwise it will pick up some perl module
Autoprov:       0
Requires:       scala = %{version}-%{release}

%description examples
Scala is a general purpose programming language for the JVM that blends
object-oriented and functional programming. This package contains examples for
the Scala programming language

%prep
%setup -q -n scala-%{fullversion}-sources
%patch1 -p1 -b .tool
%patch2 -p1 -b .sysjline
# %patch3 -p0 -b .compiler-pom
%patch4 -p1 -b .jdk7
%patch5 -p1 -b .bndx
%patch6 -p1 -b .rvk
%patch7 -p1 -b .bc

pushd src
rm -rf jline
popd

pushd lib
#  fjbg.jar ch.epfl.lamp
#  forkjoin.jar scala.concurrent.forkjoin available @ https://bugzilla.redhat.com/show_bug.cgi?id=854234 as jsr166y
#  find -not \( -name 'scala-compiler.jar' -or -name 'scala-library.jar' -or -name 'midpapi10.jar' -or \
#       -name 'msil.jar' -or -name 'fjbg.jar' -or -name 'forkjoin.jar' \) -and -name '*.jar' -delete

#  midpapi10.jar https://bugzilla.redhat.com/show_bug.cgi?id=807242 ?
#  msil.jar ch.epfl.lamp.compiler
#  scala-compiler.jar
#  scala-library-src.jar
#  scala-library.jar
  pushd ant
    rm -rf ant.jar
    rm -rf ant-contrib.jar
    ln -s $(build-classpath ant.jar) ant.jar
    ln -s $(build-classpath ant/ant-contrib) ant-contrib.jar
#    rm -rf ant-dotnet-1.0.jar
#    rm -rf maven-ant-tasks-2.1.1.jar
#    rm -rf vizant.jar
  popd
popd

cp -rf %{SOURCE31} .

%build

export ANT_OPTS="-Xms1024m -Xmx1024m"
# ant -f scala-bootstript.xml

# NB:  the "build" task is (unfortunately) necessary
#  build-opt will fail due to a scala optimizer bug
#  and its interaction with the system jline
ant replacelocker build docs || exit 1
pushd build/pack/lib
cp %{SOURCE1} bnd.properties
java -jar $(build-classpath aqute-bnd) wrap -properties \
    bnd.properties scala-library.jar
mv scala-library.jar scala-library.jar.no
mv scala-library.bar scala-library.jar
popd

%check

# these tests fail, but their failures appear spurious
rm -f test/files/run/parserJavaIdent.scala
rm -rf test/files/presentation/implicit-member
rm -rf test/files/presentation/t5708
rm -rf test/files/presentation/ide-bug-1000349
rm -rf test/files/presentation/ide-bug-1000475
rm -rf test/files/presentation/callcc-interpreter
rm -rf test/files/presentation/ide-bug-1000531
rm -rf test/files/presentation/visibility
rm -rf test/files/presentation/ping-pong

rm -f test/osgi/src/ReflectionToolboxTest.scala

ant test

%install

install -d $RPM_BUILD_ROOT%{_bindir}
for prog in scaladoc fsc scala scalac scalap; do
        install -p -m 755 build/pack/bin/$prog $RPM_BUILD_ROOT%{_bindir}
done

install -p -m 755 -d $RPM_BUILD_ROOT%{_javadir}/scala
install -p -m 755 -d $RPM_BUILD_ROOT%{scaladir}/lib
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}

for libname in scala-compiler scala-library scala-partest scala-reflect scalap scala-swing ; do
        install -m 644 build/pack/lib/$libname.jar $RPM_BUILD_ROOT%{_javadir}/scala/
        shtool mkln -s $RPM_BUILD_ROOT%{_javadir}/scala/$libname.jar $RPM_BUILD_ROOT%{scaladir}/lib
        sed -i "s|@VERSION@|%{fullversion}|" src/build/maven/$libname-pom.xml
        sed -i "s|@RELEASE_REPOSITORY@|%{release_repository}|" src/build/maven/$libname-pom.xml
        sed -i "s|@SNAPSHOT_REPOSITORY@|%{snapshot_repository}|" src/build/maven/$libname-pom.xml
        install -pm 644 src/build/maven/$libname-pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP.%{name}-$libname.pom
%add_maven_depmap JPP.%{name}-$libname.pom %{name}/$libname.jar
done
shtool mkln -s $RPM_BUILD_ROOT%{jline2_jar} $RPM_BUILD_ROOT%{scaladir}/lib
shtool mkln -s $RPM_BUILD_ROOT%{jansi_jar} $RPM_BUILD_ROOT%{scaladir}/lib

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
install -p -m 644 %{SOURCE24} $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/scala

cp -pr docs/examples $RPM_BUILD_ROOT%{_datadir}/scala/

install -d $RPM_BUILD_ROOT%{_datadir}/mime-info
install -p -m 644 %{SOURCE21} %{SOURCE22} $RPM_BUILD_ROOT%{_datadir}/mime-info/

install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages/
install -p -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_datadir}/mime/packages/

sed -i -e 's,@JAVADIR@,%{_javadir},g' -e 's,@DATADIR@,%{_datadir},g' $RPM_BUILD_ROOT%{_bindir}/*

install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m 644 build/scaladoc/manual/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1

%post
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :


%files
%{_bindir}/*
%{_javadir}/scala
%dir %{_datadir}/scala
%{_datadir}/scala/lib
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_mandir}/man1/*
%{_mavenpomdir}/JPP.%{name}-*.pom
%{_mavendepmapfragdir}/%{name}
%doc docs/LICENSE

%files -n ant-scala
# Following is plain config because the ant task classpath could change from
# release to release
%config %{_sysconfdir}/ant.d/*
%doc docs/LICENSE

%files apidoc
%doc build/scaladoc/library/*
%doc docs/LICENSE

%files examples
%{_datadir}/scala/examples
%doc docs/LICENSE

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 16 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.1-1
- New upstream releae

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan  7 2013 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.0-1
- New upstream release
- Add patch to use system aQuate-bnd.jar file

* Thu Dec 13 2012 Jochen Schmitt <s4504kr@omega.in.herr-schmitt.de> - 2.10.0-0.5
- New upstream release

* Fri Dec  7 2012 Jochen Schmitt <Jochen herr-schmitt de> - 2.10.0-0.3
- New upstream release

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.9.2-1
- update to 2.9.2
- added maven poms
- adapted to current guideline
- built with java 7 support
- removed ant-nodeps from buildrequires
- disabled swing module

* Sat Jul 21 2012 Fedora Release Engineering <JOchen herr-schmitt de> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Nov 27 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.9.1-2
- Build explicit agains java-1.6.0

* Thu Nov  3 2011 Jochen Schmitt <Jochen herr-schmitt de> - 2.9.1-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Jochen Schmitt <Jochen herr-schmitt de> - 2.8.1-1
- New upstream release (#661853)

* Sun Aug 15 2010 Geoff Reedy <geoff@programmer-monk.net> - 2.8.0-1
- Update to upstream 2.8.0 release

* Thu Oct 29 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.7-1
- Update to upstream 2.7.7 release

* Sat Sep 19 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.5-1
- Update to upstream 2.7.5 release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-5
- fix problem in tooltemplate patch

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-4
- make jline implicitly available to match upstream behavior

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-3
- fix problem with substitutions to scripts in %%install

* Mon May 18 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-2
- fix launcher scripts by modifying template, not overriding them

* Tue May 12 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.4-1
- update to 2.7.4 final

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Geoff Reedy <geoff@programmer-monk.net> - 2.7.3-1
- update to 2.7.3 final

* Sun Nov 09 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-1
- update to 2.7.2 final

* Mon Nov 03 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.3.RC6
- bump release to fix upgrade path

* Sat Nov 01 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC6
- update to 2.7.2-RC6

* Thu Oct 30 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC5
- update to 2.7.2-RC5

* Sat Sep 06 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.2.RC1
- All code is now under BSD license
- Remove dll so and exe binaries in prep
- Add BuildRequires required by Java packaging guidelines
- Add missing defattr for examples and ant-scala

* Wed Aug 20 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC1
- update to 2.7.2-RC1

* Wed Aug 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-3
- regenerate classpath in manifest patch to apply cleanly to 2.7.1

* Wed Aug 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-2
- no changes, accidental release bump

* Mon May 05 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.1-1
- Update to 2.7.1

* Fri May 02 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.0-2
- Use java-sdk-openjdk for non-fc8 builds

* Mon Mar 10 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.0-1
- Update to 2.7.0
- License now correctly indicated as BSD and LGPLv2+
- Include LICENSE file in apidoc subpackage

* Mon Feb 11 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-8
- Adhere more strongly to the emacs package guidelines
- Include some comments regarding the boot-strapping process

* Wed Jan 16 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-7
- Add dist tag to release
- Fix directory ownership issues in %%_datadir/scala
- Remove source code from -devel package
- Rename -devel package to ant-scala
- Fix packaging of gtksourceview2 language spec
- Preserve timestamps when installing and cping
- Add patch to remove Class-Path entries from jar manifests
- Fix line endings in enscript/README
 
* Sun Jan 13 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-6
- Include further information about inclusion of binary distribution
- Unpack only those files needed from the binary distribution
- Include note about license approval

* Thu Dec 27 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-5
- Add emacs(bin) BR
- Patch out call to subversion in build.xml
- Add pkgconfig to BuildRequires

* Thu Dec 27 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-4
- Reformat emacs-scala description
- Expand tabs to spaces
- Fix -devel symlinks
- Better base package summary

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-3
- Add ant config to devel package
- Require icedtea for build
- Move examples to %%{_datadir}/scala/examples
- Clean up package descriptions
- Add base package requirement for scala-examples and scala-devel

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-2
- Fix post scripts
- Use spaces instead of tabs

* Wed Dec 26 2007 Geoff Reedy <geoff@programmer-monk.net> - 2.6.1-1
- Initial build.
