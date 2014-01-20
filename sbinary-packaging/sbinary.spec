%global sbinary_version 0.4.2
%global scala_version 2.10

Name:           sbinary
Version:        %{sbinary_version}
Release:        1%{?dist}
Summary:        Library for describing binary formats for Scala types

License:        MIT
URL:            https://github.com/harrah/sbinary
Source0:        https://github.com/harrah/sbinary/archive/v%{sbinary_version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:  scala
BuildRequires:	python
BuildRequires:	mvn(net.sourceforge.fmpp:fmpp)
BuildRequires:	mvn(org.beanshell:bsh)
BuildRequires:	mvn(xml-resolver:xml-resolver)
BuildRequires:	mvn(org.freemarker:freemarker)
BuildRequires:	maven-local
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:       scala

%description

SBinary is a library for describing binary protocols, in the form of
mappings between Scala types and binary formats. It can be used as a
robust serialization mechanism for Scala objects or a way of dealing
with existing binary formats found in the wild.

It started out life as a loose port of Haskell's Data.Binary. It's
since evolved a bit from there to take advantage of the features Scala
implicits offer over Haskell type classes, but the core idea has
remained the same.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
BuildArch:	noarch

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

sed -i -e 's/2[.]10[.]2/2.10.3/g' project/SBinaryProject.scala
# sed -i -e 's/if[(]incl[)]/if(false)/g' project/SBinaryProject.scala

sed -i -e 's|"scalacheck" % "1[.]10[.]0"|"scalacheck" % "1.11.0"|g' project/SBinaryProject.scala
# sed -i -e 's|% fmppConfig.name|% fmppConfig.name from "file:///usr/share/java/fmpp.jar"|g' project/SBinaryProject.scala
sed -i -e 's|[.]identity||g' project/SBinaryProject.scala
sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties || echo sbt.version=0.13.1 > project/build.properties

cp -r /usr/share/java/sbt/ivy-local .
mkdir boot

cp %{SOURCE1} .

chmod 755 climbing-nemesis.py

./climbing-nemesis.py --jarfile /usr/share/java/scalacheck.jar org.scalacheck scalacheck ivy-local --version 1.11.0 --scala %{scala_version}

./climbing-nemesis.py net.sourceforge.fmpp fmpp ivy-local
./climbing-nemesis.py org.freemarker freemarker ivy-local
./climbing-nemesis.py org.beanshell bsh ivy-local --override org.beanshell:bsh
./climbing-nemesis.py xml-resolver xml-resolver ivy-local


%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

cp core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
cp core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp core/target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README

%files javadoc
%{_javadocdir}/%{name}


%changelog

* Tue Jan 7 2014 William Benton <willb@redhat.com> - 0.4.2-1
- initial package
