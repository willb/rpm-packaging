%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3
%global sbt_bootstrap_version 0.12.4
%global typesafe_repo http://repo.typesafe.com/typesafe/ivy-releases
%global ivy_artifact() %{1}/%{2}/%{3}/%{4}/jars/%{3}.jar

Name:           sbt
Version:        0.13.0
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}.tar.gz
%if %{do_bootstrap}
# include bootstrap libraries
Source32:       %ivy_artifact %{typesafe_repo} org.scala-sbt ivy %{sbt_bootstrap_version}.jar
Source33:       %ivy_artifact %{typesafe_repo} org.scala-sbt task-system %{sbt_bootstrap_version}.jar
Source34:       %ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version}-src.jar
Source35:       %ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version}-bin.jar
Source36:       %ivy_artifact %{typesafe_repo} org.scala-sbt testing %{sbt_bootstrap_version}.jar
Source37:       %ivy_artifact %{typesafe_repo} org.scala-sbt command %{sbt_bootstrap_version}.jar
Source38:       %ivy_artifact %{typesafe_repo} org.scala-sbt test-agent %{sbt_bootstrap_version}.jar
Source39:       %ivy_artifact %{typesafe_repo} org.scala-sbt launcher-interface %{sbt_bootstrap_version}.jar
Source40:       %ivy_artifact %{typesafe_repo} org.scala-sbt run %{sbt_bootstrap_version}.jar
Source41:       %ivy_artifact %{typesafe_repo} org.scala-sbt compiler-ivy-integration %{sbt_bootstrap_version}.jar
Source42:       %ivy_artifact %{typesafe_repo} org.scala-sbt scripted-sbt %{sbt_bootstrap_version}.jar
Source43:       %ivy_artifact %{typesafe_repo} org.scala-sbt launch-test %{sbt_bootstrap_version}.jar
Source44:       %ivy_artifact %{typesafe_repo} org.scala-sbt collections %{sbt_bootstrap_version}.jar
Source45:       %ivy_artifact %{typesafe_repo} org.scala-sbt persist %{sbt_bootstrap_version}.jar
Source46:       %ivy_artifact %{typesafe_repo} org.scala-sbt classfile %{sbt_bootstrap_version}.jar
Source47:       %ivy_artifact %{typesafe_repo} org.scala-sbt control %{sbt_bootstrap_version}.jar
Source48:       %ivy_artifact %{typesafe_repo} org.scala-sbt launcher %{sbt_bootstrap_version}.jar
Source49:       %ivy_artifact %{typesafe_repo} org.scala-sbt apply-macro %{sbt_bootstrap_version}.jar
Source50:       %ivy_artifact %{typesafe_repo} org.scala-sbt datatype-generator %{sbt_bootstrap_version}.jar
Source51:       %ivy_artifact %{typesafe_repo} org.scala-sbt interface %{sbt_bootstrap_version}.jar
Source52:       %ivy_artifact %{typesafe_repo} org.scala-sbt main-settings %{sbt_bootstrap_version}.jar
Source53:       %ivy_artifact %{typesafe_repo} org.scala-sbt incremental-compiler %{sbt_bootstrap_version}.jar
Source54:       %ivy_artifact %{typesafe_repo} org.scala-sbt cache %{sbt_bootstrap_version}.jar
Source55:       %ivy_artifact %{typesafe_repo} org.scala-sbt compiler-integration %{sbt_bootstrap_version}.jar
Source56:       %ivy_artifact %{typesafe_repo} org.scala-sbt api %{sbt_bootstrap_version}.jar
Source57:       %ivy_artifact %{typesafe_repo} org.scala-sbt main %{sbt_bootstrap_version}.jar
Source58:       %ivy_artifact %{typesafe_repo} org.scala-sbt classpath %{sbt_bootstrap_version}.jar
Source59:       %ivy_artifact %{typesafe_repo} org.scala-sbt logging %{sbt_bootstrap_version}.jar
Source60:       %ivy_artifact %{typesafe_repo} org.scala-sbt compile %{sbt_bootstrap_version}.jar
Source61:       %ivy_artifact %{typesafe_repo} org.scala-sbt process %{sbt_bootstrap_version}.jar
Source62:       %ivy_artifact %{typesafe_repo} org.scala-sbt actions %{sbt_bootstrap_version}.jar            
Source63:       %ivy_artifact %{typesafe_repo} org.scala-sbt sbt-launch %{sbt_bootstrap_version}.jar
Source64:       %ivy_artifact %{typesafe_repo} org.scala-sbt scripted-plugin %{sbt_bootstrap_version}.jar
Source65:       %ivy_artifact %{typesafe_repo} org.scala-sbt tracking %{sbt_bootstrap_version}.jar
Source66:       %ivy_artifact %{typesafe_repo} org.scala-sbt tasks %{sbt_bootstrap_version}.jar
Source67:       %ivy_artifact %{typesafe_repo} org.scala-sbt completion %{sbt_bootstrap_version}.jar
Source68:       %ivy_artifact %{typesafe_repo} org.scala-sbt cross %{sbt_bootstrap_version}.jar
Source69:       %ivy_artifact %{typesafe_repo} org.scala-sbt relation %{sbt_bootstrap_version}.jar
Source70:       %ivy_artifact %{typesafe_repo} org.scala-sbt io %{sbt_bootstrap_version}.jar
Source71:       %ivy_artifact %{typesafe_repo} org.scala-sbt sbt %{sbt_bootstrap_version}.jar
Source72:       %ivy_artifact %{typesafe_repo} org.scala-sbt scripted-framework %{sbt_bootstrap_version}.jar
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
