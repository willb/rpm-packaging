%global debug_package %{nil}

Name:           racket
Version:        6.5
Release:        2%{?dist}
Summary:        Racket is a full-spectrum programming language.

License:        LGPL
URL:            https://download.racket-lang.org/
Source0:        https://mirror.racket-lang.org/installers/%{version}/%{name}-%{version}-src.tgz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libstdc++
BuildRequires:  libstdc++-devel
BuildRequires:  glibc-devel
BuildRequires:  make
BuildRequires:  bzip2
BuildRequires:  libffi-devel
BuildRequires:  libiodbc
BuildRequires:  openssl-libs
BuildRequires:  esound-libs
BuildRequires:  tcl
BuildRequires:  xmms-libs
BuildRequires:  xosd
BuildRequires:  gmp
BuildRequires:  libX11
BuildRequires:  gtk3
BuildRequires:  libedit
BuildRequires:  glib2
BuildRequires:  libpng
BuildRequires:  libjpeg
BuildRequires:  pango
BuildRequires:  libsndfile

Requires:       libffi
Requires:       libiodbc
Requires:       openssl-libs
Requires:       esound-libs
Requires:       tcl
Requires:       xmms-libs
Requires:       xosd
Requires:       gmp
Requires:       libX11
Requires:       gtk3
Requires:       libedit
Requires:       glib2
Requires:       libpng
Requires:       libjpeg
Requires:       pango
Requires:       libsndfile

%description

Racket is a full-spectrum programming language. It goes beyond Lisp
and Scheme with dialects that support objects, types, laziness, and
more. Racket enables programmers to link components written in
different dialects, and it empowers programmers to create new,
project-specific dialects. Racket's libraries support applications
from web servers and databases to GUIs and charts.

%prep
%setup -q


%build
cd src
%configure --disable-strip
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd src
%make_install
mkdir -p %{buildroot}/%{_docdir}/%{name}

%files
%doc src/COPYING_LESSER.txt src/COPYING-libscheme.txt src/COPYING.txt src/README
%{_bindir}/*
%{_libdir}/*
%{_datadir}/applications/*
%{_datadir}/%{name}/*
%{_sysconfdir}/*
%{_docdir}
%{_mandir}
%{_includedir}/%{name}/*

%changelog
* Tue Jun 14 2016 William Benton <willb@redhat.com> - 6.5-2
- added BRs and Rs for dynamically-loaded (i.e., not dynamically-linked) libraries

* Tue Jun 14 2016 William Benton <willb@redhat.com> - 6.5-1
- initial revision

