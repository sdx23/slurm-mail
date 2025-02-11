%define debug_package %{nil}
%define rel 1

%if 0%{?sle_version} >= 150000 && 0%{?sle_version} < 160000
%define dist .sl15
%endif

Name:       slurm-mail
Version:    3.4
Release:    %{rel}%{?dist}
Summary:    Provides enhanced e-mails for Slurm
URL:        https://www.github.com/neilmunday/slurm-mail
Group:      System Environment/Base
License:    GPL v3.0
Packager:   Neil Munday

BuildArch:  noarch

Source: %{name}-%{version}.tar.gz

%{?el7:Requires: python3}
%{?el8:Requires: python38}
%{?sle_version:Requires: python3}
Requires:   cronie
Requires:   logrotate
Requires:   slurm-slurmctld

%description
Slurm-Mail is a drop in replacement for Slurm's e-mails to give users much more information about their jobs compared to the standard Slurm e-mails.

%prep
%setup -q

%build
# nothing to do here

%install
install -d -m 755 %{buildroot}/opt/slurm-mail/bin
install -m 755 bin/* %{buildroot}/opt/slurm-mail/bin/
install -d -m 700 %{buildroot}/opt/slurm-mail/conf.d/templates
install -m 600 conf.d/slurm-mail.conf conf.d/style.css %{buildroot}/opt/slurm-mail/conf.d/
install -m 600 conf.d/templates/* %{buildroot}/opt/slurm-mail/conf.d/templates
install -m 644 README.md %{buildroot}/opt/slurm-mail/
install -d -m 700 %{buildroot}/var/spool/slurm-mail
install -d -m 700 %{buildroot}/var/log/slurm-mail
touch %{buildroot}/var/log/slurm-mail/slurm-send-mail.log
touch %{buildroot}/var/log/slurm-mail/slurm-spool-mail.log
install -d -m 755 %{buildroot}/etc/cron.d
echo "*    *    *    *    *    root    /opt/slurm-mail/bin/slurm-send-mail.py" > %{buildroot}/etc/cron.d/slurm-mail
install -d m 755 %{buildroot}/etc/logrotate.d
install -m 644 logrotate.d/slurm-mail %{buildroot}/etc/logrotate.d/

# set permissions on directories?

%files
%defattr(-,root,root,0755)
/opt/slurm-mail/bin/*
%defattr(-,root,root,0644)
%config /etc/cron.d/slurm-mail
%config /etc/logrotate.d/slurm-mail
%config %attr(0640,root,slurm) /opt/slurm-mail/conf.d/slurm-mail.conf
%defattr(-,root,root,0600)
%config /opt/slurm-mail/conf.d/style.css
%dir %attr(0700,root,root) /opt/slurm-mail/conf.d/templates
%config /opt/slurm-mail/conf.d/templates/ended-array-summary.tpl
%config /opt/slurm-mail/conf.d/templates/ended-array.tpl
%config /opt/slurm-mail/conf.d/templates/ended.tpl
%config /opt/slurm-mail/conf.d/templates/invalid-dependency.tpl
%config /opt/slurm-mail/conf.d/templates/job-output.tpl
%config /opt/slurm-mail/conf.d/templates/job-table.tpl
%config /opt/slurm-mail/conf.d/templates/signature.tpl
%config /opt/slurm-mail/conf.d/templates/staged-out.tpl
%config /opt/slurm-mail/conf.d/templates/started-array-summary.tpl
%config /opt/slurm-mail/conf.d/templates/started-array.tpl
%config /opt/slurm-mail/conf.d/templates/started.tpl
%config /opt/slurm-mail/conf.d/templates/time.tpl
%defattr(-,root,root,0644)
%doc /opt/slurm-mail/README.md
%dir %attr(0700,slurm,slurm) /var/log/slurm-mail
%ghost /var/log/slurm-mail/slurm-send-mail.log
%ghost /var/log/slurm-mail/slurm-spool-mail.log
%dir %attr(0700,slurm,slurm) /var/spool/slurm-mail
