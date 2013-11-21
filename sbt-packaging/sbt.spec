%global do_bootstrap 1
%global pkg_rel 1
%global scala_version 2.10.3
%global scala_short_version 2.10
%global sbt_bootstrap_version 0.13.1-RC3
%global sbt_major 0
%global sbt_minor 13
%global sbt_patch 1
%global sbt_build -RC3
%global sbt_short_version %{sbt_major}.%{sbt_minor}
%global sbt_version %{sbt_major}.%{sbt_minor}.%{sbt_patch}
%global typesafe_repo http://repo.typesafe.com/typesafe/ivy-releases

%global generic_ivy_artifact() %{1}/%{2}/%{3}/%{4}/jars/%{5}.jar
%global generic_ivy_descriptor() %{1}/%{2}/%{3}/%{4}/ivys/ivy.xml#/%{5}-%{4}-ivy.xml

%global sbt_ivy_artifact() %{typesafe_repo}/org.scala-sbt/%{1}/%{sbt_bootstrap_version}/jars/%{1}.jar
%global sbt_ivy_descriptor() %{typesafe_repo}/org.scala-sbt/%{1}/%{sbt_bootstrap_version}/ivys/ivy.xml#/%{1}-%{sbt_bootstrap_version}-ivy.xml

%global sbt_ghpages_version 0.5.1
%global sbt_git_version 0.6.3
%global sbt_site_version 0.7.0-M1
%global sbt_site_jar_version 0.7.1

%global sxr_version 0.3.0
%global sbinary_version 0.4.2
%global scalacheck_version 1.11.0
%global specs2_version 1.12.3
%global testinterface_version 1.0
%global dispatch_http_version 0.8.9

Name:           sbt
Version:        %{sbt_version}
Release:        %{pkg_rel}%{?dist}
Summary:        simple build tool for Scala and Java projects

License:        BSD
URL:            http://www.scala-sbt.org
Source0:        https://github.com/sbt/sbt/archive/v%{version}%{sbt_build}.tar.gz

Patch0:         sbt-scala-0.13.1-RC3.patch 

# sbt-ghpages plugin
Source1:        https://github.com/sbt/sbt-ghpages/archive/v%{sbt_ghpages_version}.tar.gz

# sbt-git plugin
Source2:        https://github.com/sbt/sbt-git/archive/v%{sbt_git_version}.tar.gz

# sbt-site plugin
Source3:        https://github.com/sbt/sbt-site/archive/%{sbt_site_version}.tar.gz

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

# Ivy POM
Source18:       http://repo1.maven.org/maven2/org/apache/ivy/ivy/2.3.0/ivy-2.3.0.pom


%if %{do_bootstrap}
# include bootstrap libraries

Source32:       %sbt_ivy_artifact ivy 

Source132:      %sbt_ivy_descriptor ivy

Source33:       %sbt_ivy_artifact task-system 

Source133:      %sbt_ivy_descriptor task-system

Source34:       %generic_ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-src

Source134:      %generic_ivy_descriptor %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-src

Source35:       %generic_ivy_artifact %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-bin

Source135:       %generic_ivy_descriptor %{typesafe_repo} org.scala-sbt compiler-interface %{sbt_bootstrap_version} compiler-interface-bin

Source36:       %sbt_ivy_artifact testing 

Source136:      %sbt_ivy_descriptor testing

Source37:       %sbt_ivy_artifact command 

Source137:      %sbt_ivy_descriptor command

Source38:       %sbt_ivy_artifact test-agent 

Source138:      %sbt_ivy_descriptor test-agent

Source39:       %sbt_ivy_artifact launcher-interface 

Source139:      %sbt_ivy_descriptor launcher-interface

Source40:       %sbt_ivy_artifact run 

Source140:      %sbt_ivy_descriptor run

Source41:       %sbt_ivy_artifact compiler-ivy-integration 

Source141:      %sbt_ivy_descriptor compiler-ivy-integration

Source42:       %sbt_ivy_artifact scripted-sbt 

Source142:      %sbt_ivy_descriptor scripted-sbt

Source43:       %sbt_ivy_artifact launch-test 

Source143:      %sbt_ivy_descriptor launch-test

Source44:       %sbt_ivy_artifact collections 

Source144:      %sbt_ivy_descriptor collections

Source45:       %sbt_ivy_artifact persist 

Source145:      %sbt_ivy_descriptor persist

Source46:       %sbt_ivy_artifact classfile 

Source146:      %sbt_ivy_descriptor classfile

Source47:       %sbt_ivy_artifact control 

Source147:      %sbt_ivy_descriptor control

Source48:       %sbt_ivy_artifact launcher 

Source148:      %sbt_ivy_descriptor launcher

Source49:       %sbt_ivy_artifact apply-macro 

Source149:      %sbt_ivy_descriptor apply-macro

Source50:       %sbt_ivy_artifact datatype-generator 

Source150:      %sbt_ivy_descriptor datatype-generator

Source51:       %sbt_ivy_artifact interface 

Source151:      %sbt_ivy_descriptor interface

Source52:       %sbt_ivy_artifact main-settings 

Source152:      %sbt_ivy_descriptor main-settings

Source53:       %sbt_ivy_artifact incremental-compiler 

Source153:      %sbt_ivy_descriptor incremental-compiler

Source54:       %sbt_ivy_artifact cache 

Source154:      %sbt_ivy_descriptor cache

Source55:       %sbt_ivy_artifact compiler-integration 

Source155:      %sbt_ivy_descriptor compiler-integration

Source56:       %sbt_ivy_artifact api 

Source156:      %sbt_ivy_descriptor api

Source57:       %sbt_ivy_artifact main 

Source157:      %sbt_ivy_descriptor main

Source58:       %sbt_ivy_artifact classpath 

Source158:      %sbt_ivy_descriptor classpath

Source59:       %sbt_ivy_artifact logging 

Source159:      %sbt_ivy_descriptor logging

Source60:       %sbt_ivy_artifact compile 

Source160:      %sbt_ivy_descriptor compile

Source61:       %sbt_ivy_artifact process 

Source161:      %sbt_ivy_descriptor process

Source62:       %sbt_ivy_artifact actions

Source63:       %sbt_ivy_artifact sbt-launch 

Source163:      %sbt_ivy_descriptor sbt-launch

Source64:       %sbt_ivy_artifact scripted-plugin 

Source164:      %sbt_ivy_descriptor scripted-plugin

Source65:       %sbt_ivy_artifact tracking 

Source165:      %sbt_ivy_descriptor tracking

Source66:       %sbt_ivy_artifact tasks 

Source166:      %sbt_ivy_descriptor tasks

Source67:       %sbt_ivy_artifact completion 

Source167:      %sbt_ivy_descriptor completion

Source68:       %sbt_ivy_artifact cross 

Source168:      %sbt_ivy_descriptor cross

Source69:       %sbt_ivy_artifact relation 

Source169:      %sbt_ivy_descriptor relation

Source70:       %sbt_ivy_artifact io 

Source170:      %sbt_ivy_descriptor io

Source71:       %sbt_ivy_artifact sbt 

Source171:      %sbt_ivy_descriptor sbt

Source72:       %sbt_ivy_artifact scripted-framework 

Source172:      %sbt_ivy_descriptor scripted-framework

# sbt plugins
Source73:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-ghpages/scala_%{scala_short_version}/sbt_%{sbt_short_version}/%{sbt_ghpages_version}/jars/sbt-ghpages.jar
Source74:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-site/scala_%{scala_short_version}/sbt_%{sbt_short_version}/%{sbt_site_jar_version}/jars/sbt-site.jar
Source75:       http://scalasbt.artifactoryonline.com/scalasbt/sbt-plugin-releases/com.typesafe.sbt/sbt-git/scala_%{scala_short_version}/sbt_%{sbt_short_version}/%{sbt_git_version}/jars/sbt-git.jar

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

# dispatch-http
Source81:       http://oss.sonatype.org/content/repositories/releases/net/databinder/dispatch-http_%{scala_short_version}/%{dispatch_http_version}/dispatch-http_%{scala_short_version}-%{dispatch_http_version}.jar

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
%setup -q -n %{name}-%{sbt_version}%{sbt_build}

%patch0 -p1

cp %{SOURCE16} .
chmod 755 climbing-nemesis.py

cp %{SOURCE17} .

cp %{SOURCE128} .

sed -i -e 's/0.7.1/0.6.2/g' project/p.sbt
sed -i -e 's/FEDORA_SCALA_VERSION/%{scala_version}/g' sbt.boot.properties
sed -i -e 's/["]2[.]10[.]2["]/\"2.10.3\"/g' $(find . -name \*.sbt) $(find . -name \*.xml)
sed -i -e 's/["]2[.]10[.]2-RC2["]/\"2.10.3\"/g' $(find . -name \*.sbt)

sed -i -e 's/0.13.0/%{sbt_bootstrap_version}/g' project/build.properties

./climbing-nemesis.py commons-logging commons-logging ivy-local --version 1.1.1
./climbing-nemesis.py commons-logging commons-logging ivy-local --version 1.0.4

./climbing-nemesis.py commons-httpclient commons-httpclient ivy-local --version 3.1

./climbing-nemesis.py org.jsoup jsoup ivy-local --version 1.7.1

./climbing-nemesis.py args4j args4j ivy-local --version 2.0.16

./climbing-nemesis.py org.antlr stringtemplate ivy-local --version 3.2.1

# NB:  omit the --jarfile here once we can get climbing-nemesis to work in these cases
./climbing-nemesis.py org.apache.httpcomponents httpclient ivy-local --version 4.2.1 --jarfile %{_javadir}/httpcomponents/httpclient.jar 
./climbing-nemesis.py org.apache.httpcomponents httpclient ivy-local --version 4.1.3 --jarfile %{_javadir}/httpcomponents/httpclient.jar

./climbing-nemesis.py org.apache.httpcomponents httpcore ivy-local --version 4.1.4 --jarfile %{_javadir}/httpcomponents/httpcore.jar

./climbing-nemesis.py antlr antlr ivy-local --version 2.7.7

./climbing-nemesis.py com.jcraft jsch ivy-local --version 0.1.4841

./climbing-nemesis.py javax.servlet servlet-api ivy-local --version 3.0

for subpackage in continuation http io security server servlet webapp util xml ; do
    ./climbing-nemesis.py org.eclipse.jetty jetty-$subpackage ivy-local --version 8.1.5 --jarfile %{_javadir}/jetty/jetty-${subpackage}.jar
done

# scala compiler; nb; we may need to treat the compiler specially to remove the spurious jline dependency
./climbing-nemesis.py org.scala-lang scala-library ivy-local --version %{scala_version}
./climbing-nemesis.py org.scala-lang scala-compiler ivy-local --version %{scala_version}
./climbing-nemesis.py org.scala-lang scala-reflect ivy-local --version %{scala_version}

./climbing-nemesis.py net.java.dev.jna jna ivy-local --version 3.2.3 # we are fibbing about this version number

# both of these are fake (F18 ships 1.6)
./climbing-nemesis.py commons-codec commons-codec ivy-local --version 1.4
./climbing-nemesis.py commons-codec commons-codec ivy-local --version 1.2

./climbing-nemesis.py jline jline ivy-local --version 2.10 --jarfile %{_javadir}/jline2-2.10.jar
./climbing-nemesis.py org.fusesource.jansi jansi ivy-local --version 1.9

# this is bogus (f18 ships 2.2; f19 ships 2.3)
./climbing-nemesis.py org.apache.ivy ivy ivy-local --version 2.3.0 --pomfile %{SOURCE18} --jarfile %{_javadir}/ivy.jar
./climbing-nemesis.py org.apache.ivy ivy ivy-local --version 2.2.0 --pomfile %{SOURCE18} --jarfile %{_javadir}/ivy.jar

%if %{do_bootstrap}
./climbing-nemesis.py --jarfile %{SOURCE32} --ivyfile %{SOURCE132} org.scala-sbt ivy ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE33} --ivyfile %{SOURCE133} org.scala-sbt task-system ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE34} --ivyfile %{SOURCE134} org.scala-sbt compiler-interface-src ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE35} --ivyfile %{SOURCE135} org.scala-sbt compiler-interface-bin ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE36} --ivyfile %{SOURCE136} org.scala-sbt testing ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE37} --ivyfile %{SOURCE137} org.scala-sbt command ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE38} --ivyfile %{SOURCE138} org.scala-sbt test-agent ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE39} --ivyfile %{SOURCE139} org.scala-sbt launcher-interface ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE40} --ivyfile %{SOURCE140} org.scala-sbt run ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE41} --ivyfile %{SOURCE141} org.scala-sbt compiler-ivy-integration ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE42} --ivyfile %{SOURCE142} org.scala-sbt scripted-sbt ivy-local --version %{sbt_bootstrap_version}
# ./climbing-nemesis.py --jarfile %{SOURCE43} --ivyfile %{SOURCE143} org.scala-sbt launch-test ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE44} --ivyfile %{SOURCE144} org.scala-sbt collections ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE45} --ivyfile %{SOURCE145} org.scala-sbt persist ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE46} --ivyfile %{SOURCE146} org.scala-sbt classfile ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE47} --ivyfile %{SOURCE147} org.scala-sbt control ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE48} --ivyfile %{SOURCE148} org.scala-sbt launcher ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE49} --ivyfile %{SOURCE149} org.scala-sbt apply-macro ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE50} --ivyfile %{SOURCE150} org.scala-sbt datatype-generator ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE51} --ivyfile %{SOURCE151} org.scala-sbt interface ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE52} --ivyfile %{SOURCE152} org.scala-sbt main-settings ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE53} --ivyfile %{SOURCE153} org.scala-sbt incremental-compiler ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE54} --ivyfile %{SOURCE154} org.scala-sbt cache ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE55} --ivyfile %{SOURCE155} org.scala-sbt compiler-integration ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE56} --ivyfile %{SOURCE156} org.scala-sbt api ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE57} --ivyfile %{SOURCE157} org.scala-sbt main ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE58} --ivyfile %{SOURCE158} org.scala-sbt classpath ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE59} --ivyfile %{SOURCE159} org.scala-sbt logging ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE60} --ivyfile %{SOURCE160} org.scala-sbt compile ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE61} --ivyfile %{SOURCE161} org.scala-sbt process ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE62} --ivyfile %{SOURCE162} org.scala-sbt actions ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE63} --ivyfile %{SOURCE163} org.scala-sbt sbt-launch ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE64} --ivyfile %{SOURCE164} org.scala-sbt scripted-plugin ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE65} --ivyfile %{SOURCE165} org.scala-sbt tracking ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE66} --ivyfile %{SOURCE166} org.scala-sbt tasks ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE67} --ivyfile %{SOURCE167} org.scala-sbt completion ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE68} --ivyfile %{SOURCE168} org.scala-sbt cross ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE69} --ivyfile %{SOURCE169} org.scala-sbt relation ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE70} --ivyfile %{SOURCE170} org.scala-sbt io ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE71} --ivyfile %{SOURCE171} org.scala-sbt sbt ivy-local --version %{sbt_bootstrap_version}
./climbing-nemesis.py --jarfile %{SOURCE72} --ivyfile %{SOURCE172} org.scala-sbt scripted-framework ivy-local --version %{sbt_bootstrap_version}

# plugins

./climbing-nemesis.py --jarfile %{SOURCE73} com.typesafe.sbt sbt-ghpages ivy-local --version %{sbt_ghpages_version} --meta e:scalaVersion=%{scala_short_version} --meta e:sbtVersion=%{sbt_short_version}
./climbing-nemesis.py --jarfile %{SOURCE74} com.typesafe.sbt sbt-site ivy-local --version %{sbt_site_version} --meta e:scalaVersion=%{scala_short_version} --meta e:sbtVersion=%{sbt_short_version}
./climbing-nemesis.py --jarfile %{SOURCE75} com.typesafe.sbt sbt-git ivy-local --version %{sbt_git_version} --meta e:scalaVersion=%{scala_short_version} --meta e:sbtVersion=%{sbt_short_version}

# SXR
./climbing-nemesis.py --jarfile %{SOURCE76} org.scala-tools.sxr sxr ivy-local --version %{sxr_version}

# sbinary
./climbing-nemesis.py --jarfile %{SOURCE77} org.scala-tools.sbinary sbinary ivy-local --version %{sbinary_version}

# scalacheck
./climbing-nemesis.py --jarfile %{SOURCE78} org.scalacheck scalacheck ivy-local --version %{scalacheck_version}

# specs2
./climbing-nemesis.py --jarfile %{SOURCE79} org.specs2 specs2 ivy-local --version %{specs2_version}

# test-interface
./climbing-nemesis.py --jarfile %{SOURCE80} org.scala-sbt test-interface ivy-local --version %{testinterface_version}

# dispatch-http
./climbing-nemesis.py --jarfile %{SOURCE81} net.databinder dispatch-http_%{scala_short_version} ivy-local --version %{dispatch_http_version}

%else
# If we aren't bootstrapping, copy installed jars into local ivy cache
# dir.  It sure would be nice if we could resolve these via Ivy from
# installed packages.  This is a FIXME for now, though.

%endif

# remove any references to Scala 2.10.2
sed -i -e 's/["]2[.]10[.]2["]/\"2.10.3\"/g' $(find . -name \*.xml)

%build
export SCALA_HOME=%{_javadir}/scala

mkdir -p sbt-boot-dir/scala-%{scala_version}/org.scala-sbt/sbt/%{sbt_bootstrap_version}/
mkdir -p sbt-boot-dir/scala-%{scala_version}/lib

# for jar in $(find ivy-local/org/scala-sbt/ -name \*.jar) ; do 
#     cp $jar sbt-boot-dir/scala-%{scala_version}/org.scala-sbt/sbt/%{sbt_bootstrap_version}/
# done

# for jar in $(find ivy-local/ -name \*.jar | grep -v org/scala-sbt) ; do 
#   cp $jar sbt-boot-dir/scala-%{scala_version}/lib
# done

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
