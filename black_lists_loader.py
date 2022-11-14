from downloader import download_blocked_ips, download_blocked_domains
from uploader import upload_blocked_ips, upload_blocked_domains
from settings_loader import load_variables_to_environment
from os.path import dirname, realpath


def main():
    settings_location = dirname(realpath(__file__)) + '/settings'
    loaded_vars = load_variables_to_environment(settings_location)
    blocked_ips = download_blocked_ips(loaded_vars)
    blocked_domains = download_blocked_domains(loaded_vars)
    upload_blocked_ips(blocked_ips)
    upload_blocked_domains(blocked_domains)
    return 0


if __name__ == '__main__':
    main()
