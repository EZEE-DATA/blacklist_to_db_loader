from downloader import download_blocked_ips, download_blocked_domains
from uploader import upload_blocked_ips, upload_blocked_domains
from settings_loader import load_variables_to_environment
from os.path import dirname, realpath


def main():
    settings_location = dirname(realpath(__file__)) + '/settings'
    print(f'Loading settings from {settings_location} ...')
    loaded_vars = load_variables_to_environment(settings_location)
    print(f'Loaded {len(loaded_vars)} vars')
    blocked_ips = download_blocked_ips(loaded_vars)
    print(f'Loaded {len(blocked_ips)} blocked ips')
    blocked_domains = download_blocked_domains(loaded_vars)
    print(f'Loaded {len(blocked_domains)} blocked domains')
    upload_blocked_ips(blocked_ips)
    print(f'Blocked ips uploaded to db')
    upload_blocked_domains(blocked_domains)
    print(f'Blocked domains uploaded to db')
    print(f'Script finished successfully!')
    return 0


if __name__ == '__main__':
    main()
