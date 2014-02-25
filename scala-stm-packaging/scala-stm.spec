%global scala_short_version 2.10
Name:          scala-stm
Version:       0.7
Release:       2%{?dist}
Summary:       Software Transactional Memory for Scala
License:       BSD
URL:           http://nbronson.github.io/scala-stm/
Source0:       https://github.com/nbronson/scala-stm/archive/release-%{version}.tar.gz

BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: ant
BuildRequires: sbt

BuildRequires: mvn(org.scala-lang:scala-compiler)
BuildRequires: mvn(org.scala-lang:scala-library)
Requires:      mvn(org.scala-lang:scala-library)
Requires:      java
Requires:      javapackages-tools
BuildArch:     noarch

%description
ScalaSTM is a lightweight software transactional memory
for Scala, inspired by the STMs in Haskell and Clojure.

ScalaSTM provides a mutable cell called a Ref. If you
build a shared data structure using immutable objects and
Ref-s, then you can access it from multiple threads or
actors. No synchronized, no deadlocks or race conditions,
and good scalability. Included are concurrent sets and
maps, and we also have an easier and safer replacement
for wait and notifyAll.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-release-%{version}
# Cleanup
find -name '*.class' -print -delete
find -name '*.jar' -print -delete
# sb7_java-v1.2.tgz http://lpd.epfl.ch/gramoli/doc/sw/sb7_java-v1.2.tgz
rm -r lib/*

# get rid of sbt plugins
rm project/plugins.sbt

# patch build.sbt
sed -i -e '/% "test"/d' build.sbt
sed -i -e '/credentials/d' build.sbt
sed -i -e 's/\(scalaVersion :=\).*$/scalaVersion := "2.10.3"/' build.sbt

# delete tests due to missing deps
rm -rf src/test
rm -rf dep-tests

cp -r /usr/share/sbt/ivy-local .
mkdir boot

%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local

sbt package makePom deliverLocal doc


# No test deps available


%install

# target/scala-2.10/scala-stm_2.10-0.7.jar
mkdir -p %{buildroot}%{_javadir}
cp -p target/scala-%{scala_short_version}/%{name}_%{scala_short_version}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 target/scala-%{scala_short_version}/%{name}_%{scala_short_version}-%{version}.pom %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/scala-%{scala_short_version}/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt README RELEASE-NOTES.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Mon Feb 24 2014 William Benton <willb@redhat.com> - 0.7-2
- updated to use sbt for build

* Thu Feb 06 2014 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm
