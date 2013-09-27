Name:           java-diffutils
Version:        1.3.0
Release:        2%{?dist}
Summary:        The DiffUtils library for computing diffs, applying patches, generating side-by-side view in Java.
License:        ASL 2.0
%{?el5:Group:          Development/Libraries}
URL:            http://code.google.com/p/java-diff-utils/
# svn export http://java-diff-utils.googlecode.com/svn/branches/%{version} %{name}-%{version} ; tar -czvf %{name}-%{version}.tar.gz %{name}-%{version}
Source0:        %{name}-%{version}.tar.gz
Source1:        http://www.apache.org/licenses/LICENSE-2.0
BuildArch:      noarch

BuildRequires:  maven-local

%description
java-diffutils is the DiffUtils library for computing diffs, applying
patches, and generating side-by-side view in Java.

%package javadoc
Summary:        API documentation for %{name}
%{?el5:Group:          Documentation}

%description javadoc
This package provides %{summary}.

%prep
%setup -q
cp %{SOURCE1} LICENSE

%build
%mvn_file com.googlecode.java-diff-utils:diffutils diffutils
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Sep 27 2013 William Benton <willb@redhat.com> - 1.3.0-2
- Incorporated suggestions from Gil

* Fri Sep 27 2013 William Benton <willb@redhat.com> - 1.3.0-1
- Initial package
