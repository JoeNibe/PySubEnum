import os
import asyncio
import argparse
import configparser
import log as logg
from colorama import Fore, init
init()
log = logg.setup_logger(filename="log", con_level=3, file_level=4)


def welcome():
    message = ("\n"
               " \n"
               "██████╗░██╗░░░██╗  ░░░░░░  ░██████╗██╗░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗\n"
               "██╔══██╗╚██╗░██╔╝  ░░░░░░  ██╔════╝██║░░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║\n"
               "██████╔╝░╚████╔╝░  █████╗  ╚█████╗░██║░░░██║██████╦╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║\n"
               "██╔═══╝░░░╚██╔╝░░  ╚════╝  ░╚═══██╗██║░░░██║██╔══██╗██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║\n"
               "██║░░░░░░░░██║░░░  ░░░░░░  ██████╔╝╚██████╔╝██████╦╝███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║\n"
               "╚═╝░░░░░░░░╚═╝░░░  ░░░░░░  ╚═════╝░░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝\n"
    )
    print(f"{Fore.LIGHTBLUE_EX}{message}{Fore.RESET}")


async def run_cmd(semaphore, cmd, tool=""):
    async with semaphore:
        process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE, executable='/bin/bash')

        log.run(f"{tool} Started")
        await process.communicate()
    if process.returncode != 0:
        log.error(f'{tool} returned non-zero exit code: {process.returncode}')
    else:
        log.good(f"{tool} completed successfully")
    return process.returncode


def get_output(outputs):
    log.debug(outputs)
    subdomains = set()
    for file in outputs:
        if os.path.exists(file):
            subs = [line.strip() for line in open(file, 'r').readlines()]
            subdomains.update(subs)
    log.debug(f"Length {len(subdomains)}")
    return subdomains


async def launch_tasks(semaphore, cmds, outputs, tools, out_file="final"):
    await asyncio.gather(*(run_cmd(semaphore, c, tool=tool) for c, tool in zip(cmds, tools)))
    subdomains = get_output(outputs)
    log.good(f"{len(subdomains)} Subdomains discovered")
    log.good("Running IP checks on discovered subdomains")
    ip_list = await asyncio.gather(*(check_ip(host) for host in subdomains))
    count = 0
    with open(out_file, 'w') as f:
        for sub, ip in ip_list:
            if ip != 'Err':
                count += 1
            f.write(f"{sub},{ip}\n")
    log.good(f"{count} Subdomains with IPs discovered")
    log.good(f"Output written to file final")


async def check_ip(host):
    try:
        loop = asyncio.get_event_loop()
        result = await loop.getaddrinfo(host, 80)
        ip = result[0][-1][0]
        return host, ip
    except Exception as e:
        return host, 'Err'


def read_config(config_file):
    tools = []
    cmds = []
    outputs = []
    config = configparser.ConfigParser()
    config.read(config_file)
    for value in config.sections():
        tools.append(value)
        cmds.append(config[value]['cmd'].replace('{OUTPUT}', config[value]['output']))
        outputs.append(config[value]['output'])
    return tools, cmds, outputs


def main():
    welcome()
    parser = argparse.ArgumentParser(
        description='Python Wrapper script run a bunch of subdomain enumeration tools and consolidate the output')
    parser.add_argument('-i', '--input', action='store', type=str, default='', dest='input_file',
                        help='Input file with the target subdomains.', required=True)
    parser.add_argument('-c', '--config', action='store', type=str, default='config.ini', dest='config',
                        help='The config file that contains the commands and output files. Default: %(default)s')
    parser.add_argument('-ct', '--concurrent-tools', action='store', metavar='<number>', type=int, default=2,
                        help='The maximum number of tools to launch concurrently. Default: %(default)s')
    parser.add_argument('-o', '--output', action='store', default='results', dest='subdomains_final',
                        help='The output file. Default: %(default)s')

    args = parser.parse_args()
    tools, cmds, outputs = read_config(args.config)

    # replace INPUT with the filename
    for i in range(len(cmds)):
        cmds[i] = cmds[i].replace('{INPUT}', args.input_file)

    # remove the output files it it already exists
    for out in outputs:
        if os.path.exists(out):
            os.remove(out)

    # Get event loop for current process.
    loop = asyncio.get_event_loop()

    # Create a semaphore to limit number of concurrent process.
    semaphore = asyncio.Semaphore(2)
    try:
        loop.run_until_complete(launch_tasks(semaphore, cmds, outputs, tools, out_file=args.subdomains_final))
        log.run('Finished scanning target')
    except KeyboardInterrupt:
        log.error("Received keyboard interrupt. Exiting !!")
        exit()
    finally:
        loop.close()


main()
