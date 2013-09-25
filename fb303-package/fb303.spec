%global pkg_version 0.9.1
%global pkg_rel 3

Name:		fb303
Version:	%{pkg_version}
Release:	%{pkg_rel}%{?dist}
Summary:	Basic interface for Thrift services

License:	ASL 2.0
URL:		http://thrift.apache.org/
Source0:	http://archive.apache.org/dist/thrift/%{version}/thrift-%{version}.tar.gz
Source1:        http://repo1.maven.org/maven2/org/apache/thrift/lib%{name}/%{version}/lib%{name}-%{version}.pom
Patch0:         fb303-0.9.1-buildxml.patch
Group:		Development/Libraries

BuildRequires:	gcc-c++
BuildRequires:	libstdc++-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:	boost-devel
BuildRequires:	thrift = %{version}
BuildRequires:	thrift-devel = %{version}

Requires:	thrift = %{version}

%description
fb303 is the shared root of all Thrift services; it provides a
standard interface to monitoring, dynamic options and configuration,
uptime reports, activity, etc.

%package -n python-%{name}
Summary:        Python bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  python2-devel

%description -n python-%{name}
The python-%{name} package contains Python bindings for %{name}.

%package -n java-%{name}
Summary:        Java bindings for %{name}
Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
Requires:       mvn(org.slf4j:slf4j-api)
Requires:       mvn(commons-lang:commons-lang)
Requires:       mvn(org.apache.httpcomponents:httpclient)
Requires:       mvn(org.apache.httpcomponents:httpcore)
BuildRequires:  ant
BuildRequires:  java-libthrift = %{version}
BuildArch:      noarch

%description -n java-%{name}
The java-%{name} package contains Java bindings for %{name}.

%prep
%setup -q -n thrift-%{version}
%patch0 -p1
echo "all:
	ant
install: build/libfb303.jar
	mkdir -p %{buildroot}%{_javadir}
	/usr/bin/install -c -m 644 build/libfb303.jar %{buildroot}%{_javadir}
" > contrib/fb303/java/Makefile

%build
cd contrib/fb303
./bootstrap.sh
%configure --with-thriftpath=/usr --disable-static --with-java --without-php
make

%install
cd contrib/fb303
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.egg-info' -exec rm -rf {} ';' -quit

# Add POM file and depmap
mkdir -p %{buildroot}%{_mavenpomdir}
install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-lib%{name}.pom
%add_maven_depmap JPP-lib%{name}.pom lib%{name}.jar

test -d %{buildroot}/%{_libdir} || mkdir -p %{buildroot}/%{_libdir}
find %{buildroot} -name \*.so -exec mv {} %{buildroot}/%{_libdir}/ \;

chmod 755 $(find %{buildroot} -name \*.py -exec grep -q /usr/bin/env {} \; -print)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_includedir}/thrift/fb303
%{_libdir}/libfb303.so
%{_datarootdir}/fb303
%doc LICENSE NOTICE

%files -n python-%{name}
%{python_sitelib}/fb303
%{python_sitelib}/fb303_scripts
%doc LICENSE NOTICE

%files -n java-%{name}
%{_javadir}/lib%{name}.jar
%{_mavenpomdir}/JPP-lib%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE NOTICE

%changelog

* Wed Sep 25 2013 willb <willb@redhat> - 0.9.1-2
- Updated for Thrift 0.9.1-2 (release number is synchronized with thrift)
- Enabled Java support

* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-3
- Initial package (release number is synchronized with thrift)

