Name:           scala
Version:        2.7.2
%define fullversion %{version}.RC6
Release:        0.3.RC6%{?dist}
Summary:        A hybrid functional/object-oriented language for the JVM
BuildArch:      noarch
Group:          Development/Languages
# License was confirmed to be standard BSD by fedora-legal
# https://www.redhat.com/archives/fedora-legal-list/2007-December/msg00012.html
License:        BSD
URL:            http://www.scala-lang.org/

# Source
Source0:        http://www.scala-lang.org/downloads/distrib/files/scala-%{fullversion}-sources.tgz

%define msilversion %{fullversion}
# Exported from upstream vcs
#   svn export http://lampsvn.epfl.ch/svn-repos/scala/msil/tags/R_2_7_2_RC6 msil-2.7.2.RC6
#   tar cjf msil-2.7.2.RC6.tar.bz2 msil-2.7.2.RC6
Source1:      msil-%{msilversion}.tar.bz2

%define fjbgversion r15432
# Exported from upstream vcs
# No tag for RC6
#   svn export -r 15432 http://lampsvn.epfl.ch/svn-repos/scala/fjbg/trunk fjbg-r15432
#   tar cjf fjbg-r15432.tar.bz2 fjbg-r15432
Source2:        fjbg-%{fjbgversion}.tar.bz2

# Scripts
Source10:       scala.in
Source11:       scalac.in
Source12:       scaladoc.in
Source13:       fsc.in

Source21:       scala.keys
Source22:       scala.mime
Source23:       scala-mime-info.xml
Source24:       scala.ant.d

Patch0:         scala-buildfile.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{fedora} == 8
%define java_sdk icedtea
%else
%define java_sdk openjdk
%endif

# Force build with openjdk/icedtea because gij is horribly slow and I haven't
# been successful at integrating aot compilation with the build process
BuildRequires:  java-devel-%{java_sdk}
BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  ant-nodeps
BuildRequires:  jline
BuildRequires:  jpackage-utils, java-devel
Requires:       java
Requires:       jline
Requires:       jpackage-utils

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

%define scaladir %{_datadir}/scala

%prep
%setup -q -a 1 -a 2 -n scala-%{fullversion}-sources
%patch0 -b .build
# remove all jar files except scala-library and scala-compiler needed
# for bootstrap
find . -not \( -name 'scala-library.jar' -or -name 'scala-compiler.jar' \) -and -name '*.jar' | xargs rm -f
find . -name '*.dll' -or -name '*.so' -or -name '*.exe' | xargs rm -f
ln -s `find-jar ant-contrib` lib/ant/ant-contrib.jar

%build
# Scala is written in itself and therefore requires boot-strapping from an
# initial binary build. The dist target of the ant build is a staged build
# that makes sure that the package bootstraps properly. The bundled binary
# compiler is used to compile the source code. That binary is used to 
# compile the source code again. That binary is used to compile the code
# again and the output is checked that it is exactly the same.  This makes
# sure that the build is repeatable and that the bootstrap compiler could
# be replaced with this one and successfully build the whole distribution
# again

# Force build with openjdk/icedtea because gij is horribly slow and I haven't
# been successful at integrating aot compilation with the build process
%define java_home %{_jvmdir}/java-%{java_sdk}

%define scala_ant %ant -Dsvn.out="" -Dant.jar="`find-jar ant`" -Dant-contrib.jar="`find-jar ant-contrib`" -Djline.jar="`find-jar jline`" -Dversion.number="%{fullversion}"

# Build FJBG
export ANT_OPTS=-Xmx1024M
(cd fjbg-%{fjbgversion}; %ant -Djar-file=fjbg.jar jar) || exit 1
cp fjbg-%{fjbgversion}/fjbg.jar lib/fjbg.jar

# Build msil with bootstrap compiler
(cd msil-%{msilversion}; make SCALAC="java -Xbootclasspath/a:../lib/scala-library.jar -cp ../lib/scala-library.jar:../lib/scala-compiler.jar:../lib/fjbg.jar scala.tools.nsc.Main" jar) || exit 1
cp msil-%{msilversion}/lib/msil.jar lib/msil.jar

# Build scala binaries
%scala_ant pack.comp || exit 1

# Rebuild msil with freshly compiled scala
(cd msil-%{msilversion}; make SCALAC="java -Xbootclasspath/a:../build/pack/lib/scala-library.jar -cp ../build/pack/lib/scala-library.jar:../build/pack/lib/scala-compiler.jar scala.tools.nsc.Main" clean jar) || exit 1
cp msil-%{msilversion}/lib/msil.jar lib/msil.jar

# Rebuild scala with freshly compiled msil
%scala_ant clean fastdist || exit 1

for script in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13}; do
        sed -e 's,@@JAVADIR@@,%{_javadir},g' -e 's,@@DATADIR@@,%{_datadir},g' $script > dists/scala-%{fullversion}/bin/`basename $script .in`
done

%install
rm -rf $RPM_BUILD_ROOT

function relativepath {
  UPDIRS=""
  PATHA="$1"
  PATHB="$2"
  while [ "$PATHA" == "${PATHA#$PATHB}" ] ; do
    UPDIRS="../$UPDIRS"
    PATHB="`dirname "$PATHB"`"
  done
  echo $UPDIRS${PATHA#$PATHB/}
}

install -d $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_bindir}
for prog in scaladoc fsc scala scalac; do
        install -p -m 755 dists/scala-%{fullversion}/bin/$prog $RPM_BUILD_ROOT%{_bindir}
        install -p -m 644 dists/scala-%{fullversion}/man/man1/$prog.1 $RPM_BUILD_ROOT%{_mandir}/man1
done

install -p -m 755 -d $RPM_BUILD_ROOT%{_javadir}/scala
install -p -m 755 -d $RPM_BUILD_ROOT%{scaladir}/lib
for libname in library compiler dbc partest swing; do
        install -m 644 dists/scala-%{fullversion}/lib/scala-$libname.jar $RPM_BUILD_ROOT%{_javadir}/scala/scala-$libname-%{fullversion}.jar
        ln -s scala-$libname-%{fullversion}.jar $RPM_BUILD_ROOT%{_javadir}/scala/scala-$libname.jar
        ln -s `relativepath %{_javadir}/scala/scala-$libname.jar %{scaladir}/lib` $RPM_BUILD_ROOT%{scaladir}/lib
done

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
install -p -m 644 %{SOURCE24} $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/scala

cp -pr dists/scala-%{fullversion}/doc/scala-devel-docs/examples $RPM_BUILD_ROOT%{_datadir}/scala/

install -d $RPM_BUILD_ROOT%{_datadir}/mime-info
install -p -m 644 %{SOURCE21} %{SOURCE22} $RPM_BUILD_ROOT%{_datadir}/mime-info/

install -d $RPM_BUILD_ROOT%{_datadir}/mime/packages/
install -p -m 644 %{SOURCE23} $RPM_BUILD_ROOT%{_datadir}/mime/packages/

%post
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_javadir}/scala
%dir %{_datadir}/scala
%{_datadir}/scala/lib
%{_mandir}/man1/*
%doc dists/scala-%{fullversion}/doc/scala-devel-docs/LICENSE
%doc dists/scala-%{fullversion}/doc/scala-devel-docs/README
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*

%files -n ant-scala
%defattr(-,root,root,-)
# Following is plain config because the ant task classpath could change from
# release to release
%config %{_sysconfdir}/ant.d/*

%files apidoc
%defattr(-,root,root,-)
%doc dists/scala-%{fullversion}/doc/scala-devel-docs/api
%doc dists/scala-%{fullversion}/doc/scala-devel-docs/LICENSE

%files examples
%defattr(-,root,root,-)
%{_datadir}/scala/examples

%changelog
* Mon Nov 03 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.3.RC6
- bump release to fix upgrade path

* Thu Nov 01 2008 Geoff Reedy <geoff@programmer-monk.net> - 2.7.2-0.1.RC6
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
