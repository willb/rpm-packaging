%global squeryl_version 0.9.5-6
%global squeryl_rpm_version 0.9.5.6
%global scala_version 2.10
%global scala_long_version 2.10.3
%global upstream_src_dir Squeryl-%{squeryl_version}

# group, artifact, new version, file
%global remap_version() sed -i -e 's/"%{1}" %% "%{2}" %% "[^"]*"/"%{1}" %% "%{2}" %% "'%{3}'"/g' %{4} 

# group, artifact, file
%global remap_version_to_installed() sed -i -e 's/"%{1}" %% "%{2}" %% "[^"]*"/"%{1}" %% "%{2}" %% "'$(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))'"/g' %{3} 

# group, artifact
%global climbing_nemesis() ./climbing-nemesis.py %{1} %{2} ivy-local --version $(rpm -q --qf "%%%%{version}" $(rpm -q --whatprovides "mvn(%{1}:%{2})" ))

Name:           Squeryl
Version:        %{squeryl_rpm_version}
Release:        1%{?dist}
Summary:        Scala ORM and DSL for SQL databases

License:        MIT
URL:            https://github.com/max-l/Squeryl
Source0:        https://github.com/max-l/Squeryl/archive/%{squeryl_version}.tar.gz
Source1:	https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py

Patch0:		squeryl-0.9.5.6-notestdeps.patch
Patch1:		squeryl-0.9.5-6-noSNAPSHOT.patch

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:	python
BuildRequires:	java-devel
BuildRequires:	mvn(cglib:cglib)
BuildRequires:	mvn(com.h2database:h2)
BuildRequires:	mvn(mysql:mysql-connector-java)
BuildRequires:	mvn(postgresql:postgresql)
BuildRequires:	mvn(net.sourceforge.jtds:jtds)
BuildRequires:	mvn(org.apache.derby:derby)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(asm:asm)
BuildRequires:	mvn(org.hamcrest:hamcrest-core)
BuildRequires:	javapackages-tools

Requires:	mvn(cglib:cglib)
Requires:	mvn(com.h2database:h2)
Requires:	mvn(mysql:mysql-connector-java)
Requires:	mvn(postgresql:postgresql)
Requires:	mvn(net.sourceforge.jtds:jtds)
Requires:	mvn(org.apache.derby:derby)
Requires:	mvn(junit:junit)
Requires:	maven-local
Requires:	javapackages-tools
Requires:       scala

%description

Squeryl is a Scala ORM and DSL for talking with databases with minimum
verbosity and maximum type safety.  Squeryl statements that pass
compilation won’t fail at runtime. Refactor your schema as often as is
required, the Scala compiler and your IDE will tell you exactly which
lines of code are affected.  The composability of Squeryl statements
allows you to define them once and reuse them as sub queries within
other statements.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{squeryl_version}

%patch0 -p1
%patch1 -p1

# don't cross-compile for other Scala versions
sed -i -e 's/crossScalaVersions := Seq[(].*[)]/crossScalaVersions := Seq()/g' project/SquerylBuild.scala
sed -i -e 's/% "provided"//g' project/SquerylBuild.scala

sed -i -e 's/-nodep//g' project/SquerylBuild.scala

sed -i -e 's/, "-target", "1.6"/, "-target", "1.6", "-encoding", "UTF-8", "-J-Drelease"/' project/SquerylBuild.scala

%remap_version_to_installed com.h2database h2 project/SquerylBuild.scala

%remap_version_to_installed mysql mysql-connector-java project/SquerylBuild.scala

%remap_version_to_installed postgresql postgresql project/SquerylBuild.scala

%remap_version_to_installed net.sourceforge.jtds jtds project/SquerylBuild.scala

%remap_version_to_installed org.apache.derby derby project/SquerylBuild.scala

%remap_version_to_installed junit junit project/SquerylBuild.scala

sed -i -e 's/2[.]10[.][0-2]/2.10.3/g' project/SquerylBuild.scala

sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties || echo sbt.version=0.13.1 > project/build.properties

echo release=true >> project/build.properties

rm -f project/plugins.sbt

cp -r /usr/share/java/sbt/ivy-local .
mkdir boot

cp %{SOURCE1} .

chmod 755 climbing-nemesis.py

%climbing_nemesis org.scala-lang scalap ivy-local

%{climbing_nemesis cglib cglib-full ivy-local} --ignore asm --extra-dep asm:asm:$(rpm -q --qf "%%{version}" $(rpm -q --whatprovides "mvn(asm:asm)" ))

%climbing_nemesis com.h2database h2 ivy-local

%climbing_nemesis mysql mysql-connector-java ivy-local

%climbing_nemesis postgresql postgresql ivy-local

%climbing_nemesis net.sourceforge.jtds jtds ivy-local

%climbing_nemesis org.apache.derby derby ivy-local

%{climbing_nemesis junit junit ivy-local } --ignore hamcrest

%climbing_nemesis asm asm ivy-local

%climbing_nemesis org.hamcrest hamcrest-core ivy-local

%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

install -pm 644 core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
install -pm 644 core/target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp core/target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog

* Tue Jan 7 2014 William Benton <willb@redhat.com> - 0.4.2-1
- initial package
