import sys,glob,os,subprocess,shutil,argparse
"""
Make a VLC playable MP4 formatted video file of all images 
in the root of a directory, ordered by modification date.
"""

def filenames(datadir):
    """Get filenames of all files in root of datadir (not subdirs)
    """
    fns = []
    for root, dirs, files in os.walk(datadir):
        for fn in files:
            fns.append(os.path.join(root,fn))
    return fns

if __name__ == '__main__':
    add_arg_kwargs = {'type':str,'default':None}
    parser = argparse.ArgumentParser(description='Make directory of images to mp4')
    parser.add_argument('source_dir',help='Directory of images',**add_arg_kwargs)
    parser.add_argument('dest_file',help='MP4 file to write to',**add_arg_kwargs)
    parser.add_argument('-f','--framerate',help='frames/second',type=int,default=7)
    parser.add_argument('-x','--extension',help='image extension',type=str,default='png')

    args = parser.parse_args()

    fns = filenames(args.source_dir)
    mtimes = [os.path.getmtime(fn) for fn in fns]
    fns_by_mtime = [fn for dum,fn in sorted(zip(mtimes,fns))]
    imgs_by_mtime = [fn for fn in fns_by_mtime if args.extension in fn]
    if len(imgs_by_mtime)==0:
        raise RuntimeError('No files with extension {}'.format(args.extension))

    with open('filelist.txt','w') as f:
        for fn in imgs_by_mtime:
            # if len(os.path.split(fn)[-1].split('_')) == 4:
            #     continue
            f.write("file '{}'\n".format(fn))
            f.write("duration {:.2f}\n".format(1./args.framerate))


    ff_args = " -f concat -safe 0 -i 'filelist.txt'"
    ff_args += ' -r {}'.format(args.framerate)
    ff_args += ' -c:v libx264 -pix_fmt yuv420p'
    ff_args += ' {}'.format(args.dest_file)

    ff_cmd = 'ffmpeg'+ff_args
    print(ff_cmd)
    subprocess.check_call(ff_cmd,shell=True)
