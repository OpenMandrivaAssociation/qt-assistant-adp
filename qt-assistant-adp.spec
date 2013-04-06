%define debug_package %{nil}
Summary:	Compatibility version of Qt Assistant
Name:		qt-assistant-adp
Epoch:		4
Version:	4.6.3
Release:	6
# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License:	LGPLv2 with exceptions or GPLv3 with exceptions
Group:		System/Libraries
Url:		http://qt.nokia.com/doc/4.6/qassistantclient.html
Source:		ftp://ftp.qt.nokia.com/qt/source/qt-assistant-qassistantclient-library-compat-src-%{version}.tar.gz
# missing header files from Debian (Fathi Boudra)
Source1:	QAssistantClient
Source2:	QtAssistant
# build fixes from Debian (Fathi Boudra)
Patch1:		01_build_system.diff
BuildRequires: qt4-devel >= 4:4.7.0
Conflicts: qt4-assistant < 4:4.6.3

%description
The old version of Qt Assistant, based on Assistant Document Profile (.adp)
files, and the associated QtAssistantClient library, for compatibility with
applications providing help in that format.

New applications should use the new version of Qt Assistant introduced in Qt
4.4, based on the Qt Help Framework also introduced in Qt 4.4, instead.

%define libqassistant %mklibname qassistant 4
%package -n %{libqassistant}
Summary:	QT assistant lib
Group:		System/Libraries
Provides:	qassistantlib = %epoch:%version


%description -n %{libqassistant}
QT assistant lib.

%package devel
Summary:	Development files for the compatibility QAssistantClient
Group:		Development/KDE and Qt
Requires:	%{libqassistant} = %{epoch}:%{version}-%{release}
Requires:	qt4-devel >= 4:4.7.0

%description devel
This package contains the files necessary to build applications using the
deprecated QAssistantClient class (in the deprecated QtAssistantClient
library), which is used together with the legacy Assistant Document
Profile (.adp) version of Qt Assistant.

This class is obsolete. It is provided to keep old source code working. 
We strongly advise against using it in new code. New code should use the
Qt Help Framework introduced in Qt 4.4 and/or the version of Qt Assistant
based on it (also introduced in Qt 4.4) instead.

%prep
%setup -q -n qt-assistant-qassistantclient-library-compat-version-%{version}
%patch1 -p1 -b .build_system
mkdir include
cp -p %{SOURCE1} %{SOURCE2} include/

%build
# build assistant_adp
%qmake_qt4 QT_PRODUCT=OpenSource
%make

# build libQtAssistantClient
pushd lib
%qmake_qt4 CONFIG=create_prl
%make
popd

# build assistant_adp translations
pushd translations
lrelease assistant_adp_*.ts
popd

%install
# install assistant_adp
make install INSTALL_ROOT=%{buildroot}

# install libQtAssistantClient
make install INSTALL_ROOT=%{buildroot} -C lib

# install assistant_adp translations
mkdir -p %{buildroot}%{qt4dir}/translations
install -p -m644 translations/assistant_adp_*.qm \
                 %{buildroot}%{qt4dir}/translations

# install assistant.prf mkspec
install -D -p -m644 features/assistant.prf \
                    %{buildroot}%{qt4dir}/mkspecs/features/assistant.prf

# install missing headers (thanks to Fathi Boudra from Debian)
install -p -m644 include/Q* %{buildroot}%{qt4include}/QtAssistant/

# nuke dangling reference(s) to the buildroot
sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" %{buildroot}%{qt4lib}/*.prl

# let rpm handle binaries conflicts
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{qt4bin}
mv assistant_adp ../../../bin/
ln -s ../../../bin/assistant_adp .
popd

# _debug target (see bug #196513)
pushd %{buildroot}%{qt4lib}
echo "INPUT(-lQtAssistantClient)" >libQtAssistantClient_debug.so
popd

# Note that we intentionally DO NOT install a .desktop file for assistant_adp
# because it makes no sense to invoke it without a specific .adp file to open.
# By default, it views the Qt documentation, for which we already have a menu
# entry using the current version of the Qt Assistant, and there is no UI for
# viewing anything different. The .adp file needs to be passed on the command
# line, which is usually done by the application.

%files
%doc LGPL_EXCEPTION.txt LICENSE.LGPL LICENSE.GPL3
%{_bindir}/assistant_adp
%{qt4dir}/translations/*
%{qt4bin}/assistant_adp

%files -n %{libqassistant}
%{qt4lib}/libQtAssistantClient.so.4*

%files devel
%{qt4include}/QtAssistant/
%{qt4lib}/libQtAssistantClient.so
%{qt4lib}/libQtAssistantClient_debug.so
%{qt4lib}/libQtAssistantClient.prl
%{_libdir}/pkgconfig/QtAssistantClient.pc
%{qt4dir}/mkspecs/features/assistant.prf


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 4:4.6.3-2mdv2011.0
+ Revision: 669384
- mass rebuild

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 4:4.6.3-1mdv2011.0
+ Revision: 563937
- minor cleanup of spec file
- import qt-assistant-adp


