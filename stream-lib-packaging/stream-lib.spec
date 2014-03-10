%global streamlib_version 2.6.0
%global commit 214c92595d5be3a1cedc881b50231ccb34862074
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           stream-lib
Version:        %{streamlib_version}
Release:        1%{?dist}
Summary:        Stream summarizer and cardinality estimator
License:        ASL 2.0
URL:            https://github.com/addthis/stream-lib/
Source0:        https://github.com/addthis/stream-lib/archive/%{commit}/stream-lib-%{commit}.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(it.unimi.dsi:fastutil)

%description

A Java library for summarizing data in streams for which it is
infeasible to store all events. More specifically, there are classes
for estimating: cardinality (i.e. counting things); set membership;
top-k elements and frequency. One particularly useful feature is that
cardinality estimators with compatible configurations may be safely
merged.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
This package provides %{summary}.

%prep
%setup -qn %{name}-%{commit}

%pom_remove_plugin org.apache.maven.plugins:maven-shade-plugin pom.xml


%build
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.mdown
%doc LICENSE.txt
%dir %{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Mar 10 2014 William Benton <willb@redhat.com> - 2.6.0-1
- Initial packaging
