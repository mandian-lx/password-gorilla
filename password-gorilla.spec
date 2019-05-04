%define commit 18206d30a62f1a9843ba541d73e6c9460ec5fb56
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define sname gorilla

# Latest version is quite old so actually pre-release
# version actually it may be safey
%define pre_release 0

Summary:	A tcl/tk password manager
Name:		password-%{sname}
Version:	1.5.3.8
Release:	0
License:	GPLv2+
Group:		File tools
URL:		https://github.com/zdia
%if %{pre_release}
Source0:	https://github.com/zdia/%{sname}/archive/%{commit}/%{name}-%{commit}.tar.gz
%else
Source0:	https://github.com/zdia/%{sname}/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:		%{name}-1.5.3.7-unbundle_tcllib_uuid_module.patch
%endif
BuildArch:	noarch

BuildRequires:	docbook-to-man
BuildRequires:	imagemagick
BuildRequires:	librsvg
BuildRequires:	tk

Requires:	tcl
Requires:	tcl-tcllib
Requires:	tcl-tklib
Requires:	tk

%description
A tcl/tk password manager.

%files
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
#%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/applications/openmandriva-%{name}.desktop
%doc README
%doc sources/help.txt
%doc sources/CHANGES.txt
%doc sources/LICENSE.txt

#---------------------------------------------------------------------------

%prep
%if %{pre_release}
%setup -q -n %{sname}-%{commit}
%else
%setup -q -n %{sname}-%{version}
%endif
%autopatch -p1

# fix version
%if %{pre_release}
	sed -i -e "s|{\$Revision: 1.5.3.7 \$}|\{\$Revision: %{version} pre-release \$}|" sources/gorilla.tcl
%endif

# launcher
cat > %{name}.sh << EOF
#!/bin/sh

exec /usr/share/%{name}/%{sname}.tcl $@
EOF

%build
# Nothing to build

%install
# launcher
install -dm 0755 %{buildroot}%{_bindir}/
install -pm 0755 %{name}.sh %{buildroot}%{_bindir}/%{name}

# program
install -dm 0755 %{buildroot}%{_datadir}/%{name}/
install -pm 0644 sources/*.tcl %{buildroot}%{_datadir}/%{name}/
chmod 0755 %{buildroot}%{_datadir}/%{name}/%{sname}.tcl

install -dm 0755 %{buildroot}%{_datadir}/%{name}/modules/
install -pm 0644 sources/modules/*.tm %{buildroot}%{_datadir}/%{name}/modules/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/blowfish/
install -pm 0644 sources/blowfish/blowfish.tcl %{buildroot}%{_datadir}/%{name}/blowfish/
install -pm 0644 sources/blowfish/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/blowfish/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/twofish/
install -pm 0644 sources/twofish/twofish.tcl %{buildroot}%{_datadir}/%{name}/twofish/
install -pm 0644 sources/twofish/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/twofish/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/pwsafe/
install -pm 0644 sources/pwsafe/pwsafe*.tcl %{buildroot}%{_datadir}/%{name}/pwsafe/
install -pm 0644 sources/pwsafe/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/pwsafe/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/msgs/
install -pm 0644 sources/msgs/*msg %{buildroot}%{_datadir}/%{name}/msgs/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/msgs/help/
install -pm 0644 sources/msgs/help/*msg %{buildroot}%{_datadir}/%{name}/msgs/help/
install -pm 0644 sources/help.txt %{buildroot}%{_datadir}/%{name}/

install -dm 0755 %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/application.gif %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/browse.gif %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/%{sname}-splash.gif %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/group.gif %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/login.gif %{buildroot}%{_datadir}/%{name}/pics/
install -pm 0644 sources/pics/splash.gif %{buildroot}%{_datadir}/%{name}/pics/

# manpage
#FIXME: add manpage

# .desktop file
install -dm 0755 %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment="lightweight password manager"
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=System;
X-Vendor=OpenMandriva
EOF

# icons
# FIXME: imagemagick produces empty images (maybe
#	a bug in inkskape maybe a bug in image)
#	rsvg-convert works properly for png only
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	rsvg-convert -f png -h ${d} -w ${d} sources/pics/vector-logo/%{sname}-logo.svg \
			-o %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
#	convert -background none -size "${d}x${d}" sources/pics/vector-logo/%{sname}-logo.svg \
#																				%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
#install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
#convert -size 32x32 sources/pics/vector-logo/%{sname}-logo.svg \
#	%{buildroot}%{_datadir}/pixmaps/%{name}.xpm

%check
# .desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop
