# DNSMin

## Configuration Guide

### Introduction

The application provides a lot of fluidity in how it can be configured. This remains true for both environment
and runtime configuration. The application is designed to be flexible and allow for a wide variety of
deployment scenarios which include bare metal, virtual machines, containers, and cloud environments.

There is a plethora of environment configuration settings that can be used to bootstrap the application for
varying environments. All of these settings can be set using environment variables or by creating a
`.env` file in the root directory of the application that contains one or more environment variables to be
loaded at application startup. For more information on these settings, see the
[Environment Configuration Guide](https://github.com/dnsmin/dnsmin-api/blob/main/docs/wiki/configuration/settings/environment-settings.md)
section.

If you want to change the default path of the `.env` file, you can set the ` DNSMIN_ENV_FILE` environment variable
to the path of the file you want to use. If a relative path is provided, it will be relative to the
root directory of the application. Furthermore, if you want to use a different file encoding other than `UTF-8`,
you may do so by setting the ` DNSMIN_ENV_FILE_ENCODING` environment variable to the encoding you want to use.

#### Secrets Support

Additionally, there is support for secure settings to be kept in a filesystem location using a convention
similar to Docker-style secrets. To use this feature, you simply create a file with the same name as the
application setting you want to set and store it in the directory specified by the `env_secrets_dir` setting
or the ` DNSMIN_ENV_SECRETS_DIR` environment variable.

So for example, say you want to set the value of an application setting named `example_option`.
Assuming that `env_secrets_dir` or ` DNSMIN_ENV_SECRETS_DIR` is set to `/var/run/secrets`, one would create a file
named `example_option` and store it in the `/run/secrets` directory. The contents of the file would be
the value of the `example_option` setting. The application will automatically detect the file and use its
contents as the value of the setting.

### Application Settings

To get an in-depth understanding of the many application settings available, see the
[Application Settings Guide](https://github.com/dnsmin/dnsmin-api/blob/main/docs/wiki/configuration/settings/README.md).

#### Environment Configuration

To view the alphabetical list of environment configuration settings, see the
[Environment Configuration Guide](https://github.com/dnsmin/dnsmin-api/blob/main/docs/wiki/configuration/settings/environment-settings.md).

### Getting Started

To get an environment set up for running the API server and associated processes, you'll need to start by creating the
appropriate configuration files. The first of these files is the environment configuration file.

To create a local development environment, run the following command from the application root directory:

```bash
cp .env.local.tpl .env
```

To create a production environment, run the following command from the application root directory:

```bash
cp .env.tpl .env
```

Once you have created the environment file, you'll need to update some of the variables in it. Start by setting the
`DNSMIN_SERVICE_IP` variable to an IP address that is actively assigned to the network interface that you'll use to
access the application. This should **not be set** to any local loopback address such as `127.0.0.1` if you're running
the application inside of containers. Additionally, a secure password should be set for the `MYSQL_PASSWORD` variable
which will be used for the local MySQL database.

You are free to exclude MySQL in favor of Postgres or SQLite if desired.

The next step is creating the configuration files for the application which can be done with the following commands
from the application root directory:

```bash
cp config/config.tpl.yml config/config.yml
cp config/notifications.tpl.yml config/notifications.yml
cp config/schedules.tpl.yml config/schedules.yml
```

At this point you'll need to update some configuration settings in the `config/config.yml` file depending on your
environment. This guide will assume you're running the application in containers so a minimalistic approach will be
taken. Two settings that will need updated to reflect your database configuration are `db.sql_async_url`
and `db.sql_sync_url`.

If you're using the default approach with a MySQL database, then you'll use the following values with the password
updated accordingly to what you previously set in the `.env` file.

```yaml
db:
  sql_async_url: mysql+asyncmy://root:YOUR-MYSQL-PASSWORD@mysql/dnsmin
  sql_sync_url: mysql+pymysql://root:YOUR-MYSQL-PASSWORD@mysql/dnsmin
```

You'll likely also want to update the `logging.level` setting to either `debug` or `trace` to provide enhanced
logging detail during development. There are many other settings in this file that you might also want to update
depending on your use case such as mail server settings.
