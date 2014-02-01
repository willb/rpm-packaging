# this is the version we need for Spark
%global lift_version 2.5.1
%global scala_version 2.10
%global scala_long_version 2.10.3
%global upstream_src_dir Lift-%{lift_version}

# group, artifact, new version, file
%global remap_version() sed -i -e 's/"%{1}" %% "%{2}" %% "[^"]*"/"%{1}" %% "%{2}" %% "'%{3}'"/g' %{4} 

# group, artifact, file
%global remap_version_to_installed() sed -i -e 's/"%{1}" %% "%{2}" %% "[^"]*"/"%{1}" %% "%{2}" %% "'$(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))'"/g' %{3} 

# group, artifact
%global climbing_nemesis() ./climbing-nemesis.py %{1} %{2} ivy-local --version $(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))

Name:           lift
Version:        %{lift_version}
Release:        1%{?dist}
Summary:        Scala web framework

License:        MIT
URL:            http://liftweb.net
Source0:        https://github.com/lift/framework/archive/%{lift_version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:	python
BuildRequires:	java-devel
BuildRequires:	javapackages-tools

Requires:	maven-local
Requires:	javapackages-tools
Requires:       scala

%description

Lift is the most powerful, most secure web framework available
today. There are Seven Things that distinguish Lift from other web
frameworks.

Lift applications are:

* Secure -- Lift apps are resistant to common vulnerabilities
  including many of the OWASP Top 10

* Developer centric -- Lift apps are fast to build, concise and easy
  to maintain

* Scalable -- Lift apps are high performance and scale in the real
  world to handle insane traffic levels

* Interactive like a desktop app -- Lift's Comet support is unparalled
  and Lift's ajax support is super-easy and very secure

Because Lift applications are written in Scala, an elegant JVM
language, you can still use your favorite Java libraries and deploy to
your favorite Servlet Container and app server. Use the code you've
already written and deploy to the container you've already configured!

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{lift_version}

%patch0 -p1
%patch1 -p1

# don't cross-compile for other Scala versions
sed -i -e 's/(crossScalaVersions[^:]*) := Seq[(].*[)]/\1 := Seq()/g' build.sbt

%remap_version_to_installed com.h2database h2 project/Dependencies.scala

%remap_version_to_installed mysql mysql-connector-java project/Dependencies.scala

%remap_version_to_installed postgresql postgresql project/Dependencies.scala

%remap_version_to_installed net.sourceforge.jtds jtds project/Dependencies.scala

%remap_version_to_installed org.apache.derby derby project/Dependencies.scala

%remap_version_to_installed junit junit project/Dependencies.scala

sed -i -e 's/cross CVMapping.*//' project/Dependencies.scala

sed -i -e 's/2[.]10[.][0-2]/2.10.3/g' project/Dependencies.scala build.sbt

sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties || echo sbt.version=0.13.1 > project/build.properties

rm -f project/plugins.sbt

cp -r /usr/share/java/sbt/ivy-local .
mkdir boot

cp %{SOURCE1} .

chmod 755 climbing-nemesis.py

%climbing_nemesis org.scala-lang scalap ivy-local

%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

export JARNAME=$(echo %{name} | tr \[A-Z] \[a-z])

install -pm 644 target/scala-%{scala_version}/${JARNAME}_%{scala_version}-%{lift_version}.jar %{buildroot}/%{_javadir}/%{name}.jar
install -pm 644 target/scala-%{scala_version}/${JARNAME}_%{scala_version}-%{lift_version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc license.txt readme.markdown

%files javadoc
%{_javadocdir}/%{name}
%doc license.txt readme.markdown

%changelog

* Thu Jan 23 2014 William Benton <willb@redhat.com> - 0.9.5.6-1
- initial package
