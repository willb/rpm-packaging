%global namedreltag %nil
%global namedversion %{version}%{?namedreltag}
%global scala_short_version 2.10
Name:          akka
Version:       2.3.0
Release:       1%{?dist}
Summary:       Scalable real-time transaction processing
License:       ASL 2.0
URL:           http://akka.io/
Source0:       https://github.com/akka/akka/archive/v%{namedversion}.tar.gz
# Default use sbt
Source1:       https://raw.github.com/willb/rpm-packaging/85bb1497a483faef89749cd4704b04a23bf32e5d/akka-packaging/akka-build.xml
# Build only these sub-modules, cause: unavailable build deps
# TODO  akka-camel akka-contrib akka-durable-mailboxes akka-persistence akka-samples akka-zeromq
Source2:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-actor_%{scala_short_version}/%{namedversion}/akka-actor_%{scala_short_version}-%{namedversion}.pom
Source3:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-agent_%{scala_short_version}/%{namedversion}/akka-agent_%{scala_short_version}-%{namedversion}.pom
Source4:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-cluster_%{scala_short_version}/%{namedversion}/akka-cluster_%{scala_short_version}-%{namedversion}.pom
Source5:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-dataflow_%{scala_short_version}/%{namedversion}/akka-dataflow_%{scala_short_version}-%{namedversion}.pom
Source6:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-kernel_%{scala_short_version}/%{namedversion}/akka-kernel_%{scala_short_version}-%{namedversion}.pom
Source7:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-osgi_%{scala_short_version}/%{namedversion}/akka-osgi_%{scala_short_version}-%{namedversion}.pom
Source8:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-remote_%{scala_short_version}/%{namedversion}/akka-remote_%{scala_short_version}-%{namedversion}.pom
Source9:       http://repo1.maven.org/maven2/com/typesafe/akka/akka-slf4j_%{scala_short_version}/%{namedversion}/akka-slf4j_%{scala_short_version}-%{namedversion}.pom
Source10:      http://repo1.maven.org/maven2/com/typesafe/akka/akka-transactor_%{scala_short_version}/%{namedversion}/akka-transactor_%{scala_short_version}-%{namedversion}.pom

BuildRequires: java-devel
BuildRequires: javapackages-tools

BuildRequires: ant
BuildRequires: protobuf-compiler

BuildRequires: mvn(com.google.protobuf:protobuf-java)
# typesafe-config
BuildRequires: mvn(com.typesafe:config)
BuildRequires: mvn(org.scala-lang:scala-compiler)
BuildRequires: mvn(org.scala-lang:scala-library)
BuildRequires: mvn(org.scala-stm:scala-stm_2.10)
BuildRequires: mvn(org.eclipse.osgi:org.eclipse.osgi)
BuildRequires: mvn(org.slf4j:slf4j-api)
# requires for akka-remote
BuildRequires: mvn(org.uncommons.maths:uncommons-maths)

%if 0%{?fedora} >= 21
BuildRequires: mvn(io.netty:netty:3)
Requires:      mvn(io.netty:netty:3)
%else
BuildRequires: mvn(io.netty:netty)
Requires:      mvn(io.netty:netty)
%endif

Requires:      mvn(com.google.protobuf:protobuf-java)
Requires:      mvn(com.typesafe:config)
Requires:      mvn(org.scala-lang:scala-library)
Requires:      mvn(org.scala-stm:scala-stm_2.10)
Requires:      mvn(org.eclipse.osgi:org.eclipse.osgi)
Requires:      mvn(org.slf4j:slf4j-api)
Requires:      mvn(org.uncommons.maths:uncommons-maths)

Requires:      java-headless
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

# handle compatibility netty jar
%if 0%{?fedora} >= 21
sed -i -e 's|netty[.]jar|netty3-3.jar|' build.xml
cp -p %{SOURCE8} remote-pom.xml
%pom_xpath_set "pom:project/pom:dependencies/pom:dependency[pom:artifactId='netty']/pom:version" 3 remote-pom.xml
%endif

# use osgi 5.x apis
cp -p %{SOURCE7} osgi-pom.xml
%pom_remove_dep org.osgi: osgi-pom.xml
%pom_add_dep org.eclipse.osgi:org.eclipse.osgi osgi-pom.xml

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
cp -p target/%{name}-actor.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-agent.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-cluster.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-dataflow.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-kernel.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-osgi.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-remote.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-slf4j.jar %{buildroot}%{_javadir}/%{name}/
cp -p target/%{name}-transactor.jar %{buildroot}%{_javadir}/%{name}/

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE2} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-actor.pom
%add_maven_depmap JPP.%{name}-%{name}-actor.pom %{name}/%{name}-actor.jar

install -pm 644 %{SOURCE3} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-agent.pom
%add_maven_depmap JPP.%{name}-%{name}-agent.pom %{name}/%{name}-agent.jar

install -pm 644 %{SOURCE4} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-cluster.pom
%add_maven_depmap JPP.%{name}-%{name}-cluster.pom %{name}/%{name}-cluster.jar

install -pm 644 %{SOURCE5} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-dataflow.pom
%add_maven_depmap JPP.%{name}-%{name}-dataflow.pom %{name}/%{name}-dataflow.jar

install -pm 644 %{SOURCE6} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-kernel.pom
%add_maven_depmap JPP.%{name}-%{name}-kernel.pom %{name}/%{name}-kernel.jar

install -pm 644 osgi-pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-osgi.pom
%add_maven_depmap JPP.%{name}-%{name}-osgi.pom %{name}/%{name}-osgi.jar

%if 0%{?fedora} >= 21
install -pm 644 remote-pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-remote.pom
%else
install -pm 644 %{SOURCE8} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-remote.pom
%endif
%add_maven_depmap JPP.%{name}-%{name}-remote.pom %{name}/%{name}-remote.jar

install -pm 644 %{SOURCE9} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-slf4j.pom
%add_maven_depmap JPP.%{name}-%{name}-slf4j.pom %{name}/%{name}-slf4j.jar

install -pm 644 %{SOURCE10} %{buildroot}%{_mavenpomdir}/JPP.%{name}-%{name}-transactor.pom
%add_maven_depmap JPP.%{name}-%{name}-transactor.pom %{name}/%{name}-transactor.jar

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
* Wed Mar 05 2014 gil cattaneo <puntogil@libero.it> 2.3.0-1
- Update to 2.3.0

* Thu Feb 27 2014 gil cattaneo <puntogil@libero.it> 2.3.0-0.1.RC4
- Update to 2.3.0-RC4
- Added akka-{agent,cluster,dataflow,kernel,osgi,transactor} support

* Tue Feb 25 2014 William Benton <willb@redhat.com> 2.3.0-0.2-RC2
- Added akka-remote support

* Tue Feb 04 2014 gil cattaneo <puntogil@libero.it> 2.3.0-0.1.RC2
- initial rpm
