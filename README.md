# PySubEnum

## What is this ? 
A python tool that uses AsnycIO to launch a bunch of SubDomain tools and aggregates the output. It also resolves the IPs before writing to the output file. New tools can be added by installing them on your system then editing the config file.

## Why ?
1. I wanted to run a bunch of tools and all the scripts I found had way too much unnecessary functionalities. So I wrote this simple script that can launch tools and get the output. 

2. I really wanted to learn python AsyncIO and this seemed to be a good opportunity.

## How does this work?
The tool reads the `config.ini` file and launches all the tools mentioned in it. All tools to be run must be installed and present in PATH. Current config launches the following tools.

[Assetfinder](https://github.com/tomnomnom/assetfinder)  
[Amass](https://github.com/OWASP/Amass/)  
[Subfinder](https://github.com/subfinder/subfinder)  
[Sublist3r](https://github.com/aboul3la/Sublist3r)  
[Crobat](https://github.com/cgboal/sonarsearch)  

The current config looks like this.

```py
[Assetfinder]
cmd:while IFS= read -r line; do assetfinder $line >> {OUTPUT}; done < {INPUT}
output:assetfinder.out

[Amass]
cmd:amass enum -active -nolocaldb -o {OUTPUT} -df {INPUT}
output:amass.out

[Subfinder]
cmd:subfinder -dL {INPUT} -all -o {OUTPUT}
output:subfinder.out

[Sublist3r]
cmd:while IFS= read -r line; do python3 -m sublist3r -d $line -o sublister.tmp;cat sublister.tmp>>{OUTPUT}; done < {INPUT}
output:sublister.out

[Crobat]
cmd:crobat -s {INPUT} > {OUTPUT}
output: crobat.out
```


The general format is 
```
[Tool Name]
cmd:command to run the tool {INPUT} {OUTPUT}
output: file to write output to
```

If you are adding a new tools, the `{INPUT}` and `{OUTPUT}` keywords must be present and the tool must be installed and be present in `PATH`.

## How to use this ?

1. Requires python3
2. Install dependencies
    ```
    pip install -r requirements.txt
    ```
3. Make sure that all tools in config has been installed and available on `PATH`
4. Launch the tool

```
> python3 pysubenum.py -i input.txt -o output.txt


██████╗░██╗░░░██╗  ░░░░░░  ░██████╗██╗░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗
██╔══██╗╚██╗░██╔╝  ░░░░░░  ██╔════╝██║░░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║
██████╔╝░╚████╔╝░  █████╗  ╚█████╗░██║░░░██║██████╦╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║
██╔═══╝░░░╚██╔╝░░  ╚════╝  ░╚═══██╗██║░░░██║██╔══██╗██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║
██║░░░░░░░░██║░░░  ░░░░░░  ██████╔╝╚██████╔╝██████╦╝███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║
╚═╝░░░░░░░░╚═╝░░░  ░░░░░░  ╚═════╝░░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝

[ ] Assetfinder Started
[ ] Amass Started
[++] Assetfinder completed successfully
[ ] Subfinder Started
[++] Subfinder completed successfully
[ ] Sublist3r Started
[++] Sublist3r completed successfully
[ ] Crobat Started
[++] Crobat completed successfully
[++] Amass completed successfully
[++] 178 Subdomains discovered
[++] Output written to file final
[ ] Finished scanning target
```

Additional arguments can be viewed using `-h`

```
██████╗░██╗░░░██╗  ░░░░░░  ░██████╗██╗░░░██╗██████╗░███████╗███╗░░██╗██╗░░░██╗███╗░░░███╗
██╔══██╗╚██╗░██╔╝  ░░░░░░  ██╔════╝██║░░░██║██╔══██╗██╔════╝████╗░██║██║░░░██║████╗░████║
██████╔╝░╚████╔╝░  █████╗  ╚█████╗░██║░░░██║██████╦╝█████╗░░██╔██╗██║██║░░░██║██╔████╔██║
██╔═══╝░░░╚██╔╝░░  ╚════╝  ░╚═══██╗██║░░░██║██╔══██╗██╔══╝░░██║╚████║██║░░░██║██║╚██╔╝██║
██║░░░░░░░░██║░░░  ░░░░░░  ██████╔╝╚██████╔╝██████╦╝███████╗██║░╚███║╚██████╔╝██║░╚═╝░██║
╚═╝░░░░░░░░╚═╝░░░  ░░░░░░  ╚═════╝░░╚═════╝░╚═════╝░╚══════╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝

usage: asycprocess.py [-h] -i INPUT_FILE [-c CONFIG] [-ct <number>] [-o SUBDOMAINS_FINAL]

Python Wrapper script run a bunch of subdomain enumeration tools and consolidate the output

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        Input file with the target subdomains.
  -c CONFIG, --config CONFIG
                        The config file that contains the commands and output files. Default: config.ini
  -ct <number>, --concurrent-tools <number>
                        The maximum number of tools to launch concurrently. Default: 2
  -o SUBDOMAINS_FINAL, --output SUBDOMAINS_FINAL
                        The output file. Default: results

```