%global namedreltag -RC2
%global namedversion %{version}%{?namedreltag}
%global scala_short_version 2.10
Name:          akka
Version:       2.3.0
Release:       0.2.RC2%{?dist}
Summary:       Scalable real-time transaction processing
License:       ASL 2.0
URL:           http://akka.io/
Source0:       https://github.com/akka/akka/archive/v%{namedversion}.tar.gz
# Default use sbt
Source1:       akka-build.xml
# Build only these sub-modules, cause: unavailable build deps 
Source2:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-actor_%{scala_short_version}/%{namedversion}/akka-actor_%{scala_short_version}-%{namedversion}.pom
Source3:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-slf4j_%{scala_short_version}/%{namedversion}/akka-slf4j_%{scala_short_version}-%{namedversion}.pom
Source4:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-remote_%{scala_short_version}/%{namedversion}/akka-remote_%{scala_short_version}-%{namedversion}.pom

BuildRequires: java-devel
BuildRequires: javapackages-tools

BuildRequires: ant
# typesafe-config
BuildRequires: mvn(com.typesafe:config)
BuildRequires: mvn(org.scala-lang:scala-compiler)
BuildRequires: mvn(org.scala-lang:scala-library)
BuildRequires: mvn(org.slf4j:slf4j-api)
# requires for akka-remote
BuildRequires: mvn(org.uncommons.maths:uncommons-maths)
BuildRequires: mvn(com.google.protobuf:protobuf-java)
BuildRequires: mvn(io.netty:netty)

Requires:      java
Requires:      javapackages-tools
BuildArch:     noarch

%description
Akka is a toolkit and run-time for building highly concurrent,
distributed, and fault tolerant event-driven applications on
the JVM.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n akka-%{namedversion}
# Cleanup
find -name '*.class' -print -delete
find -name '*.jar' -print -delete

cp -p %{SOURCE1} build.xml
sed -i "s|@VERSION@|%{namedversion}|" build.xml

# fix non ASCII chars
for s in %{name}-actor/src/main/java/akka/actor/AbstractScheduler.java;do
  native2ascii -encoding UTF8 ${s} ${s}
done

# spurious-executable-perm
chmod 644 LICENSE

%build

ant dist doc

%install

mkdir -p %{buildroot}%{_javadir}/%{name}
cp -p target/%{name}-remote.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-actor.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-slf4j.jar %{buildroot}%{_javadir}/%{name}/

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-actor.pom
%add_maven_depmap JPP.%{name}-%{name}-actor.pom %{name}/%{name}-actor.jar

install -pm 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-slf4j.pom
%add_maven_depmap JPP.%{name}-%{name}-slf4j.pom %{name}/%{name}-slf4j.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE4} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-remote.pom
%add_maven_depmap JPP.%{name}-%{name}-remote.pom %{name}/%{name}-remote.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp target/apidocs/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/%{name}
%doc CONTRIBUTING.md LICENSE README.textile

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog
* Tue Feb 25 2014 William Benton <willb@redhat.com> 2.3.0-0.2-RC2
- Added akka-remote support

* Tue Feb 04 2014 gil cattaneo <puntogil@libero.it> 2.3.0-0.1.RC2
- initial rpm
