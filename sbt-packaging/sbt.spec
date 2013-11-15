%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3
%global scala_short_version 2.10
%global sbt_bootstrap_version 0.13.0
%global sbt_major 0
%global sbt_minor 13
%global sbt_patch 1
%global sbt_build -RC2
%global sbt_short_version %{sbt_major}.%{sbt_minor}
%global sbt_version %{sbt_major}.%{sbt_minor}.%{sbt_patch}
%global sbt
%global typesafe_repo http://repo.typesafe.com/typesafe/ivy-releases
%global generic_ivy_artifact() %{1}/%{2}/%{3}/%{4}/jars/%{5}.jar

%global sbt_ivy_artifact() %{typesafe_repo}/org.scala-sbt/%{1}/%{sbt_bootstrap_version}/jars/%{1}.jar

%global sbt_ghpages_version 0.5.1
%global sbt_git_version 0.6.3
%global sbt_site_version 0.6.2

%global sxr_version 0.3.0
%global sbinary_version 0.4.2
%global scalacheck_version 1.11.0
%global specs2_version 1.12.3
%global testinterface_version 1.0

Name:           sbt
Version:        %{sbt_version}
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}%{sbt_build}.tar.gz

# sbt-ghpages plugin
Source1:        https://github.com/sbt/sbt-ghpages/archive/v%{sbt_ghpages_version}.tar.gz

# sbt-git plugin
Source2:        https://github.com/sbt/sbt-git/archive/v%{sbt_git_version}.tar.gz

# sbt-site plugin
Source3:        https://github.com/sbt/sbt-site/archive/v%{sbt_site_version}.tar.gz

# sxr
Source4:        https://github.com/harrah/browse/archive/v%{sxr_version}.tar.gz

# sbinary
Source5:        https://github.com/harrah/sbinary/archive/v%{sbinary_version}.tar.gz

# scalacheck
# nb:  no "v" in this tarball URL
Source6:	https://github.com/rickynils/scalacheck/archive/%{scalacheck_version}.tar.gz

# specs 
# nb:  no "v" in this tarball url
# nb:  this depends on scalaz; might need to excise
Source7:        https://github.com/etorreborre/specs2/archive/SPECS2-%{specs2_version}.tar.gz	
Source8:        https://github.com/sbt/test-interface/archive/v%{testinterface_version}.tar.gz

Source16:       https://raw.github.com/willb/climbing-nemesis/master/climbing-nemesis.py
Source17:       https://raw.github.com/willb/sbt-packaging/master/sbt.boot.properties

%if %{do_bootstrap}
# include bootstrap libraries

%{echo: here}

%{echo: %{sbt_ivy_artifact ivy}}

%{echo: there}

%{echo: %generic_ivy_artifact %{typesafe_repo} org.scala-sbt ivy %{sbt_bootstrap_version} ivy}

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

# sbt plugins
Source73:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-ghpages/scala_%{scala_version}/sbt_%{sbt_short_version}/%{sbt_ghpages_version}/jars/sbt-ghpages.jar
Source74:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-site/scala_%{scala_version}/sbt_%{sbt_short_version}/%{sbt_site_version}/jars/sbt-site.jar
Source75:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-git/scala_%{scala_version}/sbt_%{sbt_short_version}/%{sbt_git_version}/jars/sbt-git.jar

# sxr
Source76:	http://repo.typesafe.com/typesafe/ivy-releases/org.scala-sbt.sxr/sxr_%{scala_short_version}/%{sxr_version}/jars/sxr_%{scala_short_version}.jar

# sbinary
Source77:	http://repo.typesafe.com/typesafe/ivy-releases/org.scala-tools.sbinary/sbinary_%{scala_short_version}/%{sbinary_version}/jars/sbinary_%{scala_short_version}.jar

# scalacheck
Source78:       http://oss.sonatype.org/content/repositories/releases/org/scalacheck/scalacheck_%{scala_short_version}/%{scalacheck_version}/scalacheck_%{scala_short_version}-%{scalacheck_version}.jar

# specs
Source79:       http://oss.sonatype.org/content/repositories/releases/org/specs2/specs2_%{scala_short_version}/%{specs2_version}/specs2_%{scala_short_version}-%{specs2_version}.jar

# test-interface
Source80:       http://oss.sonatype.org/content/repositories/releases/org/scala-sbt/test-interface/%{testinterface_version}/test-interface-%{testinterface_version}.jar

# sbt launcher
Source128:       http://repo.typesafe.com/typesafe/ivy-releases/org.scala-sbt/sbt-launch/%{sbt_bootstrap_version}/sbt-launch.jar

%endif

BuildRequires:  scala
BuildRequires:	java
BuildRequires:  python

%if !%{do_bootstrap}
BuildRequires:  sbt = %{sbt_bootstrap_version}
BuildRequires:  sbt-ghpages = %{sbt_ghpages_version}
BuildRequires:  sbt-site = %{sbt_site_version}
BuildRequires:  sbt-git = %{sbt_git_version}

BuildRequires:  sxr = %{sxr_version}
BuildRequires:  sbinary = %{sbinary_version}
BuildRequires:  scalacheck = %{scalacheck_version}
BuildRequires:  specs2 = %{specs2_version}

%endif

Requires:       scala

%description
sbt is the simple build tool for Scala and Java projects.

%prep
%setup -q
cp ${SOURCE16} .
chmod 755 climbing-nemesis.py

cp ${SOURCE17} .

cp ${SOURCE128} .

./climbing-nemesis.py /usr/share/java/commons-logging.jar ivy-local commons-logging commons-logging 1.1.1
./climbing-nemesis.py /usr/share/java/commons-logging.jar ivy-local commons-logging commons-logging 1.0.4

./climbing-nemesis.py /usr/share/java/commons-httpclient.jar ivy-local commons-httpclient commons-httpclient 3.1

./climbing-nemesis.py /usr/share/java/jsoup.jar ivy-local org.jsoup jsoup 1.6.1

./climbing-nemesis.py /usr/share/java/args4j.jar ivy-local args4j args4j 2.0.16

./climbing-nemesis.py /usr/share/java/stringtemplate.jar ivy-local org.antlr stringtemplate 3.2.1

./climbing-nemesis.py /usr/share/java/httpcomponents/httpclient.jar ivy-local org.apache.httpcomponents httpclient 4.2.1

./climbing-nemesis.py /usr/share/java/httpcomponents/httpclient.jar ivy-local org.apache.httpcomponents httpclient 4.1.3

./climbing-nemesis.py /usr/share/java/httpcomponents/httpcore.jar ivy-local org.apache.httpcomponents httpcore 4.1.4

./climbing-nemesis.py /usr/share/java/antlr.jar ivy-local antlr antlr 2.7.7

./climbing-nemesis.py /usr/share/java/jsch.jar ivy-local com.jcraft jsch 0.1.48

./climbing-nemesis.py /usr/share/java/tomcat-servlet-3.0-api.jar ivy-local javax.servlet servlet-api 3.0

for subpackage in continuation http io security server servlet webapp util xml ; do
    ./climbing-nemesis.py /usr/share/java/jetty/jetty-$subpackage.jar ivy-local org.eclipse.jetty jetty-$subpackage 8.1.5
done

./climbing-nemesis.py /usr/share/scala/lib/scala-library.jar ivy-local org.scala-lang scala-library %{scala_version}

./climbing-nemesis.py /usr/share/scala/lib/scala-compiler.jar ivy-local org.scala-lang scala-compiler %{scala_version}

./climbing-nemesis.py /usr/share/java/jna.jar ivy-local net.java.dev.jna jna 3.2.3 # we are fibbing about this version number

# both of these are fake (F18 ships 1.6)
./climbing-nemesis.py /usr/share/java/commons-codec.jar ivy-local commons-codec commons-codec 1.4
./climbing-nemesis.py /usr/share/java/commons-codec.jar ivy-local commons-codec commons-codec 1.2

./climbing-nemesis.py /usr/share/java/jline.jar ivy-local jline jline 1.0

# this is bogus (f18 ships 2.2)
./climbing-nemesis.py /usr/share/java/ivy.jar ivy-local org.apache.ivy ivy 2.3.0
./climbing-nemesis.py /usr/share/java/ivy.jar ivy-local org.apache.ivy ivy 2.2.0

%if %{do_bootstrap}
./climbing-nemesis.py ${SOURCE32} ivy-local org.scala-sbt ivy %{sbt_version}
./climbing-nemesis.py ${SOURCE33} ivy-local org.scala-sbt task-system %{sbt_version}
./climbing-nemesis.py ${SOURCE34} ivy-local org.scala-sbt compiler-interface-src %{sbt_version}
./climbing-nemesis.py ${SOURCE35} ivy-local org.scala-sbt compiler-interface-bin %{sbt_version}
./climbing-nemesis.py ${SOURCE36} ivy-local org.scala-sbt testing %{sbt_version}
./climbing-nemesis.py ${SOURCE37} ivy-local org.scala-sbt command %{sbt_version}
./climbing-nemesis.py ${SOURCE38} ivy-local org.scala-sbt test-agent %{sbt_version}
./climbing-nemesis.py ${SOURCE39} ivy-local org.scala-sbt launcher-interface %{sbt_version}
./climbing-nemesis.py ${SOURCE40} ivy-local org.scala-sbt run %{sbt_version}
./climbing-nemesis.py ${SOURCE41} ivy-local org.scala-sbt compiler-ivy-integration %{sbt_version}
./climbing-nemesis.py ${SOURCE42} ivy-local org.scala-sbt scripted-sbt %{sbt_version}
./climbing-nemesis.py ${SOURCE43} ivy-local org.scala-sbt launch-test %{sbt_version}
./climbing-nemesis.py ${SOURCE44} ivy-local org.scala-sbt collections %{sbt_version}
./climbing-nemesis.py ${SOURCE45} ivy-local org.scala-sbt persist %{sbt_version}
./climbing-nemesis.py ${SOURCE46} ivy-local org.scala-sbt classfile %{sbt_version}
./climbing-nemesis.py ${SOURCE47} ivy-local org.scala-sbt control %{sbt_version}
./climbing-nemesis.py ${SOURCE48} ivy-local org.scala-sbt launcher %{sbt_version}
./climbing-nemesis.py ${SOURCE49} ivy-local org.scala-sbt apply-macro %{sbt_version}
./climbing-nemesis.py ${SOURCE50} ivy-local org.scala-sbt datatype-generator %{sbt_version}
./climbing-nemesis.py ${SOURCE51} ivy-local org.scala-sbt interface %{sbt_version}
./climbing-nemesis.py ${SOURCE52} ivy-local org.scala-sbt main-settings %{sbt_version}
./climbing-nemesis.py ${SOURCE53} ivy-local org.scala-sbt incremental-compiler %{sbt_version}
./climbing-nemesis.py ${SOURCE54} ivy-local org.scala-sbt cache %{sbt_version}
./climbing-nemesis.py ${SOURCE55} ivy-local org.scala-sbt compiler-integration %{sbt_version}
./climbing-nemesis.py ${SOURCE56} ivy-local org.scala-sbt api %{sbt_version}
./climbing-nemesis.py ${SOURCE57} ivy-local org.scala-sbt main %{sbt_version}
./climbing-nemesis.py ${SOURCE58} ivy-local org.scala-sbt classpath %{sbt_version}
./climbing-nemesis.py ${SOURCE59} ivy-local org.scala-sbt logging %{sbt_version}
./climbing-nemesis.py ${SOURCE60} ivy-local org.scala-sbt compile %{sbt_version}
./climbing-nemesis.py ${SOURCE61} ivy-local org.scala-sbt process %{sbt_version}
./climbing-nemesis.py ${SOURCE62} ivy-local org.scala-sbt actions %{sbt_version}
./climbing-nemesis.py ${SOURCE63} ivy-local org.scala-sbt sbt-launch %{sbt_version}
./climbing-nemesis.py ${SOURCE64} ivy-local org.scala-sbt scripted-plugin %{sbt_version}
./climbing-nemesis.py ${SOURCE65} ivy-local org.scala-sbt tracking %{sbt_version}
./climbing-nemesis.py ${SOURCE66} ivy-local org.scala-sbt tasks %{sbt_version}
./climbing-nemesis.py ${SOURCE67} ivy-local org.scala-sbt completion %{sbt_version}
./climbing-nemesis.py ${SOURCE68} ivy-local org.scala-sbt cross %{sbt_version}
./climbing-nemesis.py ${SOURCE69} ivy-local org.scala-sbt relation %{sbt_version}
./climbing-nemesis.py ${SOURCE70} ivy-local org.scala-sbt io %{sbt_version}
./climbing-nemesis.py ${SOURCE71} ivy-local org.scala-sbt sbt %{sbt_version}
./climbing-nemesis.py ${SOURCE72} ivy-local org.scala-sbt scripted-framework %{sbt_version}

# plugins

./climbing-nemesis.py ${SOURCE73} ivy-local com.typesafe.sbt sbt-ghpages %{sbt_ghpages_version} --meta e:scalaVersion=%{scala_version} --meta e:sbtVersion=%{sbt_short_version}
./climbing-nemesis.py ${SOURCE74} ivy-local com.typesafe.sbt sbt-site %{sbt_site_version} --meta e:scalaVersion=%{scala_version} --meta e:sbtVersion=%{sbt_short_version}
./climbing-nemesis.py ${SOURCE75} ivy-local com.typesafe.sbt sbt-git %{sbt_git_version} --meta e:scalaVersion=%{scala_version} --meta e:sbtVersion=%{sbt_short_version}

# SXR
./climbing-nemesis.py ${SOURCE76} ivy-local org.scala-tools.sxr sxr %{sxr_version}

# sbinary
./climbing-nemesis.py ${SOURCE77} ivy-local org.scala-tools.sbinary sbinary %{sbinary_version}

# scalacheck
./climbing-nemesis.py ${SOURCE78} ivy-local org.scalacheck scalacheck %{scalacheck_version}

# specs2
./climbing-nemesis.py ${SOURCE79} ivy-local org.specs2 specs2 %{specs2_version}

# test-interface
./climbing-nemesis.py ${SOURCE80} ivy-local org.scala-sbt test-interface %{testinterface_version}

%else
# If we aren't bootstrapping, copy installed jars into local ivy cache
# dir.  It sure would be nice if we could resolve these via Ivy from
# installed packages.  This is a FIXME for now, though.

%endif


%build
java -Xms512M -Xmx1536M -Xss1M -XX:+CMSClassUnloadingEnabled -jar -Dsbt.boot.properties=sbt.boot.properties sbt-launch.jar

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
* Thu Nov 7 2013 William Benton <willb@redhat.com> - 0.13.0-1
- initial package
