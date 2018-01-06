%define commit e4dfc87aa1d3e974c065511e34f3a14b61641c34
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define sname gorilla

Summary:	A tcl/tk password manager
Name:		password-%{sname}
Version:	1.5.3.7
Release:	0
License:	GPLv2+
Group:		File tools
URL:		http://zdia.de/downloads/%{sname}/index.html
#Source0:	https://github.com/zdia/%{sname}/archive/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/zdia/%{sname}/archive/%{commit}/%{name}-%{commit}.tar.gz
#Patch0:		%{name}-1.5.3.7-tclsh_version-patch
BuildArch:	noarch

#Depends: tcl8.5, tk8.5, itcl3, tcllib, tklib, ${misc:Depends}
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
#% setup -q -n %{sname}-%{version}
%setup -q -n %{sname}-%{commit}
%apply_patches

# fix file-not-utf8 warning
for f in sources/CHANGES.txt
do
	iconv -f ISO-8859-1 -t UTF-8 $f >${f}.tmp
	chmod --reference=$f ${f}.tmp
	touch --reference=$f ${f}.tmp
	mv ${f}.tmp $f
done

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
Comment="lightwaight password manager"
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

