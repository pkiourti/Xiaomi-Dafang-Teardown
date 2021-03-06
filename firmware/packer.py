#!/usr/bin/env python
import click
import os
from sys import getsizeof


@click.command()
@click.argument('kernel', default="kernel.bin", type=click.Path(exists=True))
@click.argument('rootfs', default="rootfs.bin", type=click.Path(exists=True))
@click.argument('driver', default="driver.bin", type=click.Path(exists=True))
@click.argument('appfs', default="appfs.bin", type=click.Path(exists=True))
@click.argument('outfile', default="demo_5.5.1.177.bin")
def cli(kernel, rootfs, driver, appfs, outfile):
    dic = [
        ("kernel", 0x200000, click.format_filename(kernel)),
        ("rootfs", 0x350000, click.format_filename(rootfs)),
        ("driver", 0xa0000, click.format_filename(driver)),
        ("appfs", 0x4a0000, click.format_filename(appfs)),
    ]
    outfile = click.format_filename(outfile)
    tmpfile = "tmp.bin"
    fullflash = open(tmpfile, 'wb')
    for name, size, filename in dic:
        buffersize = os.path.getsize(filename)
        if (size != buffersize):
            click.echo('Size mismatch. The provided %s has a size of %s, but it need to have the size %s ' % (name,
                                                                                                              buffersize,
                                                                                                              size))
            return

        part = open(filename, "rb")
        buffer = part.read(size)


        fullflash.write(buffer)
    cmd = "mkimage -A MIPS -O linux -T firmware -C none -a 0 -e 0 -n jz_fw -d " + tmpfile + " " + outfile
    os.system(cmd)
    os.remove(tmpfile)


if __name__ == '__main__':
    cli()
    pass
