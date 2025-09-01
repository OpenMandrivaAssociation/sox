%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}

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
Version:	14.6.0.4
Release:	2%{?extrarelsuffix}
License:	LGPLv2+
Group:		Sound
# Original project:
#Url:		https://sox.sourceforge.net/
#Source0:	https://downloads.sourceforge.net/project/sox/sox/%{version}/sox-%{version}.tar.bz2
# Fork that is still maintained:
Url:		https://codeberg.org/sox_ng/sox_ng
Source0:	https://codeberg.org/sox_ng/sox_ng/releases/download/sox_ng-%{version}/sox_ng-%{version}.tar.gz
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
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libavformat)
BuildRequires:	lame-devel
%if %{build_plf}
BuildRequires:	libamrwb-devel
BuildRequires:	libamrnb-devel
%endif

Requires:	%{libname} = %{version}-%{release}

BuildSystem:	autotools
BuildOption:	--with-distro=OpenMandriva
BuildOption:	--with-ffmpeg
BuildOption:	--with-ladspa-path=%{_includedir}
BuildOption: 	--with-dyn-default
BuildOption:	--enable-dl-sndfile

%patchlist
sox-ng-actually-find-the-plugins.patch

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
cd %{buildroot}%{_bindir}
for i in *_ng; do
	ln -s $i ${i/_ng/}
done
cd %{buildroot}%{_libdir}
for i in libsox_ng.so*; do
	ln -s $i ${i/_ng/}
done
ln -s sox_ng.pc pkgconfig/sox.pc
# We place the symlink in the "wrong" direction here
# to work around the "don't replace directories with symlinks"
# rule in rpm
mv sox_ng sox
ln -s sox sox_ng

# symlink needed by mlt
ln -s sox_ng.h %{buildroot}%{_includedir}/sox.h

%files
%doc ChangeLog README AUTHORS
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox
%{_bindir}/soxi
%{_bindir}/play_ng
%{_bindir}/rec_ng
%{_bindir}/sox_ng
%{_bindir}/soxi_ng
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n %{libname}
%{_libdir}/libsox_ng.so.%{major}*
%{_libdir}/libsox.so.%{major}*
%{_libdir}/sox
%{_libdir}/sox_ng

%files -n %{devname}
%{_includedir}/*.h
%{_libdir}/libsox.so
%{_libdir}/libsox_ng.so
%{_libdir}/pkgconfig/sox.pc
%{_libdir}/pkgconfig/sox_ng.pc
%{_mandir}/man3/*
