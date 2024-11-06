import subprocess
import argparse
import datetime
import os

def run_command(command, output_file):
    """Runs a shell command and saves the output to a file."""
    try:
        print(f"Running command: {command}")
        with open(output_file, "w") as file:
            result = subprocess.run(command, shell=True, stdout=file, stderr=subprocess.STDOUT, text=True)
            if result.returncode == 0:
                print(f"Command completed successfully. Output saved to {output_file}.")
            else:
                print(f"Command failed with return code {result.returncode}. Check {output_file} for details.")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_output_filename(domain):
    """Generates a timestamped output filename based on the domain."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{domain}_{timestamp}.txt"

def run_amass_enum(domain, options):
    """Runs the Amass enum subcommand with specified options.

    Args:
        domain (str): The target domain.
        options (str): Additional Amass options.
    """
    output_dir = "Amass_Output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, generate_output_filename(domain))
    command = f"amass enum -d {domain} -o {output_file} {options}"

    run_command(command, output_file)

def main():
    parser = argparse.ArgumentParser(description="Automate Amass enum subcommands with various options.")
    parser.add_argument("domain", help="The target domain")
    parser.add_argument("-active", action="store_true", help="Attempt zone transfers and certificate name grabs")
    parser.add_argument("-aw", type=str, help="Path to a different wordlist file for alterations")
    parser.add_argument("-brute", action="store_true", help="Enable brute force mode")
    parser.add_argument("-p", type=str, help="Ports separated by commas (default: 80, 443)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-ip", action="store_true", help="Show the IP addresses for discovered names")
    parser.add_argument("-ipv4", action="store_true", help="Show the IPv4 addresses for discovered names")
    parser.add_argument("-ipv6", action="store_true", help="Show the IPv6 addresses for discovered names")
    parser.add_argument("-passive", action="store_true", help="A purely passive mode of execution")
    parser.add_argument("-o", "--output_prefix", help="Output file prefix (default: target_timestamp.txt)")

    args = parser.parse_args()

    options = ""
    if args.verbose:
        options += "-v "
    if args.brute:
        options += "-brute "
    if args.active:
        options += "-active "
    if args.passive:
        options += "-passive "
    if args.aw:
        options += f"-aw {args.aw} "
    if args.p:
        options += f"-p {args.p} "
    if args.ip:
        options += "-ip "
    if args.ipv4:
        options += "-ipv4 "
    if args.ipv6:
        options += "-ipv6 "

    output_prefix = args.output_prefix or generate_output_filename(args.domain)

    run_amass_enum(args.domain, options)

if __name__ == "__main__":
    main()
