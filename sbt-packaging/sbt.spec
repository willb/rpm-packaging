%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3
%global sbt_bootstrap_version 0.12.4
%global typesafe_repo http://repo.typesafe.com/typesafe/ivy-releases
%global generic_ivy_artifact() %{1}/%{2}/%{3}/%{4}/jars/%{5}.jar
%global sbt_ivy_artifact() %generic_ivy_artifact %{typesafe_repo} org.scala-sbt %{1} %{sbt_bootstrap_version} %{1}

Name:           sbt
Version:        0.13.0
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}.tar.gz

%if %{do_bootstrap}
# include bootstrap libraries
Source32:       %sbt_ivy_artifact ivy 
Source33:       %sbt_ivy_artifact task-system 
Source34:       %generic_ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-src
Source35:       %generic_ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-bin
Source36:       %sbt_ivy_artifact testing 
Source37:       %sbt_ivy_artifact command 
Source38:       %sbt_ivy_artifact test-agent 
Source39:       %sbt_ivy_artifact launcher-interface 
Source40:       %sbt_ivy_artifact run 
Source41:       %sbt_ivy_artifact compiler-ivy-integration 
Source42:       %sbt_ivy_artifact scripted-sbt 
Source43:       %sbt_ivy_artifact launch-test 
Source44:       %sbt_ivy_artifact collections 
Source45:       %sbt_ivy_artifact persist 
Source46:       %sbt_ivy_artifact classfile 
Source47:       %sbt_ivy_artifact control 
Source48:       %sbt_ivy_artifact launcher 
Source49:       %sbt_ivy_artifact apply-macro 
Source50:       %sbt_ivy_artifact datatype-generator 
Source51:       %sbt_ivy_artifact interface 
Source52:       %sbt_ivy_artifact main-settings 
Source53:       %sbt_ivy_artifact incremental-compiler 
Source54:       %sbt_ivy_artifact cache 
Source55:       %sbt_ivy_artifact compiler-integration 
Source56:       %sbt_ivy_artifact api 
Source57:       %sbt_ivy_artifact main 
Source58:       %sbt_ivy_artifact classpath 
Source59:       %sbt_ivy_artifact logging 
Source60:       %sbt_ivy_artifact compile 
Source61:       %sbt_ivy_artifact process 
Source62:       %sbt_ivy_artifact actions
Source63:       %sbt_ivy_artifact sbt-launch 
Source64:       %sbt_ivy_artifact scripted-plugin 
Source65:       %sbt_ivy_artifact tracking 
Source66:       %sbt_ivy_artifact tasks 
Source67:       %sbt_ivy_artifact completion 
Source68:       %sbt_ivy_artifact cross 
Source69:       %sbt_ivy_artifact relation 
Source70:       %sbt_ivy_artifact io 
Source71:       %sbt_ivy_artifact sbt 
Source72:       %sbt_ivy_artifact scripted-framework 
%endif

BuildRequires:  scala
%if !%{do_bootstrap}
BuildRequires:  sbt = %{sbt_bootstrap_version}
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
%{_javadir}/sbt/ivy.jar
%{_javadir}/sbt/task-system.jar
%{_javadir}/sbt/compiler-interface-src.jar
%{_javadir}/sbt/compiler-interface-bin.jar
%{_javadir}/sbt/testing.jar
%{_javadir}/sbt/command.jar
%{_javadir}/sbt/test-agent.jar
%{_javadir}/sbt/launcher-interface.jar
%{_javadir}/sbt/run.jar
%{_javadir}/sbt/compiler-ivy-integration.jar
%{_javadir}/sbt/scripted-sbt.jar
%{_javadir}/sbt/launch-test.jar
%{_javadir}/sbt/collections.jar
%{_javadir}/sbt/persist.jar
%{_javadir}/sbt/classfile.jar
%{_javadir}/sbt/control.jar
%{_javadir}/sbt/launcher.jar
%{_javadir}/sbt/apply-macro.jar
%{_javadir}/sbt/datatype-generator.jar
%{_javadir}/sbt/interface.jar
%{_javadir}/sbt/main-settings.jar
%{_javadir}/sbt/incremental-compiler.jar
%{_javadir}/sbt/cache.jar
%{_javadir}/sbt/compiler-integration.jar
%{_javadir}/sbt/api.jar
%{_javadir}/sbt/main.jar
%{_javadir}/sbt/classpath.jar
%{_javadir}/sbt/logging.jar
%{_javadir}/sbt/compile.jar
%{_javadir}/sbt/process.jar
%{_javadir}/sbt/actions.jar
%{_javadir}/sbt/sbt-launch.jar
%{_javadir}/sbt/scripted-plugin.jar
%{_javadir}/sbt/tracking.jar
%{_javadir}/sbt/tasks.jar
%{_javadir}/sbt/completion.jar
%{_javadir}/sbt/cross.jar
%{_javadir}/sbt/relation.jar
%{_javadir}/sbt/io.jar
%{_javadir}/sbt/sbt.jar
%{_javadir}/sbt/scripted-framework.jar
%doc README.md LICENSE NOTICE



%changelog
