#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# create cmake build system files by iterating all available languages [1]
# 

import os
import re
import sys
import getopt

cmake_filename = "CMakeLists.txt"

def createTopLevelCMakeListFile(subdir, language):
    topLevelCmakeList = os.path.join(subdir, cmake_filename)

    content = "                                            \n\
project(kde-i18n-%s)                                           \n\
                                                               \n\
# Search KDE installation                                      \n\
find_package(KDE4 REQUIRED)                                    \n\
find_package(Gettext REQUIRED)                                 \n\
include (KDE4Defaults)                                         \n\
include(MacroOptionalAddSubdirectory)                          \n\
                                                               \n\
if (NOT GETTEXT_MSGMERGE_EXECUTABLE)                           \n\
   MESSAGE(FATAL_ERROR \"Please install the msgmerge binary\") \n\
endif (NOT GETTEXT_MSGMERGE_EXECUTABLE)                        \n\
                                                               \n\
IF(NOT GETTEXT_MSGFMT_EXECUTABLE)                              \n\
   MESSAGE(FATAL_ERROR \"Please install the msgfmt binary\")   \n\
endif (NOT GETTEXT_MSGFMT_EXECUTABLE)                          \n\
" % (language)
    f = open(topLevelCmakeList,"w")
    f.write(content)
    f.write('\nset(CURRENT_LANG %s)\n\n' % (language))
    return f

#
# subdir 'messages'
#
def add_cmake_files_messages_po(path):
    filename = os.path.join(path, cmake_filename)
    fc = open(filename, "w")
    fc.write("file(GLOB _po_files *.po)\n\
GETTEXT_PROCESS_PO_FILES(${CURRENT_LANG} ALL INSTALL_DESTINATION ${LOCALE_INSTALL_DIR} ${_po_files} )\n")
    fc.close()

def walk_subdir_messages(path):
    fc = open(os.path.join(path, cmake_filename), "w")
    for subdir in os.listdir(path):
        if (subdir != "others" and subdir != "www.kde.org" and subdir != ".svn"):
            p = os.path.join(path, subdir)         
            if (os.path.isdir(p)):
                fc.write("add_subdirectory( %s )\n" % subdir)
                add_cmake_files_messages_po(p)
    fc.write("install(FILES entry.desktop DESTINATION ${LOCALE_INSTALL_DIR}/${CURRENT_LANG}/ )\n")
    fc.close()

def add_cmake_files_messages(langdir, f):
    msgdir = os.path.join(langdir, 'messages')
    if not os.path.exists(msgdir):
        return
    f.write("macro_optional_add_subdirectory( messages )\n")
    walk_subdir_messages(msgdir)


#
# subdir 'docs'
#
def add_cmake_files_docs_subdir(path, subdir):
    if subdir == "common":
        f = open(os.path.join(path, subdir, cmake_filename), "w")
        f.write("FILE(GLOB _html *.html)\n")
        f.write("FILE(GLOB _css *.css)\n")
        f.write("FILE(GLOB _pngs *.png)\n")
        f.write("install( FILES ${_html} ${_css} ${_png} DESTINATION ${HTML_INSTALL_DIR}/${CURRENT_LANG}/common)\n")
        f.close()
        return
    if os.path.isfile(os.path.join(path, subdir, "index.docbook")):
        add_subdir = ""
        openmode = "w"
        (head, tail) = os.path.split(path)
        # check for khelpcenter module
        if subdir == "faq" or subdir == "glossary" or subdir == "quickstart" or \
           subdir == "userguide" or subdir == "visualdict":
            add_subdir = "SUBDIR khelpcenter/%s" % subdir
        # kcontrol or kinfocenter main dir
        elif subdir == "kcontrol" or subdir == "kinfocenter":
            walk_subdir_docs(os.path.join(path, subdir))
            openmode = "a"
        # kcontrol subdir
        elif tail == "kcontrol":
            add_subdir = "SUBDIR kcontrol/%s" % subdir
        # kinfocenter subdir
        elif tail == "kinfocenter":
            add_subdir = "SUBDIR kinfocenter/%s" % subdir

        f = open(os.path.join(path, subdir, cmake_filename), openmode)
        f.write("kde4_create_handbook(index.docbook INSTALL_DESTINATION ${HTML_INSTALL_DIR}/${CURRENT_LANG}/ %s )\n" \
                 % add_subdir)
        f.close()
        return
    walk_subdir_docs(os.path.join(path, subdir))

def walk_subdir_docs(path):
    fc = open(os.path.join(path, cmake_filename), "w")
    for subdir in os.listdir(path):
        if (subdir != ".svn"):
            p = os.path.join(path, subdir)         
            if (os.path.isdir(p)):
                fc.write("add_subdirectory( %s )\n" % subdir)
                add_cmake_files_docs_subdir(path, subdir)
    fc.close()

def add_cmake_files_docs(path, f):
    docdir = os.path.join(path, 'docs')
    if not os.path.exists(docdir):
        return
    f.write("macro_optional_add_subdirectory( docs )\n")
    walk_subdir_docs(docdir)


#
# subdir 'data'
#
def walk_subdir_data(path):
    fc = open(os.path.join(path, cmake_filename), "w")
    for subdir in os.listdir(path):
        if (subdir != ".svn"):
            p = os.path.join(path, subdir)         
            if (os.path.isdir(p)):
                fc.write("add_subdirectory( %s )\n" % subdir)
    fc.close()


def add_cmake_files_data(path, f):
    datadir = os.path.join(path, 'data')
    if not os.path.exists(datadir):
        return
    f.write("macro_optional_add_subdirectory( data )\n")
    walk_subdir_data(datadir)


#
# subdir 'scripts'
#
def add_cmake_files_scripts_subdir(path):
    fc = open(os.path.join(path, cmake_filename), "w")
    for subdir in os.listdir(path):
        if (subdir != "internal" and subdir != ".svn"):
            p = os.path.join(path, subdir)         
            if (os.path.isdir(p)):
                fc.write("kde4_install_ts_files(\${CURRENT_LANG} %s)\n" % subdir)
    fc.close()

def walk_subdir_scripts(path):
    fc = open(os.path.join(path, cmake_filename), "w")
    for subdir in os.listdir(path):
        if (subdir != "internal" and subdir != ".svn"):
            p = os.path.join(path, subdir)         
            if (os.path.isdir(p)):
                fc.write("add_subdirectory( %s )\n" % subdir)
                add_cmake_files_scripts_subdir(os.path.join(path, subdir))
    fc.close()

def add_cmake_files_scripts(path, f):
    scriptsdir = os.path.join(path, 'scripts')
    if not os.path.exists(scriptsdir):
        return
    f.write("macro_optional_add_subdirectory( scripts )\n")
    walk_subdir_scripts(scriptsdir)

def handle_subdir(langdir, language):
    print "processing %s" % (langdir)

    # toplevel cmake script
    f = createTopLevelCMakeListFile(langdir, language)

    # UI message catalogs
    add_cmake_files_messages(langdir, f)

    # Documentation
    add_cmake_files_docs(langdir, f)

    # Custom localized application data.
    add_cmake_files_data(langdir, f)

    # Transcript files.
    add_cmake_files_scripts(langdir, f)

    search = re.compile(langdir + '@.*')
    for subdir in os.listdir(langdir):
        if search.match(subdir):
            handle_subdir(os.path.join(langdir, subdir), subdir)
            f.write("macro_optional_add_subdirectory( %s )\n" % subdir)
            
    f.close()


subdirs = sys.argv[1:]
if not subdirs:
    fileName = 'inst-apps'
    if not os.path.exists(fileName):
        fileName = 'subdirs'
    f = open(fileName, "r")
    for line in f.read().splitlines():
        subdirs.append(line)
    f.close()

if not subdirs:
    print "no subdirs given."
    exit(1)

# Go through all subdirs
for langdir in subdirs:
    handle_subdir(langdir, langdir)
