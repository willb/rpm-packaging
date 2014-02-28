%global spark_version 0.9.0
%global spark_version_suffix -incubating
%global scala_version 2.10

%if 0%{?fedora} >= 20
%global want_hadoop 1
%else
%global want_hadoop 0
%endif

%global remap_version_to_installed() sed -i -e 's/"%{1}"[\t ]*%%[\t ]*"%{2}"[\t ]*%%[\t ]*"[^"]*"/"%{1}" %% "%{2}" %% "'$(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))'"/g' %{3}

%global climbing_nemesis() ./climbing-nemesis.py %{1} %{2} ivy-local --version $(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))

Name:		spark
Version:	%{spark_version}
Release:	0.1%{?dist}
Summary:	Lightning-fast cluster computing

License:	ASL 2.0
URL:		http://spark.apache.org
Source0:	https://github.com/apache/spark/archive/v%{spark_version}%{spark_version_suffix}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

Patch0:		spark-v0.9.0-0001-Replace-lift-json-with-json4s-jackson.patch
Patch1:		spark-v0.9.0-0002-use-sbt-0.13.1.patch
Patch2:		spark-v0.9.0-0003-Removed-sbt-plugins.patch
Patch3:		spark-v0.9.0-0004-removed-examples.patch
Patch4:		spark-v0.9.0-0005-Removed-code-depending-on-Kryo.patch
Patch5:		spark-v0.9.0-0006-Remove-functionality-depending-on-stream-lib.patch
Patch6:		spark-v0.9.0-0007-Removed-mesos.patch

BuildArch:	noarch
BuildRequires:	sbt
BuildRequires:	scala
BuildRequires:	python
BuildRequires:	maven-local
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:	scala

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


# XXX: remove these once they aren't necessary
BuildRequires:	mvn(commons-io:commons-io)
Requires:	mvn(commons-io:commons-io)


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

# use regular Akka
sed -i -e 's/org[.]spark-project[.]akka/com.typesafe.akka/' project/SparkBuild.scala
sed -i -e 's/2[.]2[.]3-shaded-protobuf/2.3.0-RC2/' project/SparkBuild.scala

# remove all test deps for now
sed -i -e '/%[[:space:]]*"test"/d' project/SparkBuild.scala

# make sure we haven't introduced any syntax errors by pulling out the
# final elements in sequence literals
sed -i -e 'N;s/\([%].*["]\),\n\([\t ]*[)]\)/\1\n\2/' project/SparkBuild.scala
sed -i -e 'N;s/\([%].*[)]\),\n\([\t ]*[)]\)/\1\n\2/' project/SparkBuild.scala

cp -r /usr/share/sbt/ivy-local ivy-local
mkdir boot

# make sure we're expecting the right versions; skip things like
# json4s and akka that we handle explicitly elsewhere

%remap_version_to_installed com.codahale.metrics metrics-core project/SparkBuild.scala

%remap_version_to_installed com.codahale.metrics metrics-ganglia project/SparkBuild.scala

%remap_version_to_installed com.codahale.metrics metrics-graphite project/SparkBuild.scala

%remap_version_to_installed com.codahale.metrics metrics-json project/SparkBuild.scala

%remap_version_to_installed com.codahale.metrics metrics-jvm project/SparkBuild.scala

%remap_version_to_installed com.google.code.findbugs jsr305 project/SparkBuild.scala

%remap_version_to_installed com.google.guava guava project/SparkBuild.scala

%remap_version_to_installed commons-daemon commons-daemon project/SparkBuild.scala

# XXX: we don't need this
%remap_version_to_installed commons-io commons-io project/SparkBuild.scala

%remap_version_to_installed com.ning compress-lzf project/SparkBuild.scala

%remap_version_to_installed io.netty netty-all project/SparkBuild.scala

%remap_version_to_installed it.unimi.dsi fastutil project/SparkBuild.scala

%remap_version_to_installed log4j log4j project/SparkBuild.scala

%remap_version_to_installed net.java.dev.jets3t jets3t project/SparkBuild.scala

%remap_version_to_installed org.apache.hadoop hadoop-client project/SparkBuild.scala

%remap_version_to_installed org.apache.hadoop hadoop-client project/SparkBuild.scala

%remap_version_to_installed org.apache.hadoop hadoop-yarn-api project/SparkBuild.scala

%remap_version_to_installed org.apache.hadoop hadoop-yarn-client project/SparkBuild.scala

%remap_version_to_installed org.apache.hadoop hadoop-yarn-common project/SparkBuild.scala

%remap_version_to_installed org.apache.zookeeper zookeeper project/SparkBuild.scala

%remap_version_to_installed org.eclipse.jetty jetty-server project/SparkBuild.scala

%remap_version_to_installed org.eclipse.jetty.orbit javax.servlet project/SparkBuild.scala

%remap_version_to_installed org.jblas jblas project/SparkBuild.scala

%remap_version_to_installed org.ow2.asm asm project/SparkBuild.scala

%remap_version_to_installed org.slf4j slf4j-api project/SparkBuild.scala

%remap_version_to_installed org.slf4j slf4j-log4j12 project/SparkBuild.scala

%remap_version_to_installed org.xerial.snappy snappy-java project/SparkBuild.scala

# generate local Ivy repository
cp %{SOURCE1} .
chmod 755 ./climbing-nemesis.py

%climbing_nemesis com.freevariable.lancer lancer

%climbing_nemesis org.json4s json4s-jackson_%{scala_version}

%climbing_nemesis com.codahale.metrics metrics-core

%climbing_nemesis com.codahale.metrics metrics-ganglia

%climbing_nemesis com.codahale.metrics metrics-graphite

%climbing_nemesis com.codahale.metrics metrics-json

%climbing_nemesis com.codahale.metrics metrics-jvm

%climbing_nemesis com.google.code.findbugs jsr305

%climbing_nemesis com.google.guava guava

%climbing_nemesis commons-daemon commons-daemon

%climbing_nemesis commons-io commons-io

%climbing_nemesis com.ning compress-lzf

%climbing_nemesis io.netty netty-all

%climbing_nemesis it.unimi.dsi fastutil

%climbing_nemesis log4j log4j

%climbing_nemesis net.java.dev.jets3t jets3t

%climbing_nemesis org.apache.hadoop hadoop-client

%climbing_nemesis org.apache.zookeeper zookeeper

%climbing_nemesis org.eclipse.jetty jetty-server

%climbing_nemesis org.eclipse.jetty.orbit javax.servlet

%climbing_nemesis org.jblas jblas

%climbing_nemesis org.ow2.asm asm

%climbing_nemesis org.slf4j slf4j-api

%climbing_nemesis org.slf4j slf4j-log4j12

%climbing_nemesis com.typesafe.akka akka-remote_%{scala_version}

%climbing_nemesis com.typesafe.akka akka-actor_%{scala_version}

%climbing_nemesis org.xerial.snappy snappy-java


%build

export SPARK_HADOOP_VERSION=2.2.0
export DEFAULT_IS_NEW_HADOOP=true

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local

sbt package "set publishTo in Global := Some(Resolver.file(\"published\", file(\"published\"))(Resolver.ivyStylePatterns) ivys \"$(pwd)/published/[organization]/[module]/[revision]/ivy.xml\" artifacts \"$(pwd)/published/[organization]/[module]/[revision]/[artifact]-[revision].[ext]\")" publish makePom

# XXX: this is a hack; we seem to get correct metadata but bogus JARs
# from "sbt publish" for some reason
for f in $(find published -name \*.jar ) ; do
  find . -ipath \*target\* -and -name $(basename $f) -exec cp '{}' $f \;
done

%install
mkdir -p %{buildroot}/%{_javadir}/%{name}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}
for apidir in $(find . -name api -type d) ; do
  pushd $apidir
  cp -rp . %{buildroot}/%{_javadocdir}/%{name}
  popd
done

for jar in $(find published -name \*.jar | grep -v %{name}_%{scala_version}-%{version}.jar) ; do
  install -m 644 $jar %{buildroot}/%{_javadir}/%{name}/$(echo $jar | cut -f5 -d/ | cut -f1 -d_).jar
done

declare -a shortnames

for pom in $(find published -name \*.pom | grep -v %{name}_%{scala_version}-%{version}.pom ) ; do 
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

* Mon Feb 10 2014 William Benton <willb@redhat.com> - 0.9.0-1
- initial package
