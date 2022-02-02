
def file_categories(file_ext):
    CATEGORIES = { 'Executable':['.so', '.cu', '.mo','.exe','preinst', 'postinst', 'prerm', 'postrm','.debian', '.dep\s', '.sip', '.cmd', '.dlg', '.dll', '.flt', '.map','.o\s', '.a\s', '.a.', '.ubuntu'],
                   'Model and Weights':[ '.pb',  '.hdf5', '.pkl', '.mlmodel','model', '.onnx', '.pmml', '.pt', 'joblib', 'pickle', '.npy', '.tfrecords', '.h5', '.ph', '.proto', 'pbtxt'],
                   'python':['.py', '.cpython', 'python','.ipynb','.pyi', '.ipynb','.pyi', 'gpg', '.cs', '.java', '.css',  '.go', '.el', '.awk','.h\s','.h.','.c\s', '.hpp','.pl',  '.pm', '.pmk', '.pre\s', '.java', '.jar', '.jnl','.js', 'makefile', 'cmake', '.mk','.class', '.cc'],
                   '.mod':['.mod'],

                   'Archival':['.whl', '.zip', '.gzip', '.tar', '.xz', '.bzip', '.bz2'],
                   'OBJ':['.mtl', '.obj', '.urdf'],
                   'Test':['test', 'tox.'],
                   'Encryption': ['.md5', '.pem', 'gpg', '.enc'],
                   'wh':['.wh'],
                   'qmlc':['.qmlc'],
                   'vf':['.vf'],
                   'htf':['.htf'],
                   '.conda':['.conda'],
                   '.pack':['.pack'],
                   '3D FileExt':['.dae', '.stp'],
                   'Data File':['.wav', '.json', '.txt', '.csv', '.xls','.dat','.info', '.log'],
                   '.symbols':['.symbols'],
                   'Conf':['.toml', '.yml', '.vim','.urdf', '.sh', '.conf'],
                   'Document':['.html', '.xml', '.xhtml', '.pdf', '.ps', '.md',  '.bib', 'changelog', '.rst', 'license', 'readme', 'record', 'metadata', '.tcc', 'copyright', '.pod', '.pfb', '.qbk', '.bk', '.tex','.doc', '.cgi', '.asc'],
                   'Image':['.png', '.jpeg', '.svg', '.fits', '.tiff', '.eps', '.gif', '.pic', '.ico', '.fig', '.tif', '.xbm', '.jpg']
                   }

    file_type = file_ext
    for key, val in CATEGORIES.items():
        for v in val:
            if str(v).lower() in str(file_ext).lower():
                file_type = key
                break
    return file_type


def file_categories2(file_ext):
    CATEGORIES = {
        # 'executable': ['exe', '.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.gadget', '.jar', '.msi', '.wsf',
        #               'instal'],
        '.cu': ['.cu'],
        'cmd': ['.cmd'],
        '.email': ['.email', '.eml', '.emlx', '.msg', '.oft', '.ost', '.pst', '.vcf'],
        # 'dlg': ['.dlg', '.dll', '.sip'],
        'cc1': ['cc1'],
        # 'flt': ['.flt'],
        'ELF/COFF': ['.axf', '.bin', '.elf', '.o', '.out', '.prx', '.puff', '.ko', '.mod', '.so', 'mo', '.lib', 'dylib',
                     '.bundle', '.acm', '.ax', '.cpl', '.dll', '.drv', '.efi,' '.exe', '.mui', '.ocx', '.scr', '.sys',
                     '.tsp', '-system.', '.dlg', '.dll', '.sip', '.iso', '.toast', '.vcd', '.bin', '.dmg'],
        '.map': ['.map'],
        'Ubuntu': ['ubuntu', '.ubuntu'],
        'alpine': ['alpine'],
        'Fortran': ['.f.', '.f90', 'gfortran'],
        'debian': ['preinst', 'postinst', 'prerm', 'postrm', '.dep', '.debian', '.deb', 'dpkg'],
        '.rpm': ['.rpm'],
        '.pkg': ['.pkg'],
        'Model/ Weight': ['.pb', '.hdf5', '.pkl', '.mlmodel', 'model', '.pmml', '.pt', 'joblib', 'pickle', '.onnx',
                          'proto', '.tfrecords', '.h5', '.ph', '.proto', 'pbtxt', '.ckpt'],
        'Python': ['.py', '.cpython', '.ipynb', '.pyi', '.ipynb', '.pyi'],
        '.mod': ['.mod'],
        'PEP': ['site-packages', 'python', '.abi3', '.abi3.', '.toml'],
        'whl': ['.whl', 'wheel'],
        'GPG': ['gpg'],
        'lisp': ['.el'],
        'apt': ['apt'],
        '6m': ['.6m'],
        '.min': ['.min', '.min.'],
        'C/C++': ['.h.', '.hpp', '.cc', '.obj', '.cpp', '.cxx', '.hxx', 'cpp', 'clang', 'c++'],
        'Java': ['.java', '.jar', '.jnl', '.class', '.pack'],
        'css': ['.css'],
        'Ssh/OpenSSh': ['openssl', 'ssh', 'openssh'],
        'Php': ['.php'],
        'sh/': ['.sh'],
        'VB/.Net': ['.vb'],
        'Swift': ['.swift'],
        'ovms': ['ovms'],
        'Perl': ['.pl', '.pm', '.pmk', '.pre', '.perl', 'perl'],
        'Awk': ['.awk'],
        'Makefile': ['makefile', 'cmake', '.mk', 'qmake', '.pmk', '.make', 'cpack', 'ctest'],
        'Goland': ['.go'],
        'Ruby': ['.rb'],
        'Julia': ['julia', '.jl'],
        'Matlab': ['.m.', '.mat'],
        'libcudnn': ['libcudnn'],
        'bin': ['/bin'],
        # '.build':['.build'],
        'gcc': ['gcc', 'g++', 'gcov'],
        'lib': ['/lib', '.build'],
        'qdrant': ['qdrant'],
        '.service': ['.service'],
        'docker': ['docker'],
        'YML': ['.yaml', '.yml'],
        'archive': ['.zip', '.gzip', '.tar', '.xz', '.bzip', '.bz2', '.7z', '.arj', '.rar', '.tar.gz', '.gz'],
        '.mtl': ['.mtl'],
        '.urdf': ['urdf'],
        # '.mf': ['.mf'],
        # 'Test': ['test', 'tox.'],
        'certif/ keys': ['passwd', '.md5', 'gpg', '.enc', '.crt', '.3ssl', '.key', '.keystore', '.jks', '.p12', '.pfx',
                         '.csr', '.der', 'crt', '.cer', '.ca-bundle', '.p7b', '.p7c', '.p7s', '.pem', 'chsh', 'cert',
                         '.7m', 'security', '.pwd'],
        'wh': ['.wh'],
        'qmlc': ['.qmlc'],
        '.vf': ['.vf'],
        '.htf': ['.htf'],
        'pip': ['pip'],
        '.sh': ['.sh'],
        'core': ['core', '/core'],
        'cache': ['.cache'],
        'pandoc': ['pandoc'],
        '3D': ['.stl', '.dae', '.stp', '.obj', '.fbx', '3ds', '.iges', '.step', 'vrml', '.x3d', '.3dmf', '.3dm', '.3mf',
               '.3ds', '.ac', '.amf', '.an8', '.aoi', '.asm', '.b3d', '.blend', '.block', '.bmd', '.bdl', '.brres',
               '.c4d', '.cal3d', '.cob', '.core3d', '.dpm', '.fac', '.fbx', '.xsh', '.mf', '.flt'],
        '.conda': ['.conda'],
        # 'disc/media': ['.iso', '.toast', '.vcd', '.bin', '.dmg'],
        'Data/ DB': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml', '.json',
                     '.txt', '.xls', 'info', '.xlsm', '.ods', '.pak',
                     '.accdb', '.fdb', '.sdf', '.fp3', '.gdb', '.ibd', '.wdb', '.myd', '.idx', '.cdb', '.dbf',
                     '.bsd', '.npz', '.pdb', '.dcm', 'sql', 'data','.npy'],
        'Font': ['.ttf', '.fnt', '.fon', '.otf', '.tfm', '.pfa', '.pfb', '__db'],
        '.wad': ['.wad'],
        'Video': ['.idx', '.mov', '.mp4', '.m4a', '.m4v', '.mpg', '.mpeg', '.wmv', '.avi', '.flv', '.3gp', '.3gpp',
                  '.3g2', '.3gp2', '.rm', '.swf', '.vob', '.wmv'],

        'Audio': ['.mp3', '.wav', '.aif', '.cda', '.mid', '.mp3', '.mpa', '.ogg', '.wma', '.wpl', '.sty'],
        '.symbols': ['.symbols', 'symbolic'],
        # 'Config': ['.vim', '.conf', '.cfg', ],
        'DOC': ['.pdf', '.ps', '.md', '.bib', 'changelog', '.rst', 'license', 'readme',
                'record', 'metadata', '.tcc', 'copyright', '.pod', '.pfb', '.qbk', '.bk', '.tex', '.doc', '.cgi',
                '.asc'],
        'Git': ['git'],
        '.patch': ['patch'],
        '.npm': ['.npm'],
        'systemctl': ['systemctl'],
        'gorse-': ['gorse-master', 'gorse-server', 'gorse-worker'],
        'Node/js': ['.js', '.node', 'nodejs'],
        'Rust': ['.rs'],
        '.jsp': ['.jspx', '.jspf', 'jsp'],
        'Html/Xml': ['.htm', '.html', '.xhtml'],
        'rss': ['.rss'],
        'image': ['.png', '.jpeg', '.svg', '.fits', '.tiff', '.eps', '.gif', '.pic', '.ico', '.fig', '.tif', '.xbm',
                  '.bmp', '.ai', '.ps', '.psd', '.tif', '.tiff',
                  '.jpg', '.xpm', '.pgm'],
        'Web': ['.asp', '.war', '.cfm', '.cgi', '.part', '.apache'],
        'ppt': ['.odp', '.pps', '.ppt', '.pptx']
    }

    file_type = str(file_ext)
    if '.c' == file_type or '.C' == file_type or '.h' == file_type or 'cs' == file_type or '.hpp' == file_type or '.cpp.' in file_type or '.o' == file_type or '.o.' in file_type or file_type.endswith(
            '.o') or file_type.endswith('cc') or file_type == 'cp':
        return 'C/C++'
    elif '.a' == file_type or '.a.' in file_type or file_type.endswith('.a'):
        return '.a'
    elif '.mo' == file_type or '.mo.' in file_type:
        return 'ELF/COFF'
    elif '.z' == file_type or '.z.' in file_type:
        return 'Archival'
    elif '.f' == file_type:
        return 'Fortran'
    elif '.m' == file_type or file_type.endswith('.m'):
        return 'Matlab'
    elif file_type.endswith('node'):
        return 'Node/js'
    else:
        flag = 0
        for key, val in CATEGORIES.items():
            for v in val:
                if str(v).lower() in str(file_ext).lower():
                    file_type = key
                    flag += 1
                    break
        return file_type


def file_categories_dir(file_path):
    CATEGORIES = {
        # 'executable': ['exe', '.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.gadget', '.jar', '.msi', '.wsf',
        #               'instal'],
        '.cu': ['.cu'],
        'cmd': ['.cmd'],
        '.email': ['.email', '.eml', '.emlx', '.msg', '.oft', '.ost', '.pst', '.vcf'],
        # 'dlg': ['.dlg', '.dll', '.sip'],
        'cc1': ['cc1'],
        # 'flt': ['.flt'],
        'ELF/COFF': ['.axf', '.bin', '.elf', '.o', '.out', '.prx', '.puff', '.ko', '.mod', '.so', 'mo', '.lib', 'dylib',
                     '.bundle', '.acm', '.ax', '.cpl', '.dll', '.drv', '.efi,' '.exe', '.mui', '.ocx', '.scr', '.sys',
                     '.tsp', '-system.', '.dlg', '.dll', '.sip', '.iso', '.toast', '.vcd', '.bin', '.dmg'],
        '.map': ['.map'],
        'Ubuntu': ['ubuntu', '.ubuntu'],
        'alpine':['alpine'],
        'Fortran': ['.f.', '.f90', 'gfortran'],
        'debian': ['preinst', 'postinst', 'prerm', 'postrm', '.dep', '.debian', '.deb', 'dpkg'],
        '.rpm': ['.rpm'],
        '.pkg': ['.pkg'],
        'Model/ Weight': ['.pb', '.hdf5', '.pkl', '.mlmodel', 'model', '.pmml', '.pt', 'joblib', 'pickle', '.onnx',
                          'proto', '.tfrecords', '.h5', '.ph', '.proto', 'pbtxt', '.ckpt'],
        'Python': ['.py', '.cpython', '.ipynb', '.pyi', '.ipynb', '.pyi'],
        '.mod': ['.mod'],
        'PEP': ['site-packages', 'python', '.abi3', '.abi3.', '.toml'],
        'whl': ['.whl', 'wheel'],
        'GPG': ['gpg'],
        'lisp': ['.el'],
        'apt': ['apt'],
        '6m': ['.6m'],
        '.min': ['.min', '.min.'],
        'C/C++': ['.h.', '.hpp', '.cc', '.obj', '.cpp', '.cxx', '.hxx', 'cpp', 'clang', 'c++'],
        'Java': ['.java', '.jar', '.jnl', '.class', '.pack'],
        'css': ['.css'],
        'Ssh/OpenSSh':['openssl','ssh', 'openssh'],
        'Php': ['.php'],
        'sh/': ['.sh'],
        'VB/.Net': ['.vb'],
        'Swift': ['.swift'],
        'ovms': ['ovms'],
        'Perl': ['.pl', '.pm', '.pmk', '.pre', '.perl', 'perl'],
        'Awk': ['.awk'],
        'Makefile': ['makefile', 'cmake', '.mk', 'qmake', '.pmk', '.make', 'cpack', 'ctest'],
        'Goland': ['.go'],
        'Ruby': ['.rb'],
        'Julia': ['julia', '.jl'],
        'Matlab': ['.m.', '.mat'],
        'libcudnn': ['libcudnn'],
        'bin': ['/bin'],
        #'.build':['.build'],
        'gcc': ['gcc', 'g++', 'gcov'],
        'lib':['/lib', '.build'],
        'qdrant': ['qdrant'],
        '.service': ['.service'],
        'docker': ['docker'],
        'YML': ['.yaml', '.yml'],
        'archive': ['.zip', '.gzip', '.tar', '.xz', '.bzip', '.bz2', '.7z', '.arj', '.rar', '.tar.gz', '.gz'],
        '.mtl': ['.mtl'],
        '.urdf': ['urdf'],
        # '.mf': ['.mf'],
        # 'Test': ['test', 'tox.'],
        'certif/ keys': ['passwd', '.md5', 'gpg', '.enc', '.crt', '.3ssl', '.key', '.keystore', '.jks', '.p12', '.pfx',
                         '.csr', '.der', 'crt', '.cer', '.ca-bundle', '.p7b', '.p7c', '.p7s', '.pem', 'chsh', 'cert',
                         '.7m', 'security', '.pwd'],
        'wh': ['.wh'],
        'qmlc': ['.qmlc'],
        '.vf': ['.vf'],
        '.htf': ['.htf'],
        'pip': ['pip'],
        '.sh': ['.sh'],
        'core': ['core', '/core'],
        'cache': ['.cache'],
        'pandoc': ['pandoc'],
        '3D': ['.stl', '.dae', '.stp', '.obj', '.fbx', '3ds', '.iges', '.step', 'vrml', '.x3d', '.3dmf', '.3dm', '.3mf',
               '.3ds', '.ac', '.amf', '.an8', '.aoi', '.asm', '.b3d', '.blend', '.block', '.bmd', '.bdl', '.brres',
               '.c4d', '.cal3d', '.cob', '.core3d', '.dpm', '.fac', '.fbx', '.xsh', '.mf', '.flt'],
        '.conda': ['.conda'],
        # 'disc/media': ['.iso', '.toast', '.vcd', '.bin', '.dmg'],
        'Data/ DB': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml', '.json',
                     '.txt', '.xls', 'info', '.xlsm', '.ods', '.pak',
                     '.accdb', '.fdb', '.sdf', '.fp3', '.gdb', '.ibd', '.wdb', '.myd', '.idx', '.cdb', '.dbf',
                     '.bsd', '.npz', '.pdb', '.dcm', 'sql', 'data','.npy'],
        'Font': ['.ttf', '.fnt', '.fon', '.otf', '.tfm', '.pfa', '.pfb', '__db'],
        '.wad': ['.wad'],
        'Video': ['.idx', '.mov', '.mp4', '.m4a', '.m4v', '.mpg', '.mpeg', '.wmv', '.avi', '.flv', '.3gp', '.3gpp',
                  '.3g2', '.3gp2', '.rm', '.swf', '.vob', '.wmv'],

        'Audio': ['.mp3', '.wav', '.aif', '.cda', '.mid', '.mp3', '.mpa', '.ogg', '.wma', '.wpl', '.sty'],
        '.symbols': ['.symbols', 'symbolic'],
        # 'Config': ['.vim', '.conf', '.cfg', ],
        'DOC': ['.pdf', '.ps', '.md', '.bib', 'changelog', '.rst', 'license', 'readme',
                'record', 'metadata', '.tcc', 'copyright', '.pod', '.pfb', '.qbk', '.bk', '.tex', '.doc', '.cgi',
                '.asc'],
        'Git': ['git'],
        '.patch': ['patch'],
        '.npm':['.npm'],
        'systemctl':['systemctl'],
        'gorse-': ['gorse-master', 'gorse-server', 'gorse-worker'],
        'Node/js': ['.js', '.node', 'nodejs'],
        'Rust': ['.rs'],
        '.jsp': ['.jspx', '.jspf', 'jsp'],
        'Html/Xml': ['.htm', '.html', '.xhtml'],
        'rss': ['.rss'],
        'image': ['.png', '.jpeg', '.svg', '.fits', '.tiff', '.eps', '.gif', '.pic', '.ico', '.fig', '.tif', '.xbm',
                  '.bmp', '.ai', '.ps', '.psd', '.tif', '.tiff',
                  '.jpg', '.xpm', '.pgm'],
        'Web': ['.asp', '.war', '.cfm', '.cgi', '.part', '.apache'],
        'ppt': ['.odp', '.pps', '.ppt', '.pptx']
    }

    file_type = str(file_path)
    if '.c' == file_type or '.C' == file_type or '.h' == file_type or 'cs' == file_type or '.hpp' == file_type or '.cpp.' in file_type or '.o' == file_type or '.o.' in file_type or file_type.endswith(
            '.o') or file_type.endswith('cc') or file_type == 'cp':
        return 'C/C++'
    elif '.a' == file_type or '.a.' in file_type or file_type.endswith('.a'):
        return '.a'
    elif '.mo' == file_type or '.mo.' in file_type:
        return 'ELF/COFF'
    elif '.z' == file_type or '.z.' in file_type:
        return 'Archival'
    elif '.f' == file_type:
        return 'Fortran'
    elif '.m' == file_type or file_type.endswith('.m'):
        return 'Matlab'
    elif file_type.endswith('node'):
        return 'Node/js'
    else:
        flag = 0
        for key, val in CATEGORIES.items():
            for v in val:
                if str(v).lower() in str(file_path).lower():
                    file_type = key
                    flag += 1
                    break
    return file_type


def general_categories(file_ext):
    CATEGORIES = {
        'EOL':['.cu', 'cmd', 'ELF/COFF', 'Ubuntu',  'debian', '.pkg', '.mod', 'cc1','.rpm','pip','bin','libcudnn','gcc', 'apt', 'apt','.symbols', '6m','min', '.map','wh', 'qmlc','core', 'cache', '.htf', 'gcc','lib', '.sym', 'systemctl', 'system','alpine'],
        'Script/Source':['Fortran','Python','.patch', 'C/C++', 'sh','Php', 'Java', 'Perl','Goland', 'Ruby', 'Awk', 'Julia', 'Matlab','Rust','Js','lisp','Matlab'],
        'Web Service':['.jsp','Web','gorse-','.service','qdrant'],
        'Documents':[ 'css','Html/Xml','DOC','rss','ppt', '.patch', 'patch','YML','.urdf','pandoc','Font'],
        #'Build/ Package Managemt':['.conda', 'VB/.Net'],
        'PEP':['PEP', '.conda'],
        'Caching':['cache', 'history'],
         'Makefile': ['Makefile'],
        'Data/Database':['Data/ DB'],
        'Model':['Model/ Weight'],
        'Security':['certif/ keys', 'Ssh/OpenSSh', 'https'],
        'Image':['ovms','image'],
        #'Video Doc':['.vf','Video'],
        'Audio Doc':['Audio'],
        'Archival DOC':['Archival','archive'],
        'Git DOC': ['git','Git'],
        #'3D Graphics':['3D']
    }

    file_type = str(file_ext)
    flag = 0
    for key, val in CATEGORIES.items():
        for v in val:
            if str(v).lower() in str(file_type).lower():
                file_type = key
                flag += 1
                break
    if flag == 0:
        file_type = 'Others'
    return file_type