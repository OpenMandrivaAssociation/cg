%define major 0
%define libname %mklibname cg %{major}
%define develname %mklibname cg -d

# libGLU.so doesn'tGL- exist as a provide, so we require GL-devel and add this exception
%if %{_use_internal_dependency_generator}
%define __noautoreq 'libGLU.so'
%else
%define _requires_exceptions libGLU.so
%endif

Name:		cg
Version:	3.1.0013
Release:	4
Summary:	Cg Toolkit - GPU Shader Authoring Language
License:	Freeware
Group:		Development/C
URL:		https://developer.nvidia.com/object/cg_toolkit.html
Source0:	http://developer.download.nvidia.com/cg/Cg_2.2/Cg-3.1_April2012_x86.tgz
Source1:	http://developer.download.nvidia.com/cg/Cg_2.2/Cg-3.1_April2012_x86_64.tgz

Provides:	Cg = %{version}-%{release}
BuildRequires:	recode

ExclusiveArch:	%{ix86} x86_64

%description
The award-winning Cg Toolkit enables software developers to add the latest 
interactive effects to real-time applications with a comprehensive solution 
that works across platforms and graphics API containing:

    * Compiler for the Cg 2.2 language
    * Cg/CgFX Runtime libraries for OpenGL and Direct3D
    * User's Manual and documentation on the Cg Language, Runtime APIs, Cg 
       Library, CgFX States, and Cg Profiles
    * Numerous Cg examples

Supporting dozens of different OpenGL and DirectX profile targets, Cg 
2.2 allows you to incorporate stunning, interactive effects within your 
3D applications and share them between other Cg applications, across 
graphics APIs, and most operating systems (Windows 2000, XP, Vista, Mac 
OS X for Tiger &  Leopard, x86 Linux 32-bit & 64-bit, x86 Solaris 32-bit 
& 64-bit).

This package contains documentation.

%package examples
Summary:	Examples from %{name}
Group:		Development/C
Provides:	Cg-examples = %{version}-%{release}
Requires:	%{name} = %{version}-%{release}

%description examples
Several examples of programs using Cg toolkit.

%package -n	%{libname}
Summary:	Dynamic libraries from %{name}
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}
Provides:	libCg = %{version}-%{release}

%description -n	%{libname}
Dynamic libraries from Cg toolkit.

%package -n	%{develname}
Summary:	Header files and static libraries from %{name}
Group:		Development/C
Requires:	lib%{name} = %{version}
Requires:	pkgconfig(gl)
Requires:	pkgconfig(glu)
Provides:	%{name}-devel = %{version}-%{release} 
Provides:	Cg-devel = %{version}-%{release}
Obsoletes:	%{name}-devel < %{version}-%{release}
Obsoletes:	Cg-devel < %{version}-%{release}

%description -n	%{develname}
Binaries (compiler), libraries and includes files for developing programs 
based on Cg toolkit.

%install
#uncompress the right tarball according to the arch
mkdir -p %{buildroot}
cd %{buildroot}
%ifarch %ix86
tar xvzf %{SOURCE0}
%else
tar xvzf %{SOURCE1}
%endif

#move the doc to the right directory
mkdir -p %{buildroot}%{_docdir}/%{name}
mv %{buildroot}/usr/local/Cg/* %{buildroot}%{_docdir}/%{name}

#include the license in subpackages, too
mkdir %{buildroot}%{_docdir}/%{libname}
mkdir %{buildroot}%{_docdir}/%{develname}
cp %{buildroot}%{_docdir}/%{name}/docs/license.txt %{buildroot}%{_docdir}/%{develname}

# To avoid extra Provides
rm -rf %{buildroot}%{_docdir}/%{name}/examples/Trace

#License doesn't allow us to modify the binaries and libraries
export DONT_STRIP=1

%{buildroot}%{_bindir}/*

chmod 0755 %{buildroot}%{_libdir}/*

%files
%defattr(0644,root,root,0755)
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/examples

%files examples
%defattr(0644,root,root,0755)
%{_docdir}/%{name}/examples

%files -n %{libname}
%defattr(0755,root,root,0755)
%{_libdir}/*

%files -n %{develname}
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{multiarch_bindir}/*
%attr(0755,root,root) %{_bindir}/cgc
%attr(0755,root,root) %{_bindir}/cgfxcat
%attr(0755,root,root) %{_bindir}/cginfo
%{_docdir}/%{develname}
%{_includedir}/Cg
