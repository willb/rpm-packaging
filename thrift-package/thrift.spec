%global pkg_version 0.9.1
%global fb303_version 1.0.0_dev
%global pkg_rel 10

%global py_version 2.7

%global php_extdir  %(php-config --extension-dir 2>/dev/null || echo "undefined")

%{?perl_default_filter}
%global __provides_exclude_from ^(%{python_sitearch}/.*\\.so|%{php_extdir}/.*\\.so)$

%global have_mongrel 0

%if 0%{?fedora} >= 19
# erlang-jsx is available in F19
%global have_jsx 1
%else
%global have_jsx 0
%endif

# We should be able to enable this in the future
%global want_d 0

# Thrift's Ruby support depends on Mongrel.  Since Mongrel is
# deprecated in Fedora, we can't support Ruby bindings for Thrift
# unless and until Thrift is patched to use a different HTTP server.
%if 0%{?have_mongrel} == 0
%global ruby_configure --without-ruby
%global with_ruby 0
%else
%global ruby_configure --with-ruby
%global want_ruby 1
%endif

# Thrift's Erlang support depends on the JSX library, which is not
# currently available in Fedora.

%if 0%{?have_jsx} == 0
%global erlang_configure --without-erlang
%global want_erlang 0
%else
%global erlang_configure --with-erlang
%global want_erlang 1
%endif

# PHP appears broken in Thrift 0.9.1
%global want_php 0

%if 0%{?want_php} == 0
%global php_langname %{nil}
%global php_configure --without-php
%else
%global php_langname PHP,\ 
%global php_configure --with-php
%endif

# Thrift's GO support doesn't build under Fedora
%global want_golang 0
%global golang_configure --without-go

Name:		thrift
Version:	%{pkg_version}
Release:	%{pkg_rel}%{?dist}
Summary:	Software framework for cross-language services development

# Parts of the source are used under the BSD and zlib licenses, but
# these are OK for inclusion in an Apache 2.0-licensed whole:
# http://www.apache.org/legal/3party.html

# Here's the breakdown:
# thrift-0.9.1/lib/py/compat/win32/stdint.h is 2-clause BSD
# thrift-0.9.1/compiler/cpp/src/md5.[ch] are zlib
License:	ASL 2.0 and BSD and zlib
URL:		http://thrift.apache.org/

%if "%{version}" != "0.9.1"
Source0:	http://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}.tar.gz
%else
# Unfortunately, the distribution tarball for thrift-0.9.1 is broken, so we're
# using an exported tarball from git.  This will change in the future.

Source0:	https://github.com/apache/thrift/archive/0.9.1.tar.gz
%endif

Source1:	http://repo1.maven.org/maven2/org/apache/thrift/lib%{name}/%{version}/lib%{name}-%{version}.pom
Source2:	https://raw.github.com/apache/%{name}/%{version}/bootstrap.sh

Source3:        https://gitorious.org/pkg-scribe/thrift-deb-pkg/raw/master:debian/manpage.1.ex
Source4:	http://repo1.maven.org/maven2/org/apache/thrift/libfb303/%{version}/libfb303-%{version}.pom

# this patch is adapted from Gil Cattaneo's thrift-0.7.0 package
Patch0:		thrift-0.9.1-buildxml.patch
# don't use bundled rebar executable
Patch1:		thrift-0.9.1-rebar.patch
# for fb303, excise maven ant tasks; build against system libraries; etc.
Patch2:		fb303-0.9.1-buildxml.patch

Group:		Development/Libraries

# BuildRequires for language-specific bindings are listed under these
# subpackages, to facilitate enabling or disabling individual language
# bindings in the future

BuildRequires:	libstdc++-devel
BuildRequires:	boost-devel
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRequires:	bison-devel
BuildRequires:	flex-devel
%ifarch %{mono_arches}
BuildRequires:	mono-devel
%endif
BuildRequires:	glib2-devel
BuildRequires:	texlive
BuildRequires:	qt-devel

BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	automake

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	bison-devel
BuildRequires:	flex-devel

BuildRequires:	ant

%ifarch %{mono_arches}
Requires:	mono-core
%endif

%if 0%{?want_golang} > 0
BuildRequires:	golang
Requires:	golang
%endif

%description

The Apache Thrift software framework for cross-language services
development combines a software stack with a code generation engine to
build services that work efficiently and seamlessly between C++, Java,
Python, %{?php_langname}and other languages.

%package	 devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	pkgconfig
Requires:	boost-devel

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n	python-%{name}
Summary:	Python support for %{name}
BuildRequires:	python2-devel
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	python2

%description -n python-%{name}
The python-%{name} package contains Python bindings for %{name}.

%package -n	perl-%{name}
Summary:	Perl support for %{name}
Provides:	perl(Thrift) = %{version}-%{release}
BuildRequires:	perl(Bit::Vector)
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(Bit::Vector)
Requires:	perl(Encode)
Requires:	perl(HTTP::Request)
Requires:	perl(IO::Select)
Requires:	perl(IO::Socket::INET)
Requires:	perl(IO::String)
Requires:	perl(LWP::UserAgent)
Requires:	perl(POSIX)
Requires:	perl(base)
Requires:	perl(constant)
Requires:	perl(strict)
Requires:	perl(utf8)
Requires:	perl(warnings)
BuildArch:	noarch

%description -n perl-%{name}
The perl-%{name} package contains Perl bindings for %{name}.

%if %{?want_d}
%package -n	d-%{name}
Summary:	D support for %{name}
BuildRequires:	ldc

%description -n d-%{name}
The d-%{name} package contains D bindings for %{name}.
%endif

%if 0%{?want_php} != 0
%package -n	php-%{name}
Summary:	PHP support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	php(zend-abi) = %{php_zend_api}
Requires:	php(api) = %{php_core_api}
Requires:	php(language) >= 5.3.0
Requires:	php-date
Requires:	php-json
BuildRequires:	php-devel

%description -n php-%{name}
The php-%{name} package contains PHP bindings for %{name}.
%endif

%package -n	lib%{name}-javadoc
Summary:	API documentation for java-%{name}
Requires:	lib%{name}-java = %{version}-%{release}
BuildArch:	noarch

%description -n lib%{name}-javadoc 
The lib%{name}-javadoc package contains API documentation for the
Java bindings for %{name}.

%package -n	lib%{name}-java
Summary:	Java support for %{name}

BuildRequires:	java-devel
BuildRequires:	javapackages-tools
BuildRequires:	apache-commons-codec
BuildRequires:	apache-commons-lang
BuildRequires:	apache-commons-logging
BuildRequires:	httpcomponents-client
BuildRequires:	httpcomponents-core
BuildRequires:	junit
BuildRequires:	log4j
BuildRequires:	slf4j
BuildRequires:	tomcat-servlet-3.0-api

Requires:	java >= 1:1.6.0
Requires:	javapackages-tools
Requires:	mvn(org.slf4j:slf4j-api)
Requires:	mvn(commons-lang:commons-lang)
Requires:	mvn(org.apache.httpcomponents:httpclient)
Requires:	mvn(org.apache.httpcomponents:httpcore)
BuildArch:	noarch


%description -n lib%{name}-java
The lib%{name}-java package contains Java bindings for %{name}.

%if 0%{?want_ruby} > 0
%package -n	ruby-%{name}
Summary:	Ruby support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	ruby(release)
BuildRequires:	ruby-devel

%description -n ruby-%{name}
The ruby-%{name} package contains Ruby bindings for %{name}.
%endif

%if 0%{?want_erlang} > 0
%package -n	erlang-%{name}
Summary:	Erlang support for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	erlang
Requires:	erlang-jsx
BuildRequires:	erlang
BuildRequires:	erlang-rebar

%description -n erlang-%{name}
The erlang-%{name} package contains Erlang bindings for %{name}.
%endif

%package -n fb303
Summary:	Basic interface for Thrift services
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n fb303
fb303 is the shared root of all Thrift services; it provides a
standard interface to monitoring, dynamic options and configuration,
uptime reports, activity, etc.

%package -n fb303-devel
Summary:	Development files for fb303
Requires:	fb303%{?_isa} = %{version}-%{release}

%description -n fb303-devel
The fb303-devel package contains header files for fb303

%package -n python-fb303
Summary:	Python bindings for fb303
Requires:	fb303%{?_isa} = %{version}-%{release}
BuildRequires:	python2-devel

%description -n python-fb303
The python-fb303 package contains Python bindings for fb303.

%package -n fb303-java
Summary:	Java bindings for fb303
Requires:	java >= 1:1.6.0
Requires:	javapackages-tools
Requires:	mvn(org.slf4j:slf4j-api)
Requires:	mvn(commons-lang:commons-lang)
Requires:	mvn(org.apache.httpcomponents:httpclient)
Requires:	mvn(org.apache.httpcomponents:httpcore)
BuildArch:	noarch

%description -n fb303-java
The fb303-java package contains Java bindings for fb303.

%global _default_patch_fuzz 2
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{?!el5:sed -i -e 's/^AC_PROG_LIBTOOL/LT_INIT/g' configure.ac}

# avoid spurious executable permissions in debuginfo package
find . -name \*.cpp -or -name \*.cc -or -name \*.h | xargs -r chmod 644

cp -p %{SOURCE2} bootstrap.sh

# work around linking issues
echo 'libthrift_c_glib_la_LIBADD = $(GLIB_LIBS) $(GOBJECT_LIBS) -L../cpp/.libs ' >> lib/c_glib/Makefile.am
echo 'libthriftqt_la_LIBADD = $(QT_LIBS) -lthrift -L.libs' >> lib/cpp/Makefile.am
echo 'libthriftz_la_LIBADD = $(ZLIB_LIBS) -lthrift -L.libs' >> lib/cpp/Makefile.am
echo 'EXTRA_libthriftqt_la_DEPENDENCIES = libthrift.la' >> lib/cpp/Makefile.am
echo 'EXTRA_libthriftz_la_DEPENDENCIES = libthrift.la' >> lib/cpp/Makefile.am

# echo 'libfb303_so_LIBADD = -lthrift -L../../../lib/cpp/.libs' >> contrib/fb303/cpp/Makefile.am

sed -i 's|libfb303_so_LDFLAGS = $(SHARED_LDFLAGS)|libfb303_so_LDFLAGS = $(SHARED_LDFLAGS) -lthrift -L../../../lib/cpp/.libs -Wl,--as-needed|g' contrib/fb303/cpp/Makefile.am

%build
export PY_PREFIX=%{_prefix}
export PERL_PREFIX=%{_prefix}
export PHP_PREFIX=%{php_extdir}
export JAVA_PREFIX=%{_javadir}
export RUBY_PREFIX=%{_prefix}
export GLIB_LIBS=$(pkg-config --libs glib-2.0)
export GLIB_CFLAGS=$(pkg-config --cflags glib-2.0)
export GOBJECT_LIBS=$(pkg-config --libs gobject-2.0)
export GOBJECT_CFLAGS=$(pkg-config --cflags gobject-2.0)

find %{_builddir} -name rebar -exec rm -f '{}' \;
find . -name Makefile\* -exec sed -i -e 's/[.][/]rebar/rebar/g' {} \;

# install javadocs in proper places
sed -i 's|-Dinstall.javadoc.path=$(DESTDIR)$(docdir)/java|-Dinstall.javadoc.path=$(DESTDIR)%{_javadocdir}/%{name}|' lib/java/Makefile.*

# build a jar without a version number
sed -i 's|${thrift.artifactid}-${version}|${thrift.artifactid}|' lib/java/build.xml

# Proper permissions for Erlang files
sed -i 's|$(INSTALL) $$p|$(INSTALL) --mode 644 $$p|g' lib/erl/Makefile.am

# Build fb303 jars against the in-situ copy of thrift
sed -i 's|$(thrift_home)/bin/thrift|../../../compiler/cpp/thrift|g' \
 contrib/fb303/cpp/Makefile.am \
 contrib/fb303/py/Makefile.am

sed -i 's|$(prefix)/lib$|%{_libdir}|g' contrib/fb303/cpp/Makefile.am

sed -i 's|$(thrift_home)/include/thrift|../../../lib/cpp/src|g' \
 contrib/fb303/cpp/Makefile.am

# Create a straightforward makefile for Java fb303
echo "all:
	ant
install: build/libfb303.jar
	mkdir -p %{buildroot}%{_javadir}
	/usr/bin/install -c -m 644 build/libfb303.jar %{buildroot}%{_javadir}
" > contrib/fb303/java/Makefile

sh ./bootstrap.sh

# use unversioned doc dirs where appropriate (via _pkgdocdir macro)
%configure --disable-dependency-tracking --disable-static --without-libevent --with-boost=/usr %{ruby_configure} %{erlang_configure} %{golang_configure} %{php_configure} --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

# eliminate unused direct shlib dependencies
sed -i -e 's/ -shared / -Wl,--as-needed\0/g' libtool

make %{?_smp_mflags}

# build fb303
(
  cd contrib/fb303
  chmod 755 bootstrap.sh
  sh bootstrap.sh
  %configure --disable-static --with-java --without-php --libdir=%{_libdir}
  make %{?_smp_mflags}
  (
      cd java
      ant dist
  )
)

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name fastbinary.so | xargs -r chmod 755
find %{buildroot} -name \*.erl -or -name \*.hrl -or -name \*.app | xargs -r chmod 644

# install man page
mkdir -p %{buildroot}%{_mandir}/man1
cp %{SOURCE3} %{buildroot}%{_mandir}/man1/thrift.1
gzip -9v %{buildroot}%{_mandir}/man1/thrift.1

# Remove javadocs jar
find %{buildroot}/%{_javadir} -name lib%{name}-javadoc.jar -exec rm -f '{}' \;

# Add POM file and depmap
mkdir -p %{buildroot}%{_mavenpomdir}

install -pm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-libthrift.pom

%add_maven_depmap JPP-libthrift.pom libthrift.jar

# Remove bundled jar files
find %{buildroot} -name \*.jar -a \! -name \*thrift\* -exec rm -f '{}' \;

# Move perl files into appropriate places
find %{buildroot} -name \*.pod -exec rm -f '{}' \;
find %{buildroot} -name .packlist -exec rm -f '{}' \;
find %{buildroot}/usr/lib/perl5 -type d -empty -delete
mkdir -p %{buildroot}/%{perl_vendorlib}/
mv %{buildroot}/usr/lib/perl5/* %{buildroot}/%{perl_vendorlib}

%if 0%{?want_php} != 0

# Move arch-independent php files into the appropriate place
mkdir -p %{buildroot}/%{_datadir}/php/
mv %{buildroot}/%{php_extdir}/Thrift %{buildroot}/%{_datadir}/php/
%endif # want_php

# Fix permissions on Thread.h
find %{buildroot} -name Thread.h -exec chmod a-x '{}' \;

# install fb303
(
  cd contrib/fb303
  make DESTDIR=%{buildroot} install
  (
    cd java
    ant -Dinstall.path=%{buildroot}%{_javadir} -Dinstall.javadoc.path=%{buildroot}%{_javadocdir}/fb303 install
  )
)

# install maven pom and depmaps for fb303
install -pm 644 %{SOURCE4} %{buildroot}%{_mavenpomdir}/JPP-libfb303.pom
%add_maven_depmap JPP-libfb303.pom libfb303.jar -f "fb303"

# Ensure all python scripts are executable
find %{buildroot} -name \*.py -exec grep -q /usr/bin/env {} \; -print | xargs -r chmod 755


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE NOTICE
%{_bindir}/thrift
%{_libdir}/*.so.*
%{_libdir}/lib*-%{version}.so
%{_mandir}/man1/thrift.1.gz

%files devel
%{_includedir}/thrift
%exclude %{_includedir}/thrift/fb303
%{_libdir}/*.so
%exclude %{_libdir}/lib*-%{version}.so
%exclude %{_libdir}/libfb303.so
%{_libdir}/pkgconfig/thrift-z.pc
%{_libdir}/pkgconfig/thrift-qt.pc
%{_libdir}/pkgconfig/thrift.pc
%{_libdir}/pkgconfig/thrift_c_glib.pc
%doc LICENSE NOTICE

%files -n perl-%{name}
%{perl_vendorlib}/Thrift
%{perl_vendorlib}/Thrift.pm
%doc LICENSE NOTICE

%if 0%{?want_php} != 0
%files -n php-%{name}
%config(noreplace) /etc/php.d/thrift_protocol.ini
%{_datadir}/php/Thrift/
%{php_extdir}/thrift_protocol.so
%doc LICENSE NOTICE
%endif

%if %{?want_erlang} > 0
%files -n erlang-%{name}
%{_libdir}/erlang/lib/%{name}-%{version}/
%doc LICENSE NOTICE
%endif

%files -n python-%{name}
%{python_sitearch}/%{name}
%{python_sitearch}/%{name}-%{version}-py%{py_version}.egg-info
%doc LICENSE NOTICE

%files -n lib%{name}-javadoc
%{_javadocdir}/%{name}
%doc LICENSE NOTICE

%files -n lib%{name}-java
%{_javadir}/lib%{name}.jar
%{_mavenpomdir}/JPP-lib%{name}.pom
%{_mavendepmapfragdir}/%{name}
%doc LICENSE NOTICE

%files -n fb303
%{_datarootdir}/fb303
%doc LICENSE NOTICE

%files -n fb303-devel
%{_libdir}/libfb303.so
%{_includedir}/thrift/fb303
%doc LICENSE NOTICE

%files -n python-fb303
%{python_sitelib}/fb303
%{python_sitelib}/fb303_scripts
%{python_sitelib}/%{name}_fb303-%{fb303_version}-py%{py_version}.egg-info
%doc LICENSE NOTICE

%files -n fb303-java
%{_javadir}/libfb303.jar
%{_mavenpomdir}/JPP-libfb303.pom
%{_mavendepmapfragdir}/thrift-fb303
%doc LICENSE NOTICE



%changelog

* Fri Dec 20 2013 willb <willb@redhat> - 0.9.1-10
- fix BZ 1045544

* Wed Oct 16 2013 willb <willb@redhat> - 0.9.1-9
- Remove spurious dependencies
- Move some versioned shared libraries from -devel

* Wed Oct 16 2013 Dan Horák <dan[at]danny.cz> - 0.9.1-8
- Mono available only on selected arches

* Sun Oct 13 2013 willb <willb@redhat> - 0.9.1-7
- minor specfile cleanups

* Fri Oct 11 2013 willb <willb@redhat> - 0.9.1-6
- added thrift man page
- integrated fb303
- fixed many fb303 library dependency problems

* Tue Oct 1 2013 willb <willb@redhat> - 0.9.1-5
- fixed extension library linking when an older thrift package is not
  already installed
- fixed extension library dependencies in Makefile

* Tue Oct 1 2013 willb <willb@redhat> - 0.9.1-4
- addresses rpmlint warnings and errors
- properly links glib, qt, and z extension libraries

* Mon Sep 30 2013 willb <willb@redhat> - 0.9.1-3
- adds QT support
- clarified multiple licensing
- uses parallel make
- removes obsolete M4 macros
- specifies canonical location for source archive

* Tue Sep 24 2013 willb <willb@redhat> - 0.9.1-2
- fixes for i686
- fixes bogus requires for Java package

* Fri Sep 20 2013 willb <willb@redhat> - 0.9.1-1
- updated to upstream version 0.9.1
- disables PHP support, which FTBFS in this version

* Fri Sep 20 2013 willb <willb@redhat> - 0.9.0-5
- patch build xml to generate unversioned jars instead of moving after the fact
- unversioned doc dirs on Fedora versions where this is appropriate
- replaced some stray hardcoded paths with macros
- thanks to Gil for the above observations and suggestions for fixes

* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-4
- removed version number from jar name (obs pmackinn)

* Thu Aug 22 2013 willb <willb@redhat> - 0.9.0-3
- Fixes for F19 and Erlang support

* Thu Aug 15 2013 willb <willb@redhat> - 0.9.0-2
- Incorporates feedback from comments on review request

* Mon Jul 1 2013 willb <willb@redhat> - 0.9.0-1
- Initial package
