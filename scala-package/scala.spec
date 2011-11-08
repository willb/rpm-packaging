%global fullversion %{version}.final

Name:           scala
Version:        2.9.1
Release:        1%{?dist}
Summary:        A hybrid functional/object-oriented language for the JVM
BuildArch:      noarch
Group:          Development/Languages
# License was confirmed to be standard BSD by fedora-legal
# https://www.redhat.com/archives/fedora-legal-list/2007-December/msg00012.html
License:        BSD
URL:            http://www.scala-lang.org/

# Source
Source0:        http://www.scala-lang.org/downloads/distrib/files/scala-%{fullversion}-sources.tgz

# Change the default classpath (SCALA_HOME)
Patch1:		scala-2.9.1-tooltemplate.patch

# Use system jline2 instead of bundled jline2
Patch2:	        scala-2.9.1-use_system_jline.patch

Source21:       scala.keys
Source22:       scala.mime
Source23:       scala-mime-info.xml
Source24:       scala.ant.d

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global jline2_jar /usr/share/java/jline2.jar
%global jansi_jar /usr/share/java/jansi.jar

# Force build with openjdk/icedtea because gij is horribly slow and I haven't
# been successful at integrating aot compilation with the build process
BuildRequires:  java-devel-openjdk >= 1:1.6.0
BuildRequires:  ant
BuildRequires:  ant-contrib
BuildRequires:  ant-nodeps
BuildRequires:  jline2
BuildRequires:  jpackage-utils
BuildRequires:  shtool
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

%define scaladir %{_datadir}/scala

%prep
%setup -q -n scala-%{fullversion}-sources
%patch1 -p1 -b .tool
%patch2 -p1 -b .sysjline

pushd src
rm -rf jline
popd

%build

export ANT_OPTS="-Xms1024m -Xmx1024m"
%ant build docs

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
for prog in scaladoc fsc scala scalac scalap; do
        install -p -m 755 build/pack/bin/$prog $RPM_BUILD_ROOT%{_bindir}
done

install -p -m 755 -d $RPM_BUILD_ROOT%{_javadir}/scala
install -p -m 755 -d $RPM_BUILD_ROOT%{scaladir}/lib
for libname in scala-compiler scala-dbc scala-library scala-partest scala-swing scalap ; do
        install -m 644 build/pack/lib/$libname.jar $RPM_BUILD_ROOT%{_javadir}/scala/$libname-%{fullversion}.jar
        ln -s $libname-%{fullversion}.jar $RPM_BUILD_ROOT%{_javadir}/scala/$libname.jar
        shtool mkln -s $RPM_BUILD_ROOT%{_javadir}/scala/$libname.jar $RPM_BUILD_ROOT%{scaladir}/lib
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_javadir}/scala
%dir %{_datadir}/scala
%{_datadir}/scala/lib
%doc docs/LICENSE
%doc README
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/*
%{_mandir}/man1/*

%files -n ant-scala
%defattr(-,root,root,-)
# Following is plain config because the ant task classpath could change from
# release to release
%config %{_sysconfdir}/ant.d/*

%files apidoc
%defattr(-,root,root,-)
%doc build/scaladoc/library/*
%doc docs/LICENSE

%files examples
%defattr(-,root,root,-)
%{_datadir}/scala/examples

%changelog
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
