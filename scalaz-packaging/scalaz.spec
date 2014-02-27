%global scalaz_version 7.0.0
%global scala_short_version 2.10

# set this to 1 once scalacheck is available in Fedora (currently:
# yes) and scalaz's scalacheck support compiles (currently: no)

%global have_scalacheck 0

# set this to 1 once sbt is available in Fedora
%global have_native_sbt 1

Name:		scalaz
Version:	%{scalaz_version}
Release:	2%{?dist}
Summary:	extension to the core Scala library for functional programming

License:	BSD
URL:		http://typelevel.org
Source0:	https://github.com/scalaz/scalaz/archive/v%{scalaz_version}.tar.gz#/%{name}-v%{version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

Patch0:		scalaz-7.0.0-build.patch

BuildArch:	noarch

BuildRequires:	mvn(org.scalacheck:scalacheck_%{scala_short_version})
BuildRequires:	scala
%if %{have_native_sbt}
BuildRequires:	sbt
%endif

BuildRequires:	javapackages-tools
Requires:	javapackages-tools

Requires:       scala
Requires:	jansi

%description

Scalaz is a Scala library for functional programming.  It provides
purely functional data structures to complement those from the Scala
standard library. It defines a set of foundational type classes
(e.g. Functor, Monad) and corresponding instances for a large number
of data structures.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q
%patch0 -p1

%if %{have_native_sbt}
rm ./sbt
%endif

cp %{SOURCE1} .
chmod 755 climbing-nemesis.py

sed -i -e 's/1[.]10[.]0/1.11.0/g' project/build.scala

%if 0%{have_scalacheck} == 0
sed -i -e 's/scalacheckBinding, tests,//g' project/build.scala
%else
sed -i -e 's/ tests,//g' project/build.scala
./climbing-nemesis.py org.scalacheck scalacheck_%{scala_short_version} ivy-local
%endif

# the scalaz source directory does not include the BSD 2-clause license text
cat <<EOF > LICENSE
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

EOF

%build

%if %{have_native_sbt}
cp -r /usr/share/sbt/ivy-local .
mkdir boot

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local

sbt package makePom doc
%else
./sbt package makePom doc
%endif

%install
mkdir -p %{buildroot}/%{_javadir}/%{name}/
mkdir -p %{buildroot}/%{_mavenpomdir}
mkdir -p %{buildroot}/%{_javadocdir}/%{name}

for jar in $(find . -wholename \*/scala-%{scala_short_version}/%{name}-\*.jar); do 
    echo $jar
    shortname=$(echo $jar | sed -e 's/^.*[/]\([a-z-]\+\)_%{scala_short_version}-%{scalaz_version}.jar$/\1/g')
    cp -p $jar %{buildroot}/%{_javadir}/scalaz/${shortname}.jar
done

for apidir in $(find . -name api -type d | grep -v ivy-local); do
    module=$(echo $apidir | cut -f2 -d/)
    mkdir %{buildroot}/%{_javadocdir}/%{name}/$module
    cp -rp $apidir/* %{buildroot}/%{_javadocdir}/%{name}/$module
done

for pom in $(find . -name %{name}-\*.pom ) ; do 
    shortname=$(echo $pom | sed -e 's/^.*[/]\([a-z-]\+\)_%{scala_short_version}-%{scalaz_version}.pom$/\1/g')
    echo installing POM $pom to %{_mavenpomdir}/JPP.%{name}-${shortname}.pom
    cp -p $pom %{buildroot}/%{_mavenpomdir}/JPP.%{name}-${shortname}.pom
    echo %{_mavenpomdir}/JPP.%{name}-${shortname}.pom >> .rpm_pomfiles
    shortnames=( "${shortnames[@]}" $shortname )
done

echo shortnames are ${shortnames[@]}

for sub in ${shortnames[@]} ; do
    echo running add_maven_depmap JPP.%{name}-${sub}.pom %{name}/${sub}.jar
    %add_maven_depmap JPP.%{name}-${sub}.pom %{name}/${sub}.jar
done

%files -f .mfiles
%dir %{_javadir}/%{name}/
%doc README.md LICENSE

%files javadoc
%{_javadocdir}/%{name}/
%doc LICENSE

%changelog
* Wed Feb 26 2014 William Benton <willb@redhat.com> - 7.0.0-2
- updated paths for released sbt
- install POM files now
- generate javadocs

* Tue Nov 26 2013 William Benton <willb@redhat.com> - 7.0.0-1
- initial package
