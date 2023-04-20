package { 'nginx':
  ensure   => 'installed',
  provider => 'apt',
}

file { '/var/www/html':
  ensure => 'directory',
}

file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n",
}

file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
}

file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => template('nginx/default.conf.erb'),
  require => Package['nginx'],
}

file { '/data':
  ensure  => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  require => [
    File['/data/web_static/releases/test/index.html'],
    File['/data/web_static'],
  ],
}

exec { 'chown -R ubuntu:ubuntu /data/':
  path    => ['/bin', '/usr/bin', '/usr/local/bin'],
  require => [
    File['/data/web_static'],
    File['/data/web_static/releases'],
    File['/data/web_static/releases/test'],
  ],
}

service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => [
    File['/etc/nginx/sites-available/default'],
    File['/var/www/html/index.html'],
    File['/data/web_static/current'],
  ],
}

