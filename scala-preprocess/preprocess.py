#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from subprocess import PIPE, Popen as popen


def ant_contrib(tree):
    """ Fixes classpath for ant-contrib """
    task = tree.find(".//taskdef[@resource='net/sf/antcontrib/antlib.xml']")
    task.attrib["classpath"] = "/usr/share/java/ant-contrib/ant-contrib.jar"


def remove_jarjar(tree):
    """ Remove Jar Jar Links from the build.  Assumes this will be 
        run before aetherize """
    for childpath in [".//{urn:maven-artifact-ant}dependencies[@pathId='jarjar.classpath']", ".//taskdef[@classpathref='jarjar.classpath']", ".//jarjar"]:
        child = tree.find(childpath)
        parent = tree.find("%s/.." % childpath)
        parent.remove(child)


def remove_vizant(tree):
    """ Remove visualizations from the build. """
    for childpath in [".//target[@name='graph.init']", ".//target[@name='graph.all']", ".//target[@name='graph.sabbus']"]:
        child = tree.find(childpath)
        parent = tree.find("%s/.." % childpath)
        parent.remove(child)
    
def aetherize(tree):
    """ Replace maven-ant-tasks with aether-ant-tasks. """

    # wrap dependencies in resolves
    for parent in tree.findall(".//{urn:maven-artifact-ant}dependencies/.."):
        resolve = ET.SubElement(parent, "{antlib:org.eclipse.aether.ant}resolve")
        for child in parent.findall("{urn:maven-artifact-ant}dependencies"):
            parent.remove(child)
            child.tag = "{antlib:org.eclipse.aether.ant}dependencies"
            resolve.append(child)
            if "filesetId" in child.attrib:
                # fileset = ET.SubElement(resolve, "files")
                # fileset.attrib["refid"] = child.attrib["filesetId"]
                del child.attrib["filesetId"]
            if "pathId" in child.attrib:
                for scope in ["compile", "runtime", "test"]:
                    classpath = ET.SubElement(resolve, "path")
                    classpath.attrib["refid"] = child.attrib["pathId"]
                    classpath.attrib["classpath"] = scope
                del child.attrib["pathId"]

    for parent in tree.findall(".//copy-deps/.."):
        for copydeps in parent.findall("copy-deps"):
            parent.remove(copydeps)

    for elt in tree.findall(".//{urn:maven-artifact-ant}dependencies"):
        elt.tag = "{antlib:org.eclipse.aether.ant}dependencies"

    for elt in tree.findall(".//{urn:maven-artifact-ant}remoteRepository"):
        elt.tag = "{antlib:org.eclipse.aether.ant}remoterepo"

    classpath = tree.find(".//path[@id='maven-ant-tasks.classpath']")
    classpath.attrib["id"] = "aether-ant-tasks.classpath"
    del classpath.attrib["path"]
    classpath.tag = "path"

    typedef = tree.find(".//typedef[@resource='org/apache/maven/artifact/ant/antlib.xml']")
    typedef.attrib["resource"] = "org/eclipse/aether/ant/antlib.xml"
    typedef.attrib["uri"] = "antlib:org.eclipse.aether.ant"
    typedef.attrib["classpathref"] = "aether-ant-tasks.classpath"


def elim_bootstrap_fetch(tree):
    """ Don't fetch bootstrap libraries; 
        eliminate children of the boot target. """

    boot = tree.find('.//target[@name="boot"]')
    for child in boot.findall("./exec"):
        boot.remove(child)
    echo = boot.find("./echo")
    echo.attrib["message"] = "Not fetching bootstrap libraries in the Fedora build"


def transform(infile, outfile):
    tree = ET.parse(infile)
    
    elim_bootstrap_fetch(tree)
    ant_contrib(tree)
    remove_jarjar(tree)
    remove_vizant(tree)
    aetherize(tree)
    
    tree.write(outfile)


if __name__ == "__main__":
    from sys import argv
    transform(argv[1], argv[2])
