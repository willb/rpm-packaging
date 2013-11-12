%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3
%global sbt_bootstrap_version 0.12.4
%global typesafe_repo http://repo.typesafe.com/typesafe/ivy-releases

Name:           sbt
Version:        0.13.0
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}.tar.gz
%if %{do_bootstrap}
# include bootstrap libraries
Source32:       %{typesafe_repo}/org.scala-sbt/ivy/%{sbt_bootstrap_version}/jars/ivy.jar
Source33:       %{typesafe_repo}/org.scala-sbt/task-system/%{sbt_bootstrap_version}/jars/task-system.jar
Source34:       %{typesafe_repo}/org.scala-sbt/compiler-interface/%{sbt_bootstrap_version}/jars/compiler-interface-src.jar
Source35:       %{typesafe_repo}/org.scala-sbt/compiler-interface/%{sbt_bootstrap_version}/jars/compiler-interface-bin.jar
Source36:       %{typesafe_repo}/org.scala-sbt/testing/%{sbt_bootstrap_version}/jars/testing.jar
Source37:       %{typesafe_repo}/org.scala-sbt/command/%{sbt_bootstrap_version}/jars/command.jar
Source38:       %{typesafe_repo}/org.scala-sbt/test-agent/%{sbt_bootstrap_version}/jars/test-agent.jar
Source39:       %{typesafe_repo}/org.scala-sbt/launcher-interface/%{sbt_bootstrap_version}/jars/launcher-interface.jar
Source40:       %{typesafe_repo}/org.scala-sbt/run/%{sbt_bootstrap_version}/jars/run.jar
Source41:       %{typesafe_repo}/org.scala-sbt/compiler-ivy-integration/%{sbt_bootstrap_version}/jars/compiler-ivy-integration.jar
Source42:       %{typesafe_repo}/org.scala-sbt/scripted-sbt/%{sbt_bootstrap_version}/jars/scripted-sbt.jar
Source43:       %{typesafe_repo}/org.scala-sbt/launch-test/%{sbt_bootstrap_version}/jars/launch-test.jar
Source44:       %{typesafe_repo}/org.scala-sbt/collections/%{sbt_bootstrap_version}/jars/collections.jar
Source45:       %{typesafe_repo}/org.scala-sbt/persist/%{sbt_bootstrap_version}/jars/persist.jar
Source46:       %{typesafe_repo}/org.scala-sbt/classfile/%{sbt_bootstrap_version}/jars/classfile.jar
Source47:       %{typesafe_repo}/org.scala-sbt/control/%{sbt_bootstrap_version}/jars/control.jar
Source48:       %{typesafe_repo}/org.scala-sbt/launcher/%{sbt_bootstrap_version}/jars/launcher.jar
Source49:       %{typesafe_repo}/org.scala-sbt/apply-macro/%{sbt_bootstrap_version}/jars/apply-macro.jar
Source50:       %{typesafe_repo}/org.scala-sbt/datatype-generator/%{sbt_bootstrap_version}/jars/datatype-generator.jar
Source51:       %{typesafe_repo}/org.scala-sbt/interface/%{sbt_bootstrap_version}/jars/interface.jar
Source52:       %{typesafe_repo}/org.scala-sbt/main-settings/%{sbt_bootstrap_version}/jars/main-settings.jar
Source53:       %{typesafe_repo}/org.scala-sbt/incremental-compiler/%{sbt_bootstrap_version}/jars/incremental-compiler.jar
Source54:       %{typesafe_repo}/org.scala-sbt/cache/%{sbt_bootstrap_version}/jars/cache.jar
Source55:       %{typesafe_repo}/org.scala-sbt/compiler-integration/%{sbt_bootstrap_version}/jars/compiler-integration.jar
Source56:       %{typesafe_repo}/org.scala-sbt/api/%{sbt_bootstrap_version}/jars/api.jar
Source57:       %{typesafe_repo}/org.scala-sbt/main/%{sbt_bootstrap_version}/jars/main.jar
Source58:       %{typesafe_repo}/org.scala-sbt/classpath/%{sbt_bootstrap_version}/jars/classpath.jar
Source59:       %{typesafe_repo}/org.scala-sbt/logging/%{sbt_bootstrap_version}/jars/logging.jar
Source60:       %{typesafe_repo}/org.scala-sbt/compile/%{sbt_bootstrap_version}/jars/compile.jar
Source61:       %{typesafe_repo}/org.scala-sbt/process/%{sbt_bootstrap_version}/jars/process.jar
Source62:       %{typesafe_repo}/org.scala-sbt/actions/%{sbt_bootstrap_version}/jars/actions.jar            
Source63:       %{typesafe_repo}/org.scala-sbt/sbt-launch/%{sbt_bootstrap_version}/jars/sbt-launch.jar
Source64:       %{typesafe_repo}/org.scala-sbt/scripted-plugin/%{sbt_bootstrap_version}/jars/scripted-plugin.jar
Source65:       %{typesafe_repo}/org.scala-sbt/tracking/%{sbt_bootstrap_version}/jars/tracking.jar
Source66:       %{typesafe_repo}/org.scala-sbt/tasks/%{sbt_bootstrap_version}/jars/tasks.jar
Source67:       %{typesafe_repo}/org.scala-sbt/completion/%{sbt_bootstrap_version}/jars/completion.jar
Source68:       %{typesafe_repo}/org.scala-sbt/cross/%{sbt_bootstrap_version}/jars/cross.jar
Source69:       %{typesafe_repo}/org.scala-sbt/relation/%{sbt_bootstrap_version}/jars/relation.jar
Source70:       %{typesafe_repo}/org.scala-sbt/io/%{sbt_bootstrap_version}/jars/io.jar
Source71:       %{typesafe_repo}/org.scala-sbt/sbt/%{sbt_bootstrap_version}/jars/sbt.jar
Source72:       %{typesafe_repo}/org.scala-sbt/scripted-framework/%{sbt_bootstrap_version}/jars/scripted-framework.jar
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
