Name:       iniparser
Summary:    Stand-alone ini file parsing library
Version:    2.17
Release:    1
Group:      Applications/Databases
License:    MIT
URL:        http://ndevilla.free.fr/iniparser/
Source:     http://ndevilla.free.fr/iniparser/iniparser-%{version}.tar.gz
Source1001: packaging/iniparser.manifest 
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
iniparser is a free stand-alone ini file parsing library.
It is written in portable ANSI C and should compile anywhere.
iniparser is distributed under an MIT license.

%package devel
Summary:    Development tools for stand-alone ini file parsing library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the header files and development documentation
for %{name}. If you like to develop programs using %{name}, you will need
to install %{name}-devel.

%prep
%setup -q

%build
cp %{SOURCE1001} .

LDFLAGS="-Wl,--rpath=%{_prefix}/lib -Wl,--hash-style=both -Wl,--as-needed $LDFLAGS" \
	make prefix=%{_prefix}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT/%{_libdir}
install -m 755 libiniparser.so.0 $RPM_BUILD_ROOT/%{_libdir}
ln -s libiniparser.so.0 $RPM_BUILD_ROOT/%{_libdir}/libiniparser.so
mkdir -p $RPM_BUILD_ROOT/%{_includedir}
install -m 755 src/*.h $RPM_BUILD_ROOT/%{_includedir}
install -m 755 src/*.h $RPM_BUILD_ROOT/%{_includedir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig
cat > $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{name}.pc <<EOF
prefix = %{_prefix}
exec_prefix = %{_exec_prefix}
libdir = %{_libdir}
includedir = %{_includedir}

Name : iniparser
Description : a free stand-alone ini file parsing library.
Version : %{version}
Libs : -L\${libdir} -liniparser
Cflags : -I\${includedir}

EOF

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest iniparser.manifest
%{_libdir}/*.so.*

%files devel
%manifest iniparser.manifest
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
