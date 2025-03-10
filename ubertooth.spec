#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Ubertooth - open source, wireless development platform
Summary(pl.UTF-8):	Ubertooth - otwarta platformwa do tworzenia urządzeń bezprzewodowych
Name:		ubertooth
%define	tag_ver	2020-12-R1
Version:	%(echo %{tag_ver} | tr - _)
Release:	
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/greatscottgadgets/ubertooth/releases
Source0:	https://github.com/greatscottgadgets/ubertooth/archive/%{tag_ver}/%{name}-%{tag_ver}.tar.gz
# Source0-md5:	4dd2d6539cfc694f3d63424c65b28394
Patch0:		%{name}-python.patch
URL:		https://github.com/greatscottgadgets/ubertooth
BuildRequires:	bluez-libs-devel
BuildRequires:	cmake >= 2.8
BuildRequires:	libbtbb-devel
BuildRequires:	libusb-devel >= 1.0
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Project Ubertooth is an open source wireless development platform
suitable for Bluetooth experimentation. Ubertooth ships with a capable
BLE (Bluetooth Smart) sniffer and can sniff some data from Basic Rate
(BR) Bluetooth Classic connections.

%description -l pl.UTF-8
Projekt Ubertooth to otwarta platforma programistyczna do
eksperymentów z Bluetooth. Jest dostarczany ze snifferem BLE
(Bluetooth Smart), potrafi także podsłuchiwać część danych z połączeń
Bluetooth Classic Basic Rate (BR).

%package devel
Summary:	Header files for ubertooth library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ubertooth
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libbtbb-devel
Requires:	libusb-devel >= 1.0

%description devel
Header files for ubertooth library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ubertooth.

%package static
Summary:	Static ubertooth library
Summary(pl.UTF-8):	Statyczna biblioteka ubertooth
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ubertooth library.

%description static -l pl.UTF-8
Statyczna biblioteka ubertooth.

%package python
Summary:	Python tools from Ubertooth project
Summary(pl.UTF-8):	Narzędzia pythonowe z projektu Ubertooth
Group:		Development/Tools
BuildArch:	noarch

%description python
Python tools from Ubertooth project:
- specan_ui.py is a basic spectrum analysis tool for the Ubertooth
- ubtbr is a Python library to control the ubtbr firmware

%description python -l pl.UTF-8
Narzędzia pythonowe z projektu Ubertooth:
- specan_ui.py to narzędzie Ubertooth do podstawowej analizy widma
- ubtbr to biblioteka pythonowa do sterowania firmwarem ubtbr

%prep
%setup -q -n %{name}-%{tag_ver}
%patch0 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	host/python/{specan_ui/ubertooth-specan-ui,ubtbr/ubertooth-btbr}

%{__sed} -i -e 's, --root, --install-purelib=%{py3_sitescriptdir} &,' \
	host/python/{specan_ui,ubtbr}/CMakeLists.txt

%build
cd host
install -d build
cd build
%cmake .. \
	%{?with_static_libs:-DBUILD_STATIC_LIB=ON} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DUDEV_RULES_PATH=/lib/udev/rules.d

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C host/build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md TRADEMARK changelog
%attr(755,root,root) %{_bindir}/ubertooth-afh
%attr(755,root,root) %{_bindir}/ubertooth-btle
%attr(755,root,root) %{_bindir}/ubertooth-debug
%attr(755,root,root) %{_bindir}/ubertooth-dfu
%attr(755,root,root) %{_bindir}/ubertooth-ducky
%attr(755,root,root) %{_bindir}/ubertooth-dump
%attr(755,root,root) %{_bindir}/ubertooth-ego
%attr(755,root,root) %{_bindir}/ubertooth-follow
%attr(755,root,root) %{_bindir}/ubertooth-rx
%attr(755,root,root) %{_bindir}/ubertooth-scan
%attr(755,root,root) %{_bindir}/ubertooth-specan
%attr(755,root,root) %{_bindir}/ubertooth-tx
%attr(755,root,root) %{_bindir}/ubertooth-util
%attr(755,root,root) %{_libdir}/libubertooth.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libubertooth.so.1
/lib/udev/rules.d/40-ubertooth.rules
%{_mandir}/man1/ubertooth-afh.1*
%{_mandir}/man1/ubertooth-btle.1*
%{_mandir}/man1/ubertooth-dfu.1*
%{_mandir}/man1/ubertooth-dump.1*
%{_mandir}/man1/ubertooth-ego.1*
%{_mandir}/man1/ubertooth-rx.1*
%{_mandir}/man1/ubertooth-scan.1*
%{_mandir}/man1/ubertooth-specan.1*
%{_mandir}/man1/ubertooth-util.1*
%{_mandir}/man7/ubertooth.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libubertooth.so
%{_includedir}/ubertooth*.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libubertooth.a
%endif

%files python
%defattr(644,root,root,755)
%doc host/python/ubtbr/README.md
%attr(755,root,root) %{_bindir}/ubertooth-btbr
%attr(755,root,root) %{_bindir}/ubertooth-specan-ui
%{py3_sitescriptdir}/specan
%{py3_sitescriptdir}/specan-*.egg-info
%{py3_sitescriptdir}/ubtbr
%{py3_sitescriptdir}/ubtbr-*.egg-info
