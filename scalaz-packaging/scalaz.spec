%global scalaz_version 7.0.0
%global scala_short_version 2.10

# set this to 1 once scalacheck is available in Fedora
%global have_scalacheck 0

# set this to 1 once sbt is available in Fedora
%global have_native_sbt 0

Name:           scalaz
Version:        %{scalaz_version}
Release:        1%{?dist}
Summary:        extension to the core Scala library for functional programming

License:        BSD
URL:            http://typelevel.org
# TODO:  get a POM for scalaz or package sbt-release to generate one
Source0:        https://github.com/scalaz/scalaz/archive/v%{scalaz_version}.tar.gz#/%{name}-v%{version}.tar.gz

Patch0:		scalaz-7.0.0-build.patch

BuildArch:	noarch

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

%build

%if %{have_native_sbt}
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
