import os
import subprocess
import sys


def require_pmd() -> bool:
    install_pmd_if_missing()
    if os.system("which pmd") != 0:
        print("PMD is not installed. Please install it and try again.")
        return False
    return True


def install_pmd_if_missing() -> None:
    """
    Install PMD if it is not installed
    Reference: https://pmd.github.io/
    :return: None
    """
    if sys.platform == "linux" or sys.platform == "darwin":
        # Check for jq
        if os.system("which jq") != 0:
            print("jq is not installed. Run 'sudo apt-get install jq' to install it.")
            sys.exit(1)

        if os.system("which pmd") != 0:
            latest_version = get_latest_pmd_version_from_github()

            # Check local installation
            if os.path.exists(f"{os.environ['HOME']}/pmd"):
                # Get local version
                local_version = os.popen(f"{os.environ['HOME']}/pmd/pmd-bin-*/bin/pmd --version | grep PMD | awk '{{print $2}}'").read().strip()
                if local_version == latest_version:
                    print(f"PMD is already installed with version {latest_version}")

                    if "pmd" not in os.popen("echo $PATH").read():
                        os.system(f"echo 'export PATH=$HOME/pmd/pmd-bin-{latest_version}/bin:$PATH' >> $HOME/.bashrc")
                        os.system("source $HOME/.bashrc")
                        print("PMD added to PATH")
                    return
                else:
                    print(f"PMD is installed with version {local_version}. Installing version {latest_version}")

            print(f"PMD is not installed. Installing version {latest_version}")

            pmd_url = f"https://github.com/pmd/pmd/releases/latest/download/pmd-dist-{latest_version}-bin.zip"
            os.system(f"wget {pmd_url} -O $HOME/pmd.zip")
            os.system("unzip $HOME/pmd.zip -d $HOME/pmd")
            os.system("rm $HOME/pmd.zip")

            if "pmd" not in os.popen("echo $PATH").read():
                os.system(f"echo 'export PATH=$HOME/pmd/pmd-bin-{latest_version}/bin:$PATH' >> $HOME/.bashrc")
                os.system("source $HOME/.bashrc")

            print("PMD installed successfully")
    elif sys.platform == "win32":
        pass


def get_latest_pmd_version_from_github() -> str:
    command = "curl -s https://api.github.com/repos/pmd/pmd/releases/latest | jq -r '.tag_name' | cut -d \"/\" -f 2"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    version = result.stdout.decode("utf-8").strip()
    return version
