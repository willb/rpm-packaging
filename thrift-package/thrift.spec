%global pkg_version 0.9.0

Name:           thrift
Version:        %{pkg_version}
Release:        1%{?dist}
Summary:        Software framework for scalable cross-language services development

License:        Apache 2.0
URL:            http://thrift.apache.org/
Source0:        http://archive.apache.org/dist/%{name}/%{pkg_version}/%{name}-%{pkg_version}.tar.gz

BuildRequires:  
Requires:       

%description

The Apache Thrift software framework, for scalable cross-language services development, combines a software stack with a code generation engine to build services that work efficiently and seamlessly between C++, Java, Python, PHP, Ruby, Erlang, Perl, Haskell, C\#, Cocoa, JavaScript, Node.js, Smalltalk, OCaml and Delphi and other languages. 

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so


%changelog
