%define sname gorilla

Summary:  A tcl/tk password manager
Name:     password-%{sname}
Version:  1.5.3.7
Release:  0
License:  GPLv2+
Group:    File tools
URL:      http://zdia.de/downloads/%{sname}/index.html
Source0:  https://github.com/zdia/%{sname}/archive/v%{version}.tar.gz
Patch0:   %{name}-1.5.3.7-tclsh_version-patch
BuildArch:  noarch

BuildRequires:  tk
BuildRequires:  docbook-to-man
BuildRequires:  imagemagick
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  librsvg
BuildRequires:  imagemagick

Requires:  tcl
Requires:  tk
Requires:  tcl-tcllib
Requires:  tcl-tklib

%description
A tcl/tk password manager

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

%prep
%setup -q -n %{sname}-%{version}

# apply all patches
%patch0 -p1 -b .orig

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

%install
# program
%__install -dm 755 %{buildroot}%{_datadir}/%{name}/
%__install -pm 644 sources/*.tcl %{buildroot}%{_datadir}/%{name}/
%__chmod 755 %{buildroot}%{_datadir}/%{name}/%{sname}.tcl

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/modules/
%__install -pm 644 sources/modules/*.tm %{buildroot}%{_datadir}/%{name}/modules/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/blowfish/
%__install -pm 644 sources/blowfish/blowfish.tcl %{buildroot}%{_datadir}/%{name}/blowfish/
%__install -pm 644 sources/blowfish/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/blowfish/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/twofish/
%__install -pm 644 sources/twofish/twofish.tcl %{buildroot}%{_datadir}/%{name}/twofish/
%__install -pm 644 sources/twofish/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/twofish/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/pwsafe/
%__install -pm 644 sources/pwsafe/pwsafe*.tcl %{buildroot}%{_datadir}/%{name}/pwsafe/
%__install -pm 644 sources/pwsafe/pkgIndex.tcl %{buildroot}%{_datadir}/%{name}/pwsafe/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/msgs/
%__install -pm 644 sources/msgs/*msg %{buildroot}%{_datadir}/%{name}/msgs/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/msgs/help/
%__install -pm 644 sources/msgs/help/*msg %{buildroot}%{_datadir}/%{name}/msgs/help/

%__install -dm 755 %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/application.gif %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/browse.gif %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/%{sname}-splash.gif %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/group.gif %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/login.gif %{buildroot}%{_datadir}/%{name}/pics/
%__install -pm 644 sources/pics/splash.gif %{buildroot}%{_datadir}/%{name}/pics/

# launcher
%__install -dm 755 %{buildroot}%{_bindir}/
%__install -pm 755 %{name}.sh %{buildroot}%{_bindir}/%{name}

# manpage
#FIXME: add manpage


# .desktop file
%__install -dm 755 %{buildroot}%{_datadir}/applications/
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
#        a bug in inkskape maybe a bug in image)
#        rsvg-convert works properly for png only
for d in 16 32 48 64 72 128 256
do
  %__install -dm 755  %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
  rsvg-convert -f png -h ${d} -w ${d} sources/pics/vector-logo/%{sname}-logo.svg \
              -o %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
#  convert -background none -size "${d}x${d}" sources/pics/vector-logo/%{sname}-logo.svg \
#                                        %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{name}.png
done
#%__install -dm 755 %{buildroot}%{_datadir}/pixmaps/
#convert -size 32x32 sources/pics/vector-logo/%{sname}-logo.svg \
#                    %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

%check
# desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/openmandriva-%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

