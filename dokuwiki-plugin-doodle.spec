%define		plugin		doodle
%define		php_min_version 5.0.0
Summary:	DokuWiki doodle plugin: Easy scheduling
Name:		dokuwiki-plugin-%{plugin}
Version:	20110101
Release:	7
License:	GPL v2
Group:		Applications/WWW
Source0:	http://public.doogie.de/projects/dokuwiki/doodle-latest.tar.gz
# Source0-md5:	af99dac9cc7249d5130b420268f7c03e
URL:		http://www.dokuwiki.org/plugin:doodle2
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
BuildRequires:	unzip
Requires:	dokuwiki >= 20061106
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# no pear deps
%define		_noautopear	pear
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
With this plugin you can offer your visitors a poll, where each user
can vote for one (or more) choices. This is a unification of the
doodle, vote, and userpoll plugins.

%prep
%setup -qc
mv %{plugin}/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/VERSION

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

# use this post section if you package .css or .js files
%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/*.php
%{plugindir}/*.txt
