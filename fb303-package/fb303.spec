%global pkg_version 0.9.0
%global pkg_rel 3

Name:		fb303
Version:	%{pkg_version}
Release:	%{pkg_rel}%{?dist}
Summary:	Basic interface for Thrift services

License:	ASL 2.0
URL:		http://thrift.apache.org/
Source0:	http://archive.apache.org/dist/thrift/%{version}/thrift-%{version}.tar.gz

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

%prep
%setup -q -n thrift-%{version}

%build
cd contrib/fb303
./bootstrap.sh
%configure --with-thriftpath=/usr --disable-static
make

%install
cd contrib/fb303
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.egg-info' -exec rm -rf {} ';' -quit

test -d %{buildroot}/%{_libdir} || mkdir -p %{buildroot}/%{_libdir}
find %{buildroot} -name \*.so -exec mv {} %{buildroot}/%{_libdir}/ \;

chmod 755 $(find %{buildroot} -name \*.py -exec grep -q /usr/bin/env {} \; -print)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_includedir}/thrift/fb303
%{_libdir}/libfb303.so
/usr/share/fb303
%doc LICENSE NOTICE

%files -n python-%{name}
%{python_sitelib}/fb303
%{python_sitelib}/fb303_scripts
%doc LICENSE NOTICE

%changelog

* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-3
- Initial package (release number is synchronized with thrift)

