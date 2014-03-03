%global sxr_version 0.3.0
%global scala_version 2.10
%global jquery_version 1.3.2
%global jquery_scrollto_version 1.4.2
%global jquery_qtip_version 1.0.0-rc3

Name:           sxr
Version:        %{sxr_version}
Release:        1%{?dist}
Summary:        Scala XRay

# SXR itself is BSD-licensed, 
# JQuery and jquery-scrollto are dual-licensed under MIT and GPL, and 
# jquery-qtip is licensed under MIT
License:        BSD and (MIT or GPL) and MIT
URL:            https://github.com/harrah/browse/
Source0:        https://github.com/harrah/browse/archive/v%{sxr_version}.tar.gz
Source1:	http://jqueryjs.googlecode.com/files/jquery-%{jquery_version}.js
Source2:	http://flesler-plugins.googlecode.com/files/jquery.scrollTo-%{jquery_scrollto_version}.js
Source3:	http://craigsworks.com/projects/qtip/packages/1.0.0-rc3/jquery.qtip-%{jquery_qtip_version}.js

BuildArch:	noarch
BuildRequires:  sbt
BuildRequires:  scala
BuildRequires:	javapackages-tools
Requires:	javapackages-tools
Requires:       scala

%description

Browsable Scala source code in HTML with: syntax highlighting,
types/applied implicits in tooltips, references/definition highlighted
on mouseover, and links to definitions.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
BuildArch:	noarch

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n browse-%{sxr_version}

cp %{SOURCE1} .
cp %{SOURCE2} .
cp %{SOURCE3} .

sed -i -e 's/% "js->default"//g' project/XRay.scala
sed -i -e 's/2[.]10[.]2/2.10.3/g' project/XRay.scala
sed -i -e 's|http://jqueryjs.googlecode.com/files/|file://%{_builddir}/|g' project/XRay.scala
sed -i -e 's|http://flesler-plugins.googlecode.com/files/|file://%{_builddir}/|g' project/XRay.scala
sed -i -e 's|http://craigsworks.com/projects/qtip/packages/%{jquery_qtip_version}/|file://%{_builddir}/|g' project/XRay.scala

sed -i -e 's/0[.]13[.]0/0.13.1/g' project/build.properties

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

cp target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.jar %{buildroot}/%{_javadir}/%{name}.jar
cp target/scala-%{scala_version}/%{name}_%{scala_version}-%{version}.pom %{buildroot}/%{_mavenpomdir}/JPP-%{name}.pom

cp -rp target/scala-%{scala_version}/api/* %{buildroot}/%{_javadocdir}/%{name}

%add_maven_depmap JPP-%{name}.pom %{name}.jar

%files
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%doc LICENSE README.md

%files javadoc
%{_javadocdir}/%{name}


%changelog

* Mon Jan 6 2014 William Benton <willb@redhat.com> - 0.3.0-1
- initial package
