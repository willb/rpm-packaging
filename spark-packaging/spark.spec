%global spark_version 0.9.0
%global spark_version_suffix -incubating
%global scala_version 2.10

%if 0%{?fedora} >= 20
%global want_hadoop 1
%else
%global want_hadoop 0
%endif

%global remap_version_to_installed() sed -i -e 's/"%{1}"[\t ]*%%[\t ]*"%{2}"[\t ]*%%[\t ]*"[^"]*"/"%{1}" %% "%{2}" %% "'$(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))'"/g' %{3}

%global climbing_nemesis() ./climbing-nemesis.py %{1} %{2} ivy-local --log debug --version $(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))

Name:		spark
Version:	%{spark_version}
Release:	0.2%{?dist}
Summary:	Lightning-fast cluster computing

License:	ASL 2.0
URL:		http://spark.apache.org
Source0:	https://github.com/apache/spark/archive/v%{spark_version}%{spark_version_suffix}.tar.gz
Source1:	https://raw.github.com/willb/spark-packaging/master/xmvn-sbt
Source2:	https://raw.github.com/willb/spark-packaging/master/xmvn-sbt.properties
Source3:	https://raw.github.com/willb/spark-packaging/master/default-build.sbt

Patch0:		spark-v0.9.0-0001-Replace-lift-json-with-json4s-jackson.patch
Patch1:		spark-v0.9.0-0002-use-sbt-0.13.1.patch
Patch2:		spark-v0.9.0-0003-Removed-sbt-plugins.patch
Patch3:		spark-v0.9.0-0004-removed-examples.patch
Patch4:		spark-v0.9.0-0005-Removed-code-depending-on-Kryo.patch
Patch5:		spark-v0.9.0-0006-Remove-functionality-depending-on-stream-lib.patch
Patch6:		spark-v0.9.0-0007-Removed-mesos.patch
Patch7:		spark-v0.9.0-0008-remove-unavailable-and-unnecessary-deps.patch
Patch8:		spark-v0.9.0-0009-use-Jetty-8.patch
Patch9:		spark-v0.9.0-0010-use-Akka-2.3.0-RC2.patch
Patch10:	spark-v0.9.0-0011-xmvn.patch

BuildArch:	noarch
BuildRequires:	sbt
BuildRequires:	scala
BuildRequires:	python
BuildRequires:	maven-local
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:	scala

BuildRequires:	jetty8
Requires:	jetty8

BuildRequires:	plexus-containers-component-annotations

BuildRequires:	mvn(org.json4s:json4s-jackson_%{scala_version})
Requires:	mvn(org.json4s:json4s-jackson_%{scala_version})

BuildRequires:	mvn(com.thoughtworks.paranamer:paranamer)
Requires:	mvn(com.thoughtworks.paranamer:paranamer)

BuildRequires:	mvn(com.codahale.metrics:metrics-core)
BuildRequires:	mvn(com.codahale.metrics:metrics-ganglia)
BuildRequires:	mvn(com.codahale.metrics:metrics-graphite)
BuildRequires:	mvn(com.codahale.metrics:metrics-json)
BuildRequires:	mvn(com.codahale.metrics:metrics-jvm)
BuildRequires:	mvn(com.google.code.findbugs:jsr305)
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(commons-daemon:commons-daemon)
BuildRequires:	mvn(com.ning:compress-lzf)
BuildRequires:	mvn(io.netty:netty-all)
BuildRequires:	mvn(it.unimi.dsi:fastutil)
BuildRequires:	mvn(log4j:log4j)
BuildRequires:	mvn(net.java.dev.jets3t:jets3t)
%if %{want_hadoop}
BuildRequires:	mvn(org.apache.hadoop:hadoop-client)
%endif
BuildRequires:	mvn(org.easymock:easymock)
BuildRequires:	mvn(org.eclipse.jetty:jetty-server)
BuildRequires:	mvn(org.eclipse.jetty.orbit:javax.servlet)
BuildRequires:	mvn(org.jblas:jblas)
BuildRequires:	mvn(org.ow2.asm:asm)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(org.slf4j:slf4j-log4j12)
BuildRequires:	mvn(com.typesafe.akka:akka-actor_%{scala_version})
BuildRequires:	mvn(com.typesafe.akka:akka-remote_%{scala_version})
BuildRequires:	mvn(org.xerial.snappy:snappy-java)
BuildRequires:	mvn(com.freevariable.lancer:lancer)

Requires:	mvn(com.codahale.metrics:metrics-core)
Requires:	mvn(com.codahale.metrics:metrics-ganglia)
Requires:	mvn(com.codahale.metrics:metrics-graphite)
Requires:	mvn(com.codahale.metrics:metrics-json)
Requires:	mvn(com.codahale.metrics:metrics-jvm)
Requires:	mvn(com.google.code.findbugs:jsr305)
Requires:	mvn(com.google.guava:guava)
Requires:	mvn(commons-daemon:commons-daemon)
Requires:	mvn(com.ning:compress-lzf)
Requires:	mvn(io.netty:netty-all)
Requires:	mvn(it.unimi.dsi:fastutil)
Requires:	mvn(log4j:log4j)
Requires:	mvn(net.java.dev.jets3t:jets3t)
%if %{want_hadoop}
Requires:	mvn(org.apache.hadoop:hadoop-client)
%endif
Requires:	mvn(org.apache.zookeeper:zookeeper)
Requires:	mvn(org.easymock:easymock)
Requires:	mvn(org.eclipse.jetty:jetty-server)
Requires:	mvn(org.eclipse.jetty.orbit:javax.servlet)
Requires:	mvn(org.jblas:jblas)
Requires:	mvn(org.ow2.asm:asm)
Requires:	mvn(org.slf4j:slf4j-api)
Requires:	mvn(org.slf4j:slf4j-log4j12)
Requires:	mvn(com.typesafe.akka:akka-actor_%{scala_version})
Requires:	mvn(com.typesafe.akka:akka-remote_%{scala_version})
Requires:	mvn(org.xerial.snappy:snappy-java)
Requires:	mvn(com.freevariable.lancer:lancer)

%description

Apache Spark is a fast and general engine for large-scale data processing.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{spark_version}%{spark_version_suffix}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

sed -i -e 's/\(val [A-Z]\+_JVM_VERSION =[^1]\+\)1.6"/\11.7"/' project/SparkBuild.scala

# replace Colt with Lancer
sed -i -e 's/"colt.*1[.]2[.]0"/"com.freevariable.lancer" % "lancer" % "0.0.1"/' project/SparkBuild.scala

for jetfile in $(find . -name \*.scala | xargs grep -l cern\\.jet) ; do
    sed -i -e 's|cern[.]jet[.]random[.]engine|com.freevariable.lancer.random|' $jetfile
    sed -i -e 's|cern[.]jet[.]random|com.freevariable.lancer.random|' $jetfile
    sed -i -e 's|cern[.]jet[.]stat|com.freevariable.lancer.stat|' $jetfile
done

# remove examples dependent upon Colt functionality not yet available in Lancer
rm ./examples/src/main/scala/org/apache/spark/examples/LocalALS.scala
rm ./examples/src/main/scala/org/apache/spark/examples/SparkALS.scala

# remove chill dependency (not available yet)
sed -i -e '/com.twitter.*chill/d' project/SparkBuild.scala

# remove stream-lib dependency (not available yet)
sed -i -e '/com.clearspring.*stream/d' project/SparkBuild.scala

# remove avro because it's only used for flume (which we don't build)
sed -i -e '/org.apache.*avro/d' project/SparkBuild.scala

# remove mesos dependency (java support not available yet)
sed -i -e '/org[.]apache.*mesos/d' project/SparkBuild.scala

# remove all test deps for now
sed -i -e '/%[[:space:]]*"test"/d' project/SparkBuild.scala

# fix up json4s-jackson version
sed -i -e 's|\(json4s-jackson"[^"]*"\)3[.]2[.]6|\13.2.7|' project/SparkBuild.scala

mkdir boot

# remove bundled sbt script
rm -rf sbt

cp %{SOURCE1} sbt-xmvn
chmod 755 sbt-xmvn

cp %{SOURCE2} xmvn-sbt.properties

cp %{SOURCE3} build.sbt
cp %{SOURCE3} project/build.sbt

%build

export XMVN_CLASSPATH=$(build-classpath aether/api guava ivy maven/maven-model plexus-classworlds plexus-containers/plexus-container-default plexus/utils xbean/xbean-reflect xmvn/xmvn-connector xmvn/xmvn-core atinject google-guice-no_aop)

export SPARK_HADOOP_VERSION=2.2.0
export DEFAULT_IS_NEW_HADOOP=true

export SBT_BOOT_DIR=boot

export SBT_BOOT_PROPERTIES=xmvn-sbt.properties

mkdir lib

for f in $(echo ${XMVN_CLASSPATH} | tr : \  ); do 
    cp $f lib
done

cp /usr/share/java/plexus/containers-component-annotations.jar lib

for sub in project tools bagel mllib streaming core graphx repl; do
 ln -s $(pwd)/lib $sub/lib
done

# HACK HACK HACK
(echo q | SBT_BOOT_PROPERTIES=/etc/sbt/sbt.boot.properties sbt quit) || true
cp lib/* boot/scala-2.10.3/lib/

alltargets() {for f in "$@" ; do echo $f/package $f/makePom $f/doc $f/publishLocal; done}

# ./sbt-xmvn core/package core/makePom core/doc core/publishLocal
./sbt-xmvn $(alltargets core mllib graphx bagel streaming repl tools)

%install
mkdir -p %{buildroot}/%{_javadir}/%{name}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}
for apidir in $(find . -name api -type d) ; do
  pushd $apidir
  cp -rp . %{buildroot}/%{_javadocdir}/%{name}
  popd
done

for jar in $(find . -name \*.jar | grep _%{scala_version}-%{spark_version}%{spark_version_suffix}.jar) ; do
  install -m 644 $jar %{buildroot}/%{_javadir}/%{name}/$(echo $jar | cut -f5 -d/ | cut -f1 -d_).jar
done

declare -a shortnames

for pom in $(find . -name \*.pom | grep _%{scala_version}-%{spark_version}%{spark_version_suffix}.pom ) ; do 
  shortname=$(echo $pom | cut -f5 -d/ | cut -f1 -d_)
  echo installing POM $pom to %{_mavenpomdir}/JPP.%{name}-${shortname}.pom
  install -pm 644 $pom %{buildroot}/%{_mavenpomdir}/JPP.%{name}-${shortname}.pom
  echo %{_mavenpomdir}/JPP.%{name}-${shortname}.pom >> .rpm_pomfiles
  shortnames=( "${shortnames[@]}" $shortname )
done

for sub in ${shortnames[@]} ; do
  echo running add_maven_depmap JPP.%{name}-${sub}.pom %{name}/${sub}.jar
  %add_maven_depmap JPP.%{name}-${sub}.pom %{name}/${sub}.jar
done

%files -f .mfiles
%dir %{_javadir}/%{name}

%doc LICENSE README.md

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE


%changelog

* Sat Mar 1 2014 William Benton <willb@redhat.com> - 0.9.0-0.2
- fixes and refinements

* Mon Feb 10 2014 William Benton <willb@redhat.com> - 0.9.0-0.1
- initial package
