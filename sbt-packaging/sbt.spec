%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3

Name:           sbt
Version:        0.13.0
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}.tar.gz
%if %{do_bootstrap}
# include bootstrap libraries

%endif

BuildRequires:  scala
%if !%{do_bootstrap}
BuildRequires:  sbt
%endif

Requires:       scala

%description
sbt is the simple build tool for Scala and Java projects.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install


%files
%doc



%changelog
