# WebWatcher
## A utility for watching a list of websites for changes

### Setup

1. Rename `config.sample.yml` to `config.yml`
2. Add your gmail email and password to the config file
3. Add a single or a comma-separated list of recipients to the config file
4. (Optionally) edit the subject. Make sure to add a `%s`-sign somewhere, where the time will be displayed.
5. Edit the cookies in the config.
6. Make sure that "less secure" applications can log in with your credentials by visiting [https://www.google.com/settings/security/lesssecureapps](https://www.google.com/settings/security/lesssecureapps) and selecting **Turn on**.
7. Create a list of urls separated by a newline.
8. (Possibly) install the missing PyYAML dependency by running `pip install pyyaml`
9. Pass it into webwatcher by running `python webwatcher.py /path/to/file.txt`
