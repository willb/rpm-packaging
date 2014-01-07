%global scalacheck_version 1.11.0
%global scala_version 2.10

Name:           scalacheck
Version:        %{scalacheck_version}
Release:        1%{?dist}
Summary:        property-based testing for Scalas

License:        BSD
URL:            http://www.scalacheck.org
Source0:        https://github.com/rickynils/scalacheck/archive/%{scalacheck_version}.tar.gz
Patch0:		scalacheck-1.11.0-build.patch

BuildArch:	noarch
BuildRequires:  scala
BuildRequires:  sbt
BuildRequires:	mvn(org.scala-sbt:test-interface)
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:       scala

%description

ScalaCheck is a library written in Scala and used for automated
property-based testing of Scala or Java programs. ScalaCheck was
originally inspired by the Haskell library QuickCheck, but has also
ventured into its own.

ScalaCheck has no external dependencies other than the Scala runtime,
and works great with sbt, the Scala build tool. It is also fully
integrated in the test frameworks ScalaTest and specs2. You can of
course also use ScalaCheck completely standalone, with its built-in
test runner.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
BuildArch:      noarch

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
find . -name \*.jar -delete

cp -r /usr/share/java/sbt/ivy-local .
cp -r /usr/share/java/sbt/boot .

%patch0 -p1

sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties

%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

cp target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
cp target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

cp -rp target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README.markdown

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE README.markdown

%changelog

* Mon Dec 23 2013 William Benton <willb@redhat.com> - 1.11.0-1 
- initial package
