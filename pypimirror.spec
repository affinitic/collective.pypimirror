%define __prelink_undo_cmd %{nil}
%define init_name cerise
%define installdir /var/www/html/pub/%{name}
%define python python2.6
%define virtualenv virtualenv

Name: %{name}
Version: %{ver}
Release: %{rel}
Summary: Pypi Mirror
URL: http://www.pypi-mirrors.org
License: GPL
Vendor: Affinitic
Packager: affinitic <info@affinitic.be>
Group: Applications/Database
Source: %{name}-%{version}.tar.gz
BuildRequires:  python-devel, python-virtualenv
AutoReqProv: no

%description
%{summary}

%prep
%setup

%build
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{installdir}
%{virtualenv} -p /usr/bin/%{python} $RPM_BUILD_ROOT%{installdir}
mkdir -p $RPM_BUILD_ROOT%{installdir}/downloads
cp pypimirror.cfg.in $RPM_BUILD_ROOT%{installdir}
$RPM_BUILD_ROOT%{installdir}/bin/%{python} bootstrap.py
bin/buildout -N -c buildout.cfg buildout:directory=$RPM_BUILD_ROOT%{installdir} buildout:rpm-directory=%{installdir}

%install
sed -i s/${RPM_BUILD_ROOT//\//\\/}//g $RPM_BUILD_ROOT%{installdir}/bin/pypimirror
cp -r $RPM_BUILD_DIR/%{name}-%{version}/eggs/zc.buildout* $RPM_BUILD_ROOT%{installdir}/lib/python2.6/site-packages
cd $RPM_BUILD_ROOT%{installdir}/
rm lib64
ln -s lib lib64
# uncomment following line if using omelette in your buildout.cfg
for i in $(find parts/omelette -type l); do old_link=$(readlink $i); new_link=$(echo $old_link | sed  s/${RPM_BUILD_ROOT//\//\\/}//); rm $i; ln -f -s $new_link $i; done
#symlinks -c parts/omelette
for i in $(find parts/python-oracle -type l); do old_link=$(readlink $i); new_link=$(echo $old_link | sed  s/${RPM_BUILD_ROOT//\//\\/}//); rm $i; ln -f -s $new_link $i; done
rm  $RPM_BUILD_ROOT%{installdir}/.installed.cfg
rm -fr $RPM_BUILD_ROOT%{installdir}/downloads
rm -fr $RPM_BUILD_ROOT%{installdir}/parts/docs
rm -fr $RPM_BUILD_ROOT%{installdir}/.git
rm -fr $RPM_BUILD_ROOT%{installdir}/pypimirror.cfg.in
find $RPM_BUILD_ROOT%{installdir} -name "*.pyc" -print -delete;
find $RPM_BUILD_ROOT%{installdir} -name "*.pyo" -print -delete;

%files
%defattr(-, pypi, pypi, 0755)
%{installdir}/bin  
%{installdir}/develop-eggs
%{installdir}/eggs
%{installdir}/include  
%{installdir}/lib  
%{installdir}/lib64
%{installdir}/pypimirror.cfg

%pre
/usr/sbin/groupadd -r pypi &>/dev/null || :
/usr/sbin/useradd  -r -s /sbin/nologin  -M \
    -c 'pypi user' -g pypi pypi &>/dev/null || :
exit 0

%clean
#rm -rf $RPM_BUILD_ROOT%{installdir} $RPM_BUILD_ROOT/etc

%changelog

