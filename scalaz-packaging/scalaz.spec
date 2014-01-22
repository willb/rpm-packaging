%global scalaz_version 7.0.0
%global scala_short_version 2.10

# set this to 1 once scalacheck is available in Fedora
%global have_scalacheck 1

# set this to 1 once sbt is available in Fedora
%global have_native_sbt 1

Name:           scalaz
Version:        %{scalaz_version}
Release:        1%{?dist}
Summary:        extension to the core Scala library for functional programming

License:        BSD
URL:            http://typelevel.org
# TODO:  get a POM for scalaz or package sbt-release to generate one
Source0:        https://github.com/scalaz/scalaz/archive/v%{scalaz_version}.tar.gz#/%{name}-v%{version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py
Patch0:		scalaz-7.0.0-build.patch

BuildArch:	noarch

BuildRequires:	mvn(org.scalacheck:scalacheck_%{scala_short_version})
BuildRequires:  scala
%if %{have_native_sbt}
BuildRequires:  sbt
%endif

Requires:       scala
Requires:	jansi

%description

Scalaz is a Scala library for functional programming.  It provides
purely functional data structures to complement those from the Scala
standard library. It defines a set of foundational type classes
(e.g. Functor, Monad) and corresponding instances for a large number
of data structures.

%prep
%setup -q
%patch0 -p1

cp %{SOURCE1} .
chmod 755 climbing-nemesis.py

sed -i -e 's/1[.]10[.]0/1.11.0/g' project/build.scala

%if 0%{have_scalacheck} == 0
sed -i -e 's/scalacheckBinding, tests,//g' project/build.scala
%else
sed -i -e 's/ tests,//g' project/build.scala
./climbing-nemesis.py org.scalacheck scalacheck_%{scala_short_version} ivy-local
%endif

%build

%if %{have_native_sbt}
cp -r /usr/share/java/sbt/ivy-local .
mkdir boot

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local

sbt package
%else
./sbt package
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_javadir}/scalaz/

find . -wholename \*/scala-%{scala_short_version}/\*.jar -exec cp '{}' %{buildroot}/%{_javadir}/scalaz/ \;

%files
%{_javadir}/scalaz/
%doc



%changelog
* Tue Nov 26 2013 William Benton <willb@redhat.com> - 7.0.0-1
- initial package
