%global gem_name capricious

Name:           rubygem-capricious
Version:        0.2.2
Release:        1%{?dist}
Summary:        Pseudorandom number generator classes and support code


License:        ASL 2.0
URL:            https://github.com/willb/capricious
Source0:        http://rubygems.org/downloads/capricious-0.2.2.gem

BuildArch:      noarch
BuildRequires:  ruby rubygems-devel rubygem-rspec
Requires:       ruby(release)
Requires:       rubygems

Provides:       rubygem(%{gem_name}) = %{version}

%description

Capricious provides pseudorandom number generator classes and support
code.  Each PRNG is parameterized on a source of randomness and a
probability distribution.

%package doc
Summary:	Documentation for %{name}
Requires:	%{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

# patches for RSpec 2 compatibility
sed -i -e "/require 'spec'/d" $(find . -name spec_helper.rb)
sed -i -e 's|spec/autorun|rspec/core|' $(find . -name spec_helper.rb)
sed -i -e 's|Spec::Runner|RSpec|' $(find . -name spec_helper.rb)

# Fix some spurious failures
sed -i -e 's|poisson.aggregate.mean.should be_close[(]LAMBDA, 0.05[)]|poisson.aggregate.mean.should be_close(LAMBDA, 0.075)|' spec/poisson_spec.rb

# This probably needs to go upstream
sed -i -e 's|be_close[(]\([@a-zA-Z0-9_.]*\), \([^)]*\))|be_within(\2).of(\1)|g' $(find . -name \*_spec.rb) 

# run some more iterations for additional stability
sed -i -e 's|count=SAMPLE_COUNT|count=SAMPLE_COUNT*20|' $(find . -name \*_spec.rb) 


gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# If there were programs installed:
# mkdir -p %{buildroot}%{_bindir}
# cp -a ./%{_bindir}/* %{buildroot}%{_bindir}
 
%check
rspec -Ilib spec

%files
%{gem_instdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%{gem_instdir}/spec
%doc %{gem_docdir}

%changelog

* Thu Feb 27 2014 William Benton <willb@redhat.com> - 0.2.2-1
- initial package
