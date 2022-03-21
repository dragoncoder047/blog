Date: 2021-09-15
Title: Updating Python

After I bought myself my Raspberry Pi, I soon figured out that the only version of Python available on the Debian package repositories was 3.7.2, but as of when I wrote this it is already on 3.9.7. So, I was forced to compile from source.

The process to do this is very time consuming, so I made a shell script to do it automatically, as per the instructions on the Python website.

Here's the script: [update-python.sh]({attach}update-python.sh){download="update-python.sh"}

Save it in someplace convenient (like `~/.local/bin/update-python.sh`). Then, run the following in your terminal to add the file as a command:

<!-- cSpell:ignore raspberrypi chmod -->

```bash
chmod +x ~/.local/bin/update-python.sh #make it executable
echo 'alias update-python=". ~/.local/bin/update-python.sh"' > ~/.bashrc #let your shell find it
. ~/.bashrc #re-initialize the shell
```

The first argument to the script is the version of Python you want to install, such as 3.9.7:

```bash
update-python 3.9.7
```

This will install Python 3.9.7 as `python3`.
