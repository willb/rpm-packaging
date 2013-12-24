%global test_interface_version 1.0

Name:           test-interface
Version:        %{test_interface_version}
Release:        1%{?dist}
Summary:        uniform interface to Scala test frameworks

License:        BSD
URL:            https://github.com/sbt/test-interface
Source0:        https://github.com/sbt/test-interface/archive/v%{test_interface_version}.tar.gz

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:  scala
Requires:       scala

%description

Uniform test interface to Scala/Java test frameworks (specs,
ScalaCheck, ScalaTest, JUnit and other)

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils
BuildArch:	noarch

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n test-interface-%{test_interface_version}

sed -i -e 's/2[.]10[.]2/2.10.3/g' build.sbt
sed -i -e '/scalatest_2.10/d' build.sbt

sed -i -e 's/0[.]12[.]4/0.13.1/g' project/build.properties
rm project/plugins.sbt

cp -r /usr/share/java/sbt/ivy-local .
cp -r /usr/share/java/sbt/boot .

%build

export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_javadir}
mkdir -p %{buildroot}/%{_mavenpomdir}

mkdir -p %{buildroot}/%{_javadocdir}/%{name}

cp target/%{name}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
cp target/%{name}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp target/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README

%files javadoc
%{_javadocdir}/%{name}


%changelog
