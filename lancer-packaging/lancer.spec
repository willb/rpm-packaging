Name:           lancer
Version:        0.0.2
Release:        2%{?dist}
Summary:        Probability and statistics classes for Java
License:        ASL 2.0
URL:            https://github.com/willb/lancer/
Source0:        https://github.com/willb/lancer/archive/v%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(org.apache.commons:commons-math3)

%description
Lancer is a reimplementation of some functionality provided by the
(non-free) Colt library.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -q

echo %{summary} > README

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README
%doc LICENSE
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Tue Mar 11 2014 William Benton <willb@redhat.com> - 0.0.2-2
- rebuilding

* Tue Mar 11 2014 William Benton <willb@redhat.com> - 0.0.2-1
- updated to upstream version 0.0.2 (test changes only)

* Wed Feb 26 2014 William Benton <willb@redhat.com> - 0.0.1-1
- Initial packaging
