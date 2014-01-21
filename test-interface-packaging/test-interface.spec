%global test_interface_version 1.0
%global build_with_sbt 0

Name:           test-interface
Version:        %{test_interface_version}
Release:        1%{?dist}
Summary:        uniform interface to Scala and Java test frameworks

License:        BSD
URL:            https://github.com/sbt/test-interface
Source0:        https://github.com/sbt/test-interface/archive/v%{test_interface_version}.tar.gz
%if !%{build_with_sbt}
Source1:	http://mirrors.ibiblio.org/maven2/org/scala-sbt/%{name}/%{version}/%{name}-%{version}.pom
%endif

BuildArch:	noarch
%if %{build_with_sbt}
BuildRequires:  sbt
%else
BuildRequires:	java-devel
%endif
BuildRequires:	javapackages-tools
Requires:	javapackages-tools

%description

Uniform test interface to Scala/Java test frameworks (specs,
ScalaCheck, ScalaTest, JUnit and other)

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
BuildArch:	noarch

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%if %{build_with_sbt}
sed -i -e 's/2[.]10[.]2/2.10.3/g' build.sbt
sed -i -e '/scalatest_2.10/d' build.sbt

sed -i -e 's/0[.]12[.]4/0.13.1/g' project/build.properties
rm project/plugins.sbt

cp -r /usr/share/java/sbt/ivy-local .
mkdir boot
%else # building without sbt

cp -p %{SOURCE1} pom.xml
# Remove unavailable test dep
%pom_remove_dep :scalatest_2.10

%endif

%build

%if %{build_with_sbt}
export SBT_BOOT_DIR=boot
export SBT_IVY_DIR=ivy-local
sbt package deliverLocal publishM2Configuration
%else # building without sbt
mkdir -p classes target/api
%javac -d classes $(find src/main/java -name "*.java")

(
cd classes
mkdir -p META-INF
cat > META-INF/MANIFEST.MF << 'EOF'
'EOF'
Manifest-Version: 1.0
Implementation-Vendor: org.scala-sbt
Implementation-Title: %{name}
Implementation-Version: %{version}
Implementation-Vendor-Id: org.scala-sbt
Specification-Vendor: org.scala-sbt
Specification-Title: %{name}
Specification-Version: %{version}
EOF
%jar -cMf ../target/%{name}-%{version}.jar *
)

%javadoc -d target/api -classpath $PWD/target/%{name}.jar $(find src/main/java -name "*.java")

cp pom.xml target/%{name}-%{version}.pom

%endif

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

* Mon Dec 23 2013 William Benton <willb@redhat.com> - 1.0-1
- initial package
