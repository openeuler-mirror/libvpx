Name:                   libvpx
Version:                1.12.0
Release:                1
Summary:                VP8/VP9 Video Codec SDK
License:                BSD
Source0:                https://github.com/webmproject/libvpx/archive/v%{version}.tar.gz
URL:                    http://www.webmproject.org/code/
BuildRequires:          gcc gcc-c++ doxygen, php-cli, perl(Getopt::Long)
%ifarch x86_64
BuildRequires:          yasm
%endif
Provides:               %{name}-utils = %{version}-%{release}
Obsoletes:              %{name}-utils < %{version}-%{release}

%description
libvpx provides the VP8/VP9 SDK, which allows you to integrate your applications
with the VP8 and VP9 video codecs, high quality, royalty free, open source codecs
deployed on millions of computers and devices worldwide.

%package devel
Summary:                Development files for libvpx
Requires:               %{name} = %{version}-%{release}

%description devel
Development libraries and headers for developing software against libvpx.

%prep
%autosetup libvpx-%{version} -p1

%build
%ifarch x86_64
%global vpxtarget x86_64-linux-gcc
%else
%ifarch aarch64
%global vpxtarget arm64-linux-gcc
%endif
%endif
%set_build_flags

./configure --target=%{vpxtarget} \
--enable-pic --disable-install-srcs --enable-vp9-decoder \
--enable-vp9-encoder --enable-experimental \
--enable-vp9-highbitdepth --enable-shared --enable-install-srcs \
--prefix=%{_prefix} --libdir=%{_libdir} --size-limit=16384x16384

sed -i "s|-O3|%{optflags}|g" libs-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" examples-%{vpxtarget}.mk
sed -i "s|-O3|%{optflags}|g" docs-%{vpxtarget}.mk

%make_build verbose=true

%install
make DIST_DIR=%{buildroot}%{_prefix} dist

if [ -d %{buildroot}/usr/docs ]; then
   mv %{buildroot}/usr/docs doc/
fi

cd %{buildroot}
mv usr/bin/examples/* usr/bin/
mv usr/bin/postproc usr/bin/vp8_postproc
mv usr/bin/simple_decoder usr/bin/vp8_simple_decoder
mv usr/bin/simple_encoder usr/bin/vp8_simple_encoder
mv usr/bin/twopass_encoder usr/bin/vp8_twopass_encoder
chmod 755 usr/bin/*
cd -

cp -a vpx_config.h %{buildroot}%{_includedir}/vpx/vpx_config-%{_arch}.h
touch -r AUTHORS %{buildroot}%{_includedir}/vpx/vpx_config.h

mv %{buildroot}%{_prefix}/src/vpx_dsp %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_mem %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_ports %{buildroot}%{_includedir}/
mv %{buildroot}%{_prefix}/src/vpx_scale %{buildroot}%{_includedir}/

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%license LICENSE
%doc AUTHORS CHANGELOG README
%{_libdir}/libvpx.so.*
%{_bindir}/*
%exclude /usr/build/
%exclude /usr/md5sums.txt
%exclude /usr/lib*/*.a
%exclude /usr/CHANGELOG
%exclude /usr/README
%exclude /usr/bin/examples
%exclude %{_prefix}/src

%files devel
%doc docs/html/
%{_includedir}/vpx/
%{_includedir}/vpx_dsp/
%{_includedir}/vpx_mem/
%{_includedir}/vpx_ports/
%{_includedir}/vpx_scale/
%{_libdir}/pkgconfig/vpx.pc
%{_libdir}/libvpx.so

%changelog
* Sat Feb 04 2023 wenchaofan <349464272@qq.com> - 1.12.0-1
- Update to 1.12.0 version

* Fri Nov 08 2019 Lijin Yang <yanglijin@huawei.com> -1.7.0-8
- Pakcage init

