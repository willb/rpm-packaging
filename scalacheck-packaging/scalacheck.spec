%global scalacheck_version 1.11.3
%global scala_version 2.10
%global SBT 0
%global ANT 1
%global build_style %{ANT}

Name:           scalacheck
Version:        %{scalacheck_version}
Release:        1%{?dist}
Summary:        property-based testing for Scala

License:        BSD
URL:            http://www.scalacheck.org
Source0:        https://github.com/rickynils/scalacheck/archive/%{scalacheck_version}.tar.gz

%if %{build_style} == %{SBT}
# remove cross-compilation (not supported for Fedora) and
# binary-compatibility testing (due to unsupported deps)
Patch0:		scalacheck-1.11.0-build.patch
%else
# We don't generate a POM from the ant build
Source1:       http://repo1.maven.org/maven2/org/scalacheck/%{name}_%{scala_version}/%{version}/%{name}_%{scala_version}-%{version}.pom

# remove maven-ant-tasks
Patch0:		scalacheck-1.11.3-ant-build.patch
%endif

BuildArch:	noarch
BuildRequires:  scala

%if %{build_style} == %{SBT}
BuildRequires:  sbt
%else
BuildRequires:	ant
%endif

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
find . -name \*.class -delete
find . -name \*.jar -delete

%if %{build_style} == %{SBT}
cp -r /usr/share/java/sbt/ivy-local .
mkdir boot
%else

%endif

%patch0 -p1

%if %{build_style} == %{SBT}
sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties
%endif

%build

%if %{build_style} == %{SBT}
export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration
%else
ant -Dversion=%{version} jar doc
%endif

%install

%if %{build_style} == %{SBT}

mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

install -pm 644 target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
install -pm 644 target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

%add_maven_depmap JPP-%{name}.pom %{name}.jar

cp -rp target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%else
mkdir -p %{buildroot}/%{_javadir}
install -m 644 target/%{name}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar

mkdir -p %{buildroot}/%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}/%{_javadocdir}/%{name}
cp -rp target/doc/main/api/* %{buildroot}/%{_javadocdir}/%{name}

# We only run %check in an ant build at the moment
%check
ant test

%endif

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README.markdown RELEASE

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog

* Wed Jan 29 2014 William Benton <willb@redhat.com> - 1.11.3-1 
- added optional but on-by-default Ant build (thanks to Gil Cattaneo for contributing this!)

* Mon Dec 23 2013 William Benton <willb@redhat.com> - 1.11.0-1 
- initial package
