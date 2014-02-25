%global scala_short_version 2.10
Name:          scala-stm
Version:       0.7
Release:       1%{?dist}
Summary:       Software Transactional Memory for Scala
License:       BSD
URL:           http://nbronson.github.io/scala-stm/
Source0:       https://github.com/nbronson/scala-stm/archive/release-%{version}.tar.gz
# Default use sbt
Source1:       scala-stm-build.xml
Source2:       http://repo1.maven.org/maven2/org/scala-stm/scala-stm_%{scala_short_version}/%{version}/scala-stm_%{scala_short_version}-%{version}.pom

BuildRequires: java-devel
BuildRequires: javapackages-tools
BuildRequires: ant
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

cp -p %{SOURCE1} build.xml
sed -i "s|@VERSION@|%{version}|" build.xml

%build

# No test deps available
ant jar doc

%install

mkdir -p %{buildroot}%{_javadir}
cp -p target/%{name}.jar %{buildroot}%{_javadir}/

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/doc/main/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE.txt README RELEASE-NOTES.txt

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE.txt

%changelog
* Thu Feb 06 2014 gil cattaneo <puntogil@libero.it> 0.7-1
- initial rpm