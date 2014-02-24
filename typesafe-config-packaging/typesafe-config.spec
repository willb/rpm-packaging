Name:          typesafe-config
Version:       1.2.0
Release:       1%{?dist}
Summary:       Configuration library for JVM languages
License:       ASL 2.0
URL:           https://github.com/typesafehub/config/
Source0:       https://github.com/typesafehub/config/archive/v%{version}.tar.gz
Source1:       typesafe-config-template.pom
# http://mirrors.ibiblio.org/maven2/com/typesafe/config/1.1.0-9f31d6308e7ebbc3d7904b64ebb9f61f7e22a968/config-1.1.0-9f31d6308e7ebbc3d7904b64ebb9f61f7e22a968.pom
BuildRequires: java-devel
BuildRequires: javapackages-tools

Requires:      java
Requires:      javapackages-tools
BuildArch:     noarch

%description
Configuration library for JVM languages.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n config-%{version}

%build

mkdir -p config/classes config/target/api
%javac -d config/classes $(find config/src/main/java -name "*.java")

(
cd config/classes
%jar -cf ../target/%{name}-%{version}.jar *
)

%javadoc -d config/target/api \
 -classpath $PWD/config/target/%{name}-%{version}.jar \
 $(find config/src/main/java -name "*.java")

%install

mkdir -p %{buildroot}%{_javadir}
cp -p config/target/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp config/target/api/* %{buildroot}%{_javadocdir}/%{name}

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE-2.0.txt NEWS.md README.md

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE-2.0.txt

%changelog
* Tue Feb 04 2014 gil cattaneo <puntogil@libero.it> 1.2.0-1
- initial rpm