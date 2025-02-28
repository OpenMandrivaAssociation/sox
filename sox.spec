%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%define _disable_lto 1

######################
# Hardcode PLF build
%define build_plf 0
######################

%if %{build_plf}
%define distsuffix plf
%define extrarelsuffix plf
%endif

%define major	3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	A general purpose sound file conversion tool
Name:		sox
Version:	14.4.2
Release:	9%{?extrarelsuffix}1
License:	LGPLv2+
Group:		Sound
Url:		https://sox.sourceforge.net/
Source0:	https://downloads.sourceforge.net/project/sox/sox/%{version}/sox-%{version}.tar.bz2
BuildRequires:	gomp-devel
BuildRequires:	gsm-devel
BuildRequires:	ladspa-devel
BuildRequires:	libtool-devel
BuildRequires:	lpc10-devel
BuildRequires:	magic-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(id3tag)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(wavpack)
BuildRequires:	lame-devel
%if %{build_plf}
BuildRequires:	libamrwb-devel
BuildRequires:	libamrnb-devel
%endif

Requires:	%{libname} = %{version}-%{release}

BuildSystem:	autotools
BuildOption:	--with-ladspa-path=%{_includedir}
BuildOption: 	--with-dyn-default
BuildOption:	--enable-dl-sndfile

%description
SoX (Sound eXchange) is a sound file format converter for Linux,
UNIX and DOS PCs. The self-described 'Swiss Army knife of sound
tools,' SoX can convert between many different digitized sound
formats and perform simple sound manipulation functions,
including sound effects.

Install the sox package if you'd like to convert sound file formats
or manipulate some sounds.

%if %{build_plf}
This package is in restricted as it was build with AMR encoder
support, which is in restricted.
%endif

%package -n %{libname}
Summary:	Libraries for SoX
Group:		System/Libraries

%description -n %{libname}
Libraries for SoX.

%package -n %{devname}
Summary:	Development headers and libraries for libst
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development headers and libraries for SoX.

%conf -p
export CFLAGS="%{optflags} -DHAVE_SYS_SOUNDCARD_H=1 -D_FILE_OFFSET_BITS=64 -fPIC -DPIC"

%install -a

ln -sf play %{buildroot}%{_bindir}/rec

cat << EOF > %{buildroot}%{_bindir}/soxplay
#!/bin/sh

%{_bindir}/sox \$1 -t .au - > /dev/audio

EOF
chmod 755 %{buildroot}%{_bindir}/soxplay

ln -snf play %{buildroot}%{_bindir}/rec
ln -s play.1%{_extension} %{buildroot}%{_mandir}/man1/rec.1%{_extension}

%files
%doc ChangeLog README NEWS AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox*
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/libsox.so.%{major}*	
%{_libdir}/sox/libsox_fmt_*.so

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_mandir}/man3/*

