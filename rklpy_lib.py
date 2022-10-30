def clc():
    print('\033[H\033[J')

def isextension(input_args):    #find type of file in a string with at least one dot(*.)
#input_args='hellow world.rkl'
    
    str=input_args
    s=len(str)
    #rstr=str
    vez=1
    #encontrado=0
    
    found=0
    rstr=''
    ext=''
    rext=''
    for i in range(1,s + 1):
        rstr += str[len(str) - i]
        if (str[len(str) - i]=='.') and vez==1:
            found=i-1
            vez=vez+1
    
    for x in range(0, found):
        rext=rext+rstr[x]
    
    for i in range(1, len(rext) + 1):
        ext += rext[len(rext) - i]
    if found==0:
        ext='mp4'
    elif len(ext)>3:
        ext='mp4'   
    elif len(ext)<3:
        ext='mp4'   
    elif ext=='5':
        ext='mp4'
    elif ' ' in ext:
        ext='mp4' 
    
    output_args=ext
    return output_args
#answ=isextension('hellow world')

def is_extension(input_str,min_chars=1,max_chars=100,not_ext_found_return=''):
#input_args='hellow world.rkl'
    """
*SHORT DESCRIPTION________________________________________________________
    Identify the extension of a string of characters, aka, a full file name.
    
*ARGUMENTS________________________________________________________________
        input_dtr = 'some string.txt'

        max_chars = 3 ### Max number of characters allowed for the extension.

        not_ext_found_return= 'Not_Found_case_extension'        
    
*DESCRIPTION_______________________________________________________________
    This function returns the extension identifiable in a string.
    You can delimite the maximum number of characters with max_chars that 
    usually are strings, it's usually 3 or 4, as in 'my_file.doc' or 
    'my_file.docx' and differentiate between 'my_file.asdafd', which probably
    is not a valid file extension but could be the result of a virus creating 
    files.
    With the not_ext_found_return argument you can determine the output of this 
    function as anything you prefer:
        is_extension(input_str,max_chars,False)
        is_extension(input_str,max_chars,'Not_Found')
        is_extension(input_str,max_chars,0)
    
    This is usefull if what you are doing is changing the extension of 
    multiple files whit different file extensions.
    
*EXAMPLES___________________________________________________________________
    Input : is_extension('myfile.homework.pdf',1,'Not_ext')    
    Output:'Not_ext'
    
    Input : is_extension('myfile homework pdf',3,False)
    Output: False
    

    Input : is_extension('myfile.homework.pdf',4,'Not_ext') 
    Output: 'pdf'    
    """    
    str=input_str
    s=len(str)
    #rstr=str
    vez=1
    #encontrado=0
    
    found=0
    rstr=''
    ext=''
    rext=''
    for i in range(1,s + 1):
        rstr += str[len(str) - i]
        if (str[len(str) - i]=='.') and vez==1:
            found=i-1
            vez=vez+1
    
    for x in range(0, found):
        rext=rext+rstr[x]
    
    for i in range(1, len(rext) + 1):
        ext += rext[len(rext) - i]
    if found==0:
        ext=not_ext_found_return
    elif len(ext)>max_chars:
        ext=not_ext_found_return
    elif len(ext)<min_chars:
        ext=not_ext_found_return
    elif ' ' in ext:
        ext=not_ext_found_return
        
    output_args=ext
    return output_args
#answ=isextension('hellow world')

def sorti(lst):     #sort a list as an insensitive case
    lst2 = [[x for x in range(0, 2)] for y in range(0, len(lst))]
    for i in range(0, len(lst)):
        lst2[i][0] = lst[i].lower()
        lst2[i][1] = lst[i]
    lst2.sort()
    for i in range(0, len(lst)):
        lst[i] = lst2[i][1]
    return lst

def getAllFiles(path,files_ext='*',auto_sort=True):
    import os
    filelist=[os.path.join(r,file) for r,d,f in os.walk(path) for file in f]
    sf=len(filelist)    #number of files in path direcctory
    files_ext=files_ext.lower()
    if files_ext != '*':
        kon=0
        filelist2=[]
        for i in range(0, sf):
            ext=is_extension(filelist[i],1,100,'Not_an_extension').lower()
            if files_ext==ext:
                filelist2.append(kon)
                filelist2[kon]=filelist[i];
                kon=kon+1;
            #end if
        #end for
    else:
        filelist2=filelist

    if auto_sort:
        return sorti(filelist2);

    return filelist
    
def getFiles(path,files_ext=''):
    #if path[-1] != '/':path+='/'
    import os
    filelist=[]
    files_here=os.listdir(path)
    
    #print(files_ext,files_here)
    for file in files_here:
        # if '.' not in os.path.basename(file):
        #     continue

        ext=os.path.splitext(file)[-1].replace('.','')
        
        if files_ext:
            # if os.path.isfile(file) and ext in files_ext:
            if ext in files_ext:
                f=os.path.join(path, file)
                if os.path.isdir(f):
                    continue
                filelist.append(f)
        else:
            file_path=os.path.join(path, file)
            if os.path.isfile(file_path):
                filelist.append(file_path)
    
    #filelist=[f.replace('/','\\') for f in filelist]
    filelist=sorti(filelist)
    return filelist
#path='C:\\c\\Python_projects\\RKL_channel\\xml2'
#files_ext='xml'
#xmls=getAllFiles(path,files_ext)


def strjoin(list):  #join a list of strings
    joined=''
    for i in range(0, len(list)):
        joined=joined+list[i]
    return joined
#answ=strjoin(['hellow', 'world'])
    
def ensure_dir(file_path):
    import os
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
def ensure_dir2(directory):
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
        
##________________PENDING FUNCTIONS_______________##
def titlexml( str ):
    #eliminate the already in xml format
    str = str.replace(":", "")
    str = str.replace("&amp;", "&")
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("&quot;", "\"")
    str = str.replace('\'', '&apos;')
    #end eliminate the already in xml format
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "&quot;")
    str = str.replace('\'', '&apos;')
    
    str=regexrepi('[^ 0-9a-zñ&;,.//?¿!¡=)(_:-]','*',str)
    # nnt=''
    # for c in str:
    #     rep=c.encode("unicode_escape").decode('utf-8')
    #     if len(rep)>1:
    #         # print(c,repr(rep),rep[2:])
    #         nnt+='&#'+rep[2:]+';'
    #     else:
    #         nnt+=c
    # str=nnt

    return str

def xmltext( str ):
    from xml.sax.saxutils import unescape
    from xml.sax.saxutils import escape
    str=unescape(str)
    str=escape(str)
    
    #eliminate the already in xml format
    str = str.replace('&#8217;','’');
    str = str.replace('&#8224;','†')
    str = str.replace("&amp;", "&")
    str = str.replace("&lt;", "<")
    str = str.replace("&gt;", ">")
    str = str.replace("&quot;", "\"")
    str = str.replace('&apos;', '\'')
    str = str.replace('&lsquo;', '\'')
    str = str.replace('&rsquo;', '\'')
    str = str.replace('&ldquo;','"')
    str = str.replace('&rdquo;','"')
    str = str.replace('&nbsp;',' ')
    str = str.replace('…','...')
    
    ######################################################################
    str=str.replace('&gt;','>')
    str=str.replace('&iexcl;','¡')
    str=str.replace('&cent;','¢')
    str=str.replace('&pound;','£')
    str=str.replace('&curren;','¤')
    str=str.replace('&yen;','¥')
    str=str.replace('&brvbar;','¦')
    str=str.replace('&sect;','§')
    str=str.replace('&uml;','¨')
    str=str.replace('&copy;','©')
    str=str.replace('&ordf;','ª')
    str=str.replace('&laquo;','«')
    str=str.replace('&not;','¬')
    str=str.replace('&reg;','®')
    str=str.replace('&macr;','¯')
    str=str.replace('&deg;','°')
    str=str.replace('&plusmn;','±')
    str=str.replace('&sup2;','²')
    str=str.replace('&sup3;','³')
    str=str.replace('&acute;','´')
    str=str.replace('&micro;','µ')
    str=str.replace('&para;','¶')
    str=str.replace('&middot;','·')
    str=str.replace('&cedil;','¸')
    str=str.replace('&sup1;','¹')
    str=str.replace('&ordm;','º')
    str=str.replace('&raquo;','»')
    str=str.replace('&frac14;','¼')
    str=str.replace('&frac12;','½')
    str=str.replace('&frac34;','¾')
    str=str.replace('&iquest;','¿')
    str=str.replace('&Agrave;','À')
    str=str.replace('&Aacute;','Á')
    str=str.replace('&Acirc;','Â')
    str=str.replace('&Atilde;','Ã')
    str=str.replace('&Auml;','Ä')
    str=str.replace('&Aring;','Å')
    str=str.replace('&AElig;','Æ')
    str=str.replace('&Ccedil;','Ç')
    str=str.replace('&Egrave;','È')
    str=str.replace('&Eacute;','É')
    str=str.replace('&Ecirc;','Ê')
    str=str.replace('&Euml;','Ë')
    str=str.replace('&Igrave;','Ì')
    str=str.replace('&Iacute;','Í')
    str=str.replace('&Icirc;','Î')
    str=str.replace('&Iuml;','Ï')
    str=str.replace('&ETH;','Ð')
    str=str.replace('&Ntilde;','Ñ')
    str=str.replace('&Ograve;','Ò')
    str=str.replace('&Oacute;','Ó')
    str=str.replace('&Ocirc;','Ô')
    str=str.replace('&Otilde;','Õ')
    str=str.replace('&Ouml;','Ö')
    str=str.replace('&times;','×')
    str=str.replace('&Oslash;','Ø')
    str=str.replace('&Ugrave;','Ù')
    str=str.replace('&Uacute;','Ú')
    str=str.replace('&Ucirc;','Û')
    str=str.replace('&Uuml;','Ü')
    str=str.replace('&Yacute;','Ý')
    str=str.replace('&THORN;','Þ')
    str=str.replace('&szlig;','ß')
    str=str.replace('&agrave;','à')
    str=str.replace('&aacute;','á')
    str=str.replace('&acirc;','â')
    str=str.replace('&atilde;','ã')
    str=str.replace('&auml;','ä')
    str=str.replace('&aring;','å')
    str=str.replace('&aelig;','æ')
    str=str.replace('&ccedil;','ç')
    str=str.replace('&egrave;','è')
    str=str.replace('&eacute;','é')
    str=str.replace('&ecirc;','ê')
    str=str.replace('&euml;','ë')
    str=str.replace('&igrave;','ì')
    str=str.replace('&iacute;','í')
    str=str.replace('&icirc;','î')
    str=str.replace('&iuml;','ï')
    str=str.replace('&eth	;','ð')
    str=str.replace('&ntilde;','ñ')
    str=str.replace('&ograve;','ò')
    str=str.replace('&oacute;','ó')
    str=str.replace('&ocirc;','ô')
    str=str.replace('&otilde;','õ')
    str=str.replace('&ouml;','ö')
    str=str.replace('&divide;','÷')
    str=str.replace('&oslash;','ø')
    str=str.replace('&ugrave;','ù')
    str=str.replace('&uacute;','ú')
    str=str.replace('&ucirc;','û')
    str=str.replace('&uuml;','ü')
    str=str.replace('&yacute;','ý')
    str=str.replace('&thorn;','þ')
    str=str.replace('&yuml;','ÿ')
    str=str.replace('&OElig;','Œ')
    str=str.replace('&oelig;','œ')
    str=str.replace('&Scaron;','Š')
    str=str.replace('&scaron;','š')
    str=str.replace('&Yuml;','Ÿ')
    str=str.replace('&fnof;','ƒ')
    str=str.replace('&circ;','ˆ')
    str=str.replace('&tilde;','˜	')
    str=str.replace('&Alpha;','Α')
    str=str.replace('&Beta;','Β')
    str=str.replace('&Gamma;','Γ')
    str=str.replace('&Delta;','Δ')
    str=str.replace('&Epsilon;','Ε')
    str=str.replace('&Zeta;','Ζ')
    str=str.replace('&Eta;','Η')
    str=str.replace('&Theta;','Θ')
    str=str.replace('&Iota;','Ι')
    str=str.replace('&Kappa;','Κ')
    str=str.replace('&Lambda;','Λ')
    str=str.replace('&Mu;','Μ')
    str=str.replace('&Nu;','Ν')
    str=str.replace('&Xi;','Ξ')
    str=str.replace('&Omicron;','Ο')
    str=str.replace('&Pi;','Π')
    str=str.replace('&Rho;','Ρ')
    str=str.replace('&Sigma;','Σ')
    str=str.replace('&Tau;','Τ')
    str=str.replace('&Upsilon;','Υ')
    str=str.replace('&Phi;','Φ')
    str=str.replace('&Chi;','Χ')
    str=str.replace('&Psi;','Ψ')
    str=str.replace('&Omega;','Ω')
    str=str.replace('&alpha;','α')
    str=str.replace('&beta;','β')
    str=str.replace('&gamma;','γ')
    str=str.replace('&delta;','δ')
    str=str.replace('&epsilon;','ε')
    str=str.replace('&zeta;','ζ')
    str=str.replace('&eta;','η')
    str=str.replace('&theta;','θ')
    str=str.replace('&iota;','ι')
    str=str.replace('&kappa;','κ')
    str=str.replace('&lambda;','λ')
    str=str.replace('&mu;','μ')
    str=str.replace('&nu;','ν')
    str=str.replace('&xi;','ξ')
    str=str.replace('&omicron;','ο')
    str=str.replace('&pi;','π')
    str=str.replace('&rho;','ρ')
    str=str.replace('&sigmaf;','ς')
    str=str.replace('&sigma;','σ')
    str=str.replace('&tau;','τ')
    str=str.replace('&upsilon;','υ')
    str=str.replace('&phi;','φ')
    str=str.replace('&chi;','χ')
    str=str.replace('&psi;','ψ')
    str=str.replace('&omega;','ω')
    str=str.replace('&thetasym;','ϑ')
    str=str.replace('&upsih;','ϒ')
    str=str.replace('&piv;','ϖ')
    str=str.replace('&ndash;','–')
    str=str.replace('&mdash;','—')
    str=str.replace('&lsquo;','‘')
    str=str.replace('&rsquo;','’')
    str=str.replace('&sbquo;','‚')
    str=str.replace('&ldquo;','“')
    str=str.replace('&rdquo;','”')
    str=str.replace('&bdquo;','„')
    str=str.replace('&dagger;','†')
    str=str.replace('&Dagger;','‡')
    str=str.replace('&bull;','•')
    str=str.replace('&hellip;','…')
    str=str.replace('&permil;','‰')
    str=str.replace('&prime;','′')
    str=str.replace('&Prime;','″')
    str=str.replace('&lsaquo;','‹')
    str=str.replace('&rsaquo;','›')
    str=str.replace('&oline;','‾')
    str=str.replace('&frasl;','⁄')
    str=str.replace('&euro;','€')
    str=str.replace('&trade;','™')
    str=str.replace('&larr;','←')
    str=str.replace('&uarr;','↑')
    str=str.replace('&rarr;','→')
    str=str.replace('&darr;','↓')
    str=str.replace('&harr;','↔')
    str=str.replace('&rArr;','⇒')
    str=str.replace('&hArr;','⇔')
    str=str.replace('&forall;','∀')
    str=str.replace('&part;','∂')
    str=str.replace('&nabla;','∇')
    str=str.replace('&prod;','∏')
    str=str.replace('&sum;','∑')
    str=str.replace('&minus;','−')
    str=str.replace('&radic;','√')
    str=str.replace('&infin;','∞')
    str=str.replace('&and;','∧')
    str=str.replace('&or;','∨')
    str=str.replace('&cap;','∩')
    str=str.replace('&cup;','∪')
    str=str.replace('&int;','∫')
    str=str.replace('&there4;','∴')
    str=str.replace('&asymp;','≈')
    str=str.replace('&ne;','≠')
    str=str.replace('&equiv;','≡')
    str=str.replace('&le;','≤')
    str=str.replace('&ge;','≥')
    str=str.replace('&perp;','⊥')
    str=str.replace('&lang;','〈')
    str=str.replace('&rang;','〉')
    str=str.replace('&loz;','◊')
    str=str.replace('&spades;','♠')
    str=str.replace('&clubs;','♣')
    str=str.replace('&hearts;','♥')
    str=str.replace('&diams;','♦')
    
    ######################################################################
    
    #end eliminate the already in xml format
    
    str = str.replace('"','&quot;');
    str = str.replace('“','"');
    str = str.replace('”','"');
    str = str.replace('‘','\'');
    str = str.replace('’','\'');
    str = str.replace('†','&dagger;')
    str = str.replace("&", "&amp;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    str = str.replace("\"", "&quot;")
    str = str.replace('\'', '&apos;')
########################################    str = str.replace('//', '&frasl;')
    
    #####################################################################
    str=str.replace('>','&gt;')
    str=str.replace('¡','&iexcl;')
    str=str.replace('¢','&cent;')
    str=str.replace('£','&pound;')
    str=str.replace('¤','&curren;')
    str=str.replace('¥','&yen;')
    str=str.replace('¦','&brvbar;')
    str=str.replace('§','&sect;')
    str=str.replace('¨','&uml;')
    str=str.replace('©','&copy;')
    str=str.replace('ª','&ordf;')
    str=str.replace('«','&laquo;')
    str=str.replace('¬','&not;')
    str=str.replace('®','&reg;')
    str=str.replace('¯','&macr;')
    str=str.replace('°','&deg;')
    str=str.replace('±','&plusmn;')
    str=str.replace('²','&sup2;')
    str=str.replace('³','&sup3;')
    str=str.replace('´','&acute;')
    str=str.replace('µ','&micro;')
    str=str.replace('¶','&para;')
    str=str.replace('·','&middot;')
    str=str.replace('¸','&cedil;')
    str=str.replace('¹','&sup1;')
    str=str.replace('º','&ordm;')
    str=str.replace('»','&raquo;')
    str=str.replace('¼','&frac14;')
    str=str.replace('½','&frac12;')
    str=str.replace('¾','&frac34;')
    str=str.replace('¿','&iquest;')
    str=str.replace('À','&Agrave;')
    str=str.replace('Á','&Aacute;')
    str=str.replace('Â','&Acirc;')
    str=str.replace('Ã','&Atilde;')
    str=str.replace('Ä','&Auml;')
    str=str.replace('Å','&Aring;')
    str=str.replace('Æ','&AElig;')
    str=str.replace('Ç','&Ccedil;')
    str=str.replace('È','&Egrave;')
    str=str.replace('É','&Eacute;')
    str=str.replace('Ê','&Ecirc;')
    str=str.replace('Ë','&Euml;')
    str=str.replace('Ì','&Igrave;')
    str=str.replace('Í','&Iacute;')
    str=str.replace('Î','&Icirc;')
    str=str.replace('Ï','&Iuml;')
    str=str.replace('Ð','&ETH;')
    str=str.replace('Ñ','&Ntilde;')
    str=str.replace('Ò','&Ograve;')
    str=str.replace('Ó','&Oacute;')
    str=str.replace('Ô','&Ocirc;')
    str=str.replace('Õ','&Otilde;')
    str=str.replace('Ö','&Ouml;')
    str=str.replace('×','&times;')
    str=str.replace('Ø','&Oslash;')
    str=str.replace('Ù','&Ugrave;')
    str=str.replace('Ú','&Uacute;')
    str=str.replace('Û','&Ucirc;')
    str=str.replace('Ü','&Uuml;')
    str=str.replace('Ý','&Yacute;')
    str=str.replace('Þ','&THORN;')
    str=str.replace('ß','&szlig;')
    str=str.replace('à','&agrave;')
    str=str.replace('á','&aacute;')
    str=str.replace('â','&acirc;')
    str=str.replace('ã','&atilde;')
    str=str.replace('ä','&auml;')
    str=str.replace('å','&aring;')
    str=str.replace('æ','&aelig;')
    str=str.replace('ç','&ccedil;')
    str=str.replace('è','&egrave;')
    str=str.replace('é','&eacute;')
    str=str.replace('ê','&ecirc;')
    str=str.replace('ë','&euml;')
    str=str.replace('ì','&igrave;')
    str=str.replace('í','&iacute;')
    str=str.replace('î','&icirc;')
    str=str.replace('ï','&iuml;')
    str=str.replace('ð','&eth	;')
    str=str.replace('ñ','&ntilde;')
    str=str.replace('ò','&ograve;')
    str=str.replace('ó','&oacute;')
    str=str.replace('ô','&ocirc;')
    str=str.replace('õ','&otilde;')
    str=str.replace('ö','&ouml;')
    str=str.replace('÷','&divide;')
    str=str.replace('ø','&oslash;')
    str=str.replace('ù','&ugrave;')
    str=str.replace('ú','&uacute;')
    str=str.replace('û','&ucirc;')
    str=str.replace('ü','&uuml;')
    str=str.replace('ý','&yacute;')
    str=str.replace('þ','&thorn;')
    str=str.replace('ÿ','&yuml;')
    str=str.replace('Œ','&OElig;')
    str=str.replace('œ','&oelig;')
    str=str.replace('Š','&Scaron;')
    str=str.replace('š','&scaron;')
    str=str.replace('Ÿ','&Yuml;')
    str=str.replace('ƒ','&fnof;')
    str=str.replace('ˆ','&circ;')
    str=str.replace('˜	','&tilde;')
    str=str.replace('Α','&Alpha;')
    str=str.replace('Β','&Beta;')
    str=str.replace('Γ','&Gamma;')
    str=str.replace('Δ','&Delta;')
    str=str.replace('Ε','&Epsilon;')
    str=str.replace('Ζ','&Zeta;')
    str=str.replace('Η','&Eta;')
    str=str.replace('Θ','&Theta;')
    str=str.replace('Ι','&Iota;')
    str=str.replace('Κ','&Kappa;')
    str=str.replace('Λ','&Lambda;')
    str=str.replace('Μ','&Mu;')
    str=str.replace('Ν','&Nu;')
    str=str.replace('Ξ','&Xi;')
    str=str.replace('Ο','&Omicron;')
    str=str.replace('Π','&Pi;')
    str=str.replace('Ρ','&Rho;')
    str=str.replace('Σ','&Sigma;')
    str=str.replace('Τ','&Tau;')
    str=str.replace('Υ','&Upsilon;')
    str=str.replace('Φ','&Phi;')
    str=str.replace('Χ','&Chi;')
    str=str.replace('Ψ','&Psi;')
    str=str.replace('Ω','&Omega;')
    str=str.replace('α','&alpha;')
    str=str.replace('β','&beta;')
    str=str.replace('γ','&gamma;')
    str=str.replace('δ','&delta;')
    str=str.replace('ε','&epsilon;')
    str=str.replace('ζ','&zeta;')
    str=str.replace('η','&eta;')
    str=str.replace('θ','&theta;')
    str=str.replace('ι','&iota;')
    str=str.replace('κ','&kappa;')
    str=str.replace('λ','&lambda;')
    str=str.replace('μ','&mu;')
    str=str.replace('ν','&nu;')
    str=str.replace('ξ','&xi;')
    str=str.replace('ο','&omicron;')
    str=str.replace('π','&pi;')
    str=str.replace('ρ','&rho;')
    str=str.replace('ς','&sigmaf;')
    str=str.replace('σ','&sigma;')
    str=str.replace('τ','&tau;')
    str=str.replace('υ','&upsilon;')
    str=str.replace('φ','&phi;')
    str=str.replace('χ','&chi;')
    str=str.replace('ψ','&psi;')
    str=str.replace('ω','&omega;')
    str=str.replace('ϑ','&thetasym;')
    str=str.replace('ϒ','&upsih;')
    str=str.replace('ϖ','&piv;')
    str=str.replace('–','&ndash;')
    str=str.replace('—','&mdash;')
    str=str.replace('‘','&lsquo;')
    str=str.replace('’','&rsquo;')
    str=str.replace('‚','&sbquo;')
    str=str.replace('“','&ldquo;')
    str=str.replace('”','&rdquo;')
    str=str.replace('„','&bdquo;')
    str=str.replace('†','&dagger;')
    str=str.replace('‡','&Dagger;')
    str=str.replace('•','&bull;')
    str=str.replace('…','&hellip;')
    str=str.replace('‰','&permil;')
    str=str.replace('′','&prime;')
    str=str.replace('″','&Prime;')
    str=str.replace('‹','&lsaquo;')
    str=str.replace('›','&rsaquo;')
    str=str.replace('‾','&oline;')
    str=str.replace('⁄','&frasl;')
    str=str.replace('€','&euro;')
    str=str.replace('™','&trade;')
    str=str.replace('←','&larr;')
    str=str.replace('↑','&uarr;')
    str=str.replace('→','&rarr;')
    str=str.replace('↓','&darr;')
    str=str.replace('↔','&harr;')
    str=str.replace('⇒','&rArr;')
    str=str.replace('⇔','&hArr;')
    str=str.replace('∀','&forall;')
    str=str.replace('∂','&part;')
    str=str.replace('∇','&nabla;')
    str=str.replace('∏','&prod;')
    str=str.replace('∑','&sum;')
    str=str.replace('−','&minus;')
    str=str.replace('√','&radic;')
    str=str.replace('∞','&infin;')
    str=str.replace('∧','&and;')
    str=str.replace('∨','&or;')
    str=str.replace('∩','&cap;')
    str=str.replace('∪','&cup;')
    str=str.replace('∫','&int;')
    str=str.replace('∴','&there4;')
    str=str.replace('≈','&asymp;')
    str=str.replace('≠','&ne;')
    str=str.replace('≡','&equiv;')
    str=str.replace('≤','&le;')
    str=str.replace('≥','&ge;')
    str=str.replace('⊥','&perp;')
    str=str.replace('〈','&lang;')
    str=str.replace('〉','&rang;')
    str=str.replace('◊','&loz;')
    str=str.replace('♠','&spades;')
    str=str.replace('♣','&clubs;')
    str=str.replace('♥','&hearts;')
    str=str.replace('♦','&diams;')
    #####################################################################
    str=regexrepi('[^ 0-9a-zñ&;,.?¿!¡=)(_:#-/]','*',str)
    return str

#def xmltext_rare(text):
#    text=xmltext(text)
#    #text=text.replace('&amp;','&')
#    #text=text.replace("&lt;", "<")
#    #text=text.replace("&gt;", ">")
#    #text=text.replace("&apos;", '\'')
#    text=text.replace("&quot;", "\"")
#    return text

def urlxml(url):
    from urllib.parse import quote
    
    url=url.replace('%20',' ');
    url=url.replace('%2b','+');
    url=url.replace('%2B','+');
    
    if 'www.dropbox.com' in url:
        url=url.replace('www.dropbox.com','dl.dropboxusercontent.com');
        url=url.replace('?dl=0','?dl=1');
    #end
    
    url=quote(url, safe='')
    
    url=url.replace('%2F','/');
    url=url.replace('%3A',':');
    
    urlx=url
    return urlx

def url_dropbox(url):
    if 'www.dropbox.com' in url:
        url=url.replace('www.dropbox.com','dl.dropboxusercontent.com');
        url=url.replace('?dl=0','?dl=1');
        
    return url
#ur=urlxml('https://www.dropbox.com/s/ftitwyhmeg1ici0/A.Christmas.Horror.Story.2015.BDRip.x264-ROVERS.mkv.mp4?dl=0&x?3----KÃ-mpfer-')
#ur=urlxml('_@')
    
##________________________________________________##
def regexpi_2(patern, string):
    import re
    string=string.lower()
    result = re.match(patern, string,flags=re.IGNORECASE)
    result=result.group(0)
    return result

def regexpi(find_str,from_string):
    find_str=find_str.lower()
    from_string=from_string.lower()
    result=find_str in from_string
    return result

def regexpi_count(find_str,from_string):
    find_str=find_str.lower()
    from_string=from_string.lower()
    result=find_str in from_string
    if result:
        result=len(from_string.split(find_str))-1
    else:
        result=0
    
    return result
#a=regexpi('patern','oPatErnsdfgh')

def regexrep(patern, repwith, from_string): #replace a patern with something else from a string
    from re import sub
    replaced=sub(patern, repwith, from_string)
    return replaced
#b='ASA- - Fafdsffv s123fdf1414 ASAÑñDa+a112*1á´ésdâsdsäëïöüàèìòù~.,_;'
#a=regexrep('[a-z _Ññâêîôûáéíóúäëïöüàèìòù^\W]','',b)
#a=regexrep('[^A-Z0-9]','',b)
def regexrepi(patern, repwith, from_string): #replace a patern with something else from a string, case insensitive
    import re
    pattern = re.compile(patern, re.IGNORECASE)
    replaced=pattern.sub(repwith, from_string)
    return replaced


def animef_db(searchfor):
    #searchfor='overlord movie 1'
    norm_chars_param='[^a-zA-Z0-9 ]'  #normalaize characters in the names, replaced to ' '
    
    searchfor=regexrep(norm_chars_param,' ',searchfor)
    searchfor=regexrep('  ',' ',searchfor)
    searchfor=searchfor.strip()
    nm=searchfor.split()
    nop=len(nm)      #number of words
    
    #adb=open('ANIME.datb','r').read()
    adb=open('ANIME.datb', encoding="utf8").read()
    adb2=adb.splitlines()
    adb2=sorti(adb2)
    resreal=-2;respar=-2;res=-2;respart=-2;respart_lazy=-2
    ovs=len(adb2);      #overall size
    
    info=[]
    namesdb=[]
    postersdb=[]
    descdb=[]
    for i in range(0, ovs):
        info.append(i)
        info[i]=adb2[i].split('<<')
        
        namesdb.append(i)
        namesdb[i]=info[i][1]
        
        postersdb.append(i)
        postersdb[i]=info[i][2]
        
        descdb.append(i)
        descdb[i]=info[i][3]    
    #end for
    
    names_all_lazy=[]
    namesforsearch=namesdb
    coincidences_old=0
    coincidences_old_lazy=0
    lazy_c=0
    for i in range(0, ovs):
        namesforsearch[i]=regexrep(norm_chars_param,' ',namesforsearch[i])
        namesforsearch[i]=regexrep('  ','',namesforsearch[i])
        namesforsearch[i]=namesforsearch[i].strip()    
        
        nm2=namesforsearch[i].split()    
        npfs=len(nm2)       #number of words in the for search  name
             
        ifound=regexpi(searchfor,namesforsearch[i])
        
        if ifound and nop==npfs:
            resreal=i
        if ifound and nop<npfs:
            respar=i
        elif ifound==False:
            coincidences=0
            for j in range(0,npfs):            
                if len(nm2[j])>1 and regexpi(nm2[j],searchfor):
                    #print(nm2[j],searchfor,i)
                    coincidences=coincidences+1
            #end for
            if coincidences>0 and coincidences>coincidences_old:
                respart=i
                coincidences_old=coincidences
            #end if
        #end if, elif
        
        if ifound==False:
            coincidences=0
            for j in range(0,nop):
                if regexpi(nm[j],namesforsearch[i]):
                    coincidences=coincidences+1
            #end for
            if coincidences>0 and coincidences>coincidences_old_lazy:
                respart_lazy=i
                
                names_all_lazy.append(lazy_c)
                names_all_lazy[lazy_c]=namesforsearch[i]
                lazy_c=lazy_c+1
                #if len(namesforsearch[i])<len(namesforsearch[respart_lazy_old]):
                #    respart_lazy=respart_lazy_old
                #end if            
                coincidences_old_lazy=coincidences
            #end if
        
    #end for

    if respart>-1:
        res=respart            
    if respart_lazy>-1:
        res=respart_lazy    
    if respar>-1:
        res=respar
    if resreal>-1:
        res=resreal
        
    if res>-1:
        N=namesdb[res]
        P=postersdb[res]
        D=descdb[res]
    else:
        N='Not_Found'
        P='Not_Found'
        D='Not_Found'
    #end if, else
        
    #print(searchfor,res,N)

    
    #print(names_all_lazy)
    #print(namesdb[respart],namesdb[respart_lazy],namesdb[respar],namesdb[resreal])
    return [N,P,D]
#searchfor='black clover'
#def animef_db(searchfor):

def search_in_standard_database(searchfor,datb_dir):
    """
*SHORT DESCRIPTION________________________________________________________
    Search a term in a standard *.datb file.
    
*ARGUMENTS________________________________________________________________
        searchfor = 'some string'

        datb_dir = 'C:\\Some\\Absolute\\Path\\To\\my_database.datb'
            *OR
        datb_dir = 'Some_Relative_Path_To\\my_database.datb'
    
*DESCRIPTION_______________________________________________________________
    This function returns an array containing [Name,info_1,info_2] from a
    standard *.datb file, being the "Name" result the best match for the
    "searchfor" input acording to the logic within this function.
    
    The more accurate input as the "searchfor" variable according to the
    information within the *.datb file, the better the results.
    
*EXAMPLE___________________________________________________________________
    Input : search_in_standard_database('dragon ball super','ANIME.datb')   
    Output: 
    ['Dragon Ball Super',
     'http://images.animeadvice.com/assets/media/1/7/6/23671.jpg',
     'animestreams.tv: Synopsis: Reuniting the franchise's iconic characters, Dragon Ball Super will follow the aftermath of Goku's fierce battle with Majin Buu as he attempts to maintain earth's fragile peace.']
    """
    #searchfor='searchterm'
    norm_chars_param='[^a-zA-Z0-9 ]'  #normalaize characters in the names, replaced to ' '
    
    searchfor=regexrep(norm_chars_param,' ',searchfor)
    searchfor=regexrep('  ',' ',searchfor)
    searchfor=searchfor.strip()
    nm=searchfor.split()
    nop=len(nm)      #number of words
    
    #adb=open('ANIME.datb','r').read()
    adb=open(datb_dir,'r', encoding="utf8").read()
    adb2=adb.splitlines()
    adb2=sorti(adb2)
    resreal=-2;respar=-2;res=-2;respart=-2;respart_lazy=-2
    ovs=len(adb2);      #overall size
    
    info=[]
    namesdb=[]
    postersdb=[]
    descdb=[]
    for i in range(0, ovs):
        info.append(i)
        info[i]=adb2[i].split('<<')
        
        namesdb.append(i)
        namesdb[i]=info[i][1]
        
        postersdb.append(i)
        postersdb[i]=info[i][2]
        
        descdb.append(i)
        descdb[i]=info[i][3]    
    #end for
    
    names_all_lazy=[]
    namesforsearch=namesdb
    coincidences_old=0
    coincidences_old_lazy=0
    lazy_c=0
    for i in range(0, ovs):
        namesforsearch[i]=regexrep(norm_chars_param,' ',namesforsearch[i])
        namesforsearch[i]=regexrep('  ','',namesforsearch[i])
        namesforsearch[i]=namesforsearch[i].strip()    
        
        nm2=namesforsearch[i].split()    
        npfs=len(nm2)       #number of words in the for search  name
             
        ifound=regexpi(searchfor,namesforsearch[i])
        
        if ifound and nop==npfs:
            resreal=i
        if ifound and nop<npfs:
            respar=i
        elif ifound==False:
            coincidences=0
            for j in range(0,npfs):            
                if len(nm2[j])>1 and regexpi(nm2[j],searchfor):
                    #print(nm2[j],searchfor,i)
                    coincidences=coincidences+1
            #end for
            if coincidences>0 and coincidences>coincidences_old:
                respart=i
                coincidences_old=coincidences
            #end if
        #end if, elif
        
        if ifound==False:
            coincidences=0
            for j in range(0,nop):
                if regexpi(nm[j],namesforsearch[i]):
                    coincidences=coincidences+1
            #end for
            if coincidences>0 and coincidences>coincidences_old_lazy:
                respart_lazy=i
                
                names_all_lazy.append(lazy_c)
                names_all_lazy[lazy_c]=namesforsearch[i]
                lazy_c=lazy_c+1
                #if len(namesforsearch[i])<len(namesforsearch[respart_lazy_old]):
                #    respart_lazy=respart_lazy_old
                #end if            
                coincidences_old_lazy=coincidences
            #end if
        
    #end for

    if respart>-1:
        res=respart            
    if respart_lazy>-1:
        res=respart_lazy    
    if respar>-1:
        res=respar
    if resreal>-1:
        res=resreal
        
    if res>-1:
        N=namesdb[res]
        P=postersdb[res]
        D=descdb[res]
    else:
        N='Not_Found'
        P='Not_Found'
        D='Not_Found'
    #end if, else
        
    #print(searchfor,res,N)

    
    #print(names_all_lazy)
    #print(namesdb[respart],namesdb[respart_lazy],namesdb[respar],namesdb[resreal])
    return [N,P,D]
#[N,P,D]=search_in_standard_database('dragon ball super','ANIME.datb')
    

def progressbar(val):
    #from time import sleep
    import sys
        
    i=round(val/5)
    sys.stdout.flush()
    #if val<1:val=val*100
    
    sys.stdout.write('\r')
    # the exact output you're looking for:    
    sys.stdout.write("[%-20s] %d%%" % ('='*i, val))    
    sys.stdout.flush()
    #sleep(0.01)
    #if round(i)==100:sys.stdout.write("\r\n")    
#---------------------------------------------------#    
#for i in range(0,101):
#    progressbar(i)
#print('\nsdfghj\nsdfghj')    
#for j in range(0,101):
#    progressbar(j)
    
    
def progressbar_2(val):
    from time import sleep
    import sys
    
    i=round(val/5)
    sys.stdout.flush()
    
    #sys.stdout.write('\r')
    
    # the exact output you're looking for:    
    #sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))    
    sys.stdout.write("\033[F")
    print('\r',"[%-20s] %d%%" % ('='*i, val),'\r')    
    sys.stdout.flush()
    sleep(0.01)
#---------------------------------------------------#    
#for i in range(0,101):
#    progressbar_2(i)
#print('\nsdfghj\nsdfghj')    
#for j in range(0,101):
#    progressbar_2(j)

def progressbar_3(val):
    val=int(val)
    clc()
    print('[','='*int(val/5),' '*(20-int(val/5)),']',str(val),'%',sep='')

def text_between(string,first_delimiter,last_delimiter):
    btw=''
    for i in range(0,len(string)):
        if string[i] is first_delimiter:
            btw=string[i+1]
            for j in range(i+2,len(string)):
                if string[j] is not last_delimiter:
                    btw=btw+string[j]
                    #print(btw)
                else:
                    break
                #end if
            #end for
            break
        #end if
    return btw

# print(text_between( r'<10>C:\c\Python_projects','<','>'),)

def numbers_in_string(string):
    numbers=''
    for i in range(0,len(string)):
        if string[i] == '0' or string[i] == '1' or string[i] == '2' or string[i] == '3' or string[i] == '4' or string[i] == '5' or string[i] == '6' or string[i] == '7' or string[i] == '8' or string[i] == '9':
            numbers=numbers+string[i]
        
    return numbers

def round_up(float_n):
    r_n=round(float_n)
    if r_n<float_n:
        rounded_n=r_n+1
    else:
        rounded_n=r_n
    
    return rounded_n
    
def chia_download_vid(browser,url):
#url="http://download.animepremium.tv/video/96560"

    #from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    #browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB) 
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    
    browser.get(url)
    
    html_source=browser.page_source
    name=browser.title.replace('Download ','')
    
    available=True
    if name=='not available yet':
        print('*ERROR: Bad url or episode is not available')
        available=False
        videos_url=['https://darkstuffsite.000webhostapp.com/videos/video_not_found.mp4','https://darkstuffsite.000webhostapp.com/videos/video_not_found.mp4','https://darkstuffsite.000webhostapp.com/videos/video_not_found.mp4','https://darkstuffsite.000webhostapp.com/videos/video_not_found.mp4']
        return [name,videos_url,browser]
        
    delay = 20 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bttn.green')))
        #print("Page is ready!")
        #print(myElem.text,myElem.get_attribute('href'))
        #video=myElem.get_attribute('href')
    #        Page is ready!
    #        Server Zero http://cache2.animepremium.tv:8880/downloadcache/J7tWTedpC0NjEz-SrSJf1Q/1516339203/ynpoovepfz6q.html.mp4/Dragon-Ball-Super-Episode-122-chia-anime.com.mp4
        videos_obj=browser.find_elements_by_css_selector('a.bttn.green')
        videos_url=[]
        
        for i in range(0,len(videos_obj)):
            videos_url.append(i)
            videos_url[i]=videos_obj[i].get_attribute('href')
        
    except TimeoutException:
        print("Loading took too much time!")
    
    #browser.close()
    if available:
        return [name,videos_url,browser]

def chia_download_vid_list(url_list):
#url_list=["http://download.animepremium.tv/video/97263","http://download.animepremium.tv/video/97345"]
    import random as rand

    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB) 
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    ep_names=[]
    ep_vid_urls=[]
    for uli in range(0,len(url_list)):
    
        url=url_list[uli]
        browser.get(url)
        
        html_source=browser.page_source
        name=browser.title.replace('Download ','')
    
        if name=='not available yet':
            print('*ERROR: Bad url or episode is not available')
            return
            
        delay = 20 # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bttn.green')))
            #print("Page is ready!")
            #print(myElem.text,myElem.get_attribute('href'))
            #video=myElem.get_attribute('href')
        #        Page is ready!
        #        Server Zero http://cache2.animepremium.tv:8880/downloadcache/J7tWTedpC0NjEz-SrSJf1Q/1516339203/ynpoovepfz6q.html.mp4/Dragon-Ball-Super-Episode-122-chia-anime.com.mp4
            videos_obj=browser.find_elements_by_css_selector('a.bttn.green')
            videos_url=[]
            
            
            for i in range(0,len(videos_obj)):
                videos_url.append(i)
                videos_url[i]=videos_obj[i].get_attribute('href')
                
########################################
            ep_names.append(uli)
            ep_vid_urls.append(uli)
            n=rand.randint(0,len(videos_url)-2)
            [ep_names[uli],ep_vid_urls[uli]]=[name,videos_url[n]]
########################################
            
        except TimeoutException:
            print("Loading took too much time!")
            
    #end for uli
    
    browser.close()    
    return [ep_names,ep_vid_urls]

def chia_anime_animescrap(url):
    #[title,vid_url]=roku.chia_download_vid('http://download.animepremium.tv/video/96994')
    #http://download.animepremium.tv/video/
    
    #url='http://m1.chia-anime.tv/show/aa-megami-sama-sorezore-no-tsubasa/'
    css='span.mug'
    attribute='style'
    
    if url[-1] != '/':url=url+'/'
    url=url+'&paged=1&order='
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    browser.get(url)
    html_source=browser.page_source
    name=browser.title.replace('Watch ','').replace(' Episodes via mobile','')
    
    delay = 20 # seconds
    
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        print("Page is ready!")
        
        all_eps_list=browser.find_elements_by_css_selector('select')
        all_eps_num=len(all_eps_list[0].text.split('\n'))
        pagged_n=round_up(all_eps_num/30)
        
        
        css_obj=browser.find_elements_by_css_selector(css)
        css_url=[]    
        episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
        episode_name=[]
        down_url=[]
        
        for i in range(0,len(css_obj)):
            css_url.append(i)
            episode_name.append(i)
            episode_name[i]=episode_obj[i].text.replace('\n',' ')
            #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
            css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
            down_url.append(i)
            down_url[i]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
        #end for
        
    except TimeoutException:
        print("Loading took too much time!")
    
    
    
    if pagged_n>1:
        for pag in range(2,pagged_n+1):
            url=url.replace('&paged='+str(pag-1)+'&order=','&paged='+str(pag)+'&order=')
            browser.get(url)
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
                print("Page is ready!")
                
                
                css_obj=browser.find_elements_by_css_selector(css)
                episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
                
                for i in range(0,len(css_obj)):
                    ii=i+30*(pag-1)
                    css_url.append(i)
                    episode_name.append(ii)
                    episode_name[ii]=episode_obj[i].text.replace('\n',' ')
                    #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
                    css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
                    down_url.append(ii)
                    down_url[ii]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
                #end for
                
            except TimeoutException:
                print("Loading took too much time!")
        #end for
    #end if
    
    episode_name=list(reversed(episode_name))
    down_url=list(reversed(down_url))
    
    browser.close()
    return [episode_name,down_url,name]

def prettify(elem):
    from xml.etree import ElementTree
    from xml.dom import minidom
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def OrderedSet(alist):
    """ Creates an ordered set from a list of tuples or other hashable items """
    mmap = {} # implements hashed lookup
    oset = [] # storage for set
    for item in alist:
            #Save unique items in input order
            if item not in mmap:
                    mmap[item] = 1
                    oset.append(item)
    return oset

def OrderedSet_xml(alist):
    oset=OrderedSet(alist)
    o2=[]
    for i in range(0,len(oset)):
        o2.append(i)
        o2[i]=oset[i]
        
        letter=0
        bs=''
        for j in range(0,len(o2[i])):
            if letter==0 and o2[i][j]==' ':
                bs=j*' '
            else:
                letter=1
        letter=0
        bs2=''
        if i+1<len(oset):
            for j in range(0,len(oset[i+1])):
                if letter==0 and oset[i+1][j]==' ':
                    bs2=j*' '
                else:
                    letter=1
                
        if '<categoryLeaf' in oset[i] and '<category ' in oset[i+1]:
            o2[i]=o2[i]+'\n'+bs[0:-1]+'</category>'
        
        if '<categoryLeaf' in oset[i] and '</categories>' in oset[i+1]:
            o2[i]=o2[i]+'\n'+bs[0:-1]+'</category>'
        
    o3=[]
    for i in range(0,len(o2)):
        o3.append(i)
        o3[i]=o2[i]+'\n'
    o4=strjoin(o3)
    o5=o4.split('\n')
    
    o6=[]
    for i in range(0,len(o5)):
        o6.append(i)
        o6[i]=o5[i]
        
        letter=0
        bs=''
        for j in range(0,len(o6[i])):
            if letter==0 and o6[i][j]==' ':
                bs=j*' '
            else:
                letter=1
        letter=0
        bs2=''
        if i+1<len(o5):
            for j in range(0,len(o5[i+1])):
                if letter==0 and o5[i+1][j]==' ':
                    bs2=j*' '
                else:
                    letter=1
                
        if '</category>' in o5[i] and '<category ' in o5[i+1] and bs!=bs2:
            o6[i]=o6[i]+'\n'+(len(bs2)+1)*' '+'</category>'
    
    return o6

def add_betw_alist(alist,delim):
    out=''
    for i in range(0,len(alist)):
        out=out+alist[i]+delim
    return out

#s=[]
#for i in range(0,22):s.append(i)
#
#s[0]='<categories>'
#s[1]='  <category hd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" sd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" title="anime">'
#s[2]='    <category hd_img="https://darkstuffsite.000webhostapp.com/images/A.png" sd_img="https://darkstuffsite.000webhostapp.com/images/A.png" title="A">'
#s[3]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/A/Accel World.xml/" title="Accel World"/>'
#s[4]='    </category>'
#s[5]='  </category>'
#s[6]='  <category hd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" sd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" title="anime">'
#s[7]='    <category hd_img="https://darkstuffsite.000webhostapp.com/images/D.png" sd_img="https://darkstuffsite.000webhostapp.com/images/D.png" title="D">'
#s[8]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/D/D. Gray-Man part01.xml/" title="D. Gray-Man part01"/>'
#s[9]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/D/D. Gray-Man part02.xml/" title="D. Gray-Man part02"/>'
#s[10]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/D/D.Gray-man Hallow.xml/" title="D.Gray-man Hallow"/>'
#s[11]='    </category>'
#s[12]='  </category>'
#s[13]='  <category hd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" sd_img="https://darkstuffsite.000webhostapp.com/images/anime.png" title="anime op2">'
#s[14]='    <category hd_img="https://darkstuffsite.000webhostapp.com/images/A.png" sd_img="https://darkstuffsite.000webhostapp.com/images/A.png" title="A">'
#s[15]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/A/Accel World.xml/" title="Accel World"/>'
#s[16]='    </category>'
#s[17]='    <category hd_img="https://darkstuffsite.000webhostapp.com/images/A.png" sd_img="https://darkstuffsite.000webhostapp.com/images/A.png" title="A">'
#s[18]='      <categoryLeaf feed="https://darkstuffsite.000webhostapp.com/xml2/anime/A/Accel World.xml/" title="Accel World"/>'
#s[19]='    </category>'
#s[20]='  </category>'
#s[21]='</categories>'

def xml_line_level(line):
    if line[0]==' ':
        level=int((len(text_between(line,' ','<'))+1)/2)
    else:
        level=0
    return level

def xml_line_atribute(line,atr):
    n_atr= atr+'='
    if n_atr in line:
        temp=line.split(n_atr)
        if temp[-1][0]=='"':
            atr_ans=text_between(temp[-1],'"','"')
        elif temp[-1][0]=='\'':
            atr_ans=text_between(temp[-1],'\'','\'')
        else:
            atr_ans=temp[-1]
    else:
        atr_ans=False
    return atr_ans

def xml_fuse_repeated_parents(tree):
    l=len(tree)
    parents=[]
    lvls=[]
    ts=[]
    c=0
    prev_par=[]
    pp_idx=0
    for i in range(0,l):
        if '<category ' in tree[i]:# and '<categoryleaf' in tree[i+1]:
            parents.append(c)
            lvls.append(c)
            ts.append(c)
            
            parents[c]=tree[i]
            n_ts=xml_line_atribute(tree[i],'title')
            lvls[c]=xml_line_level(tree[i])
            if n_ts in ts:
                found_idx=ts.index(n_ts)
                #print(parents[c-1],parents[found_idx-1])
                if lvls[c]==1 and lvls[c]==lvls[found_idx]:
                    ts[c]=n_ts+'--DeLeTeMe'
                    tree[i]=tree[i]+'--DeLeTeMe'
                elif lvls[c]>1 and lvls[found_idx]>1 and lvls[c]==lvls[found_idx]:# and parents[c-1]==parents[found_idx-1]:
                    ### find the previus parent
                    for k in range(0,c):
                        #print(lvls[c-k])
                        if lvls[c-k]<lvls[c]:
                            prev_par_n=ts[c-k]
                            ppn_idx=c-k
                            break
                    
                    if prev_par_n==prev_par and ppn_idx==pp_idx:
                        ts[c]=n_ts+'--DeLeTeMe'
                        tree[i]=tree[i]+'--DeLeTeMe'
                    else:
                        ts[c]=n_ts
                        tree[i]=tree[i]
                    #print(ts[c])
                    prev_par=prev_par_n
                    ppn_idx=pp_idx
                    #print(prev_par)
                else:
                    ts[c]=xml_line_atribute(tree[i],'title')
            else:
                ts[c]=xml_line_atribute(tree[i],'title')
            
            c=c+1

    for i in range(0,l):
        if '--DeLeTeMe' in tree[i]:
            tree[i-1]=[]
            tree[i]=[]
            
            
    n_tree=[]         
    c=0
    for i in range(0,l):
        if len(tree[i])>0:
            n_tree.append(c)
            n_tree[c]=tree[i]
            c=c+1
   
    
    #s_ans=parents
    #return tree,s_ans,lvls,ts
    return n_tree

def xml_lines2string(xml_lines):
    c3=[]
    for i in range(0,len(xml_lines)):
        c3.append(i)
        c3[i]=xml_lines[i]+'\n'
    c4=strjoin(c3)
    return c4

def valid_names4categories_file(name):
    name=name.replace('\\','==')
    renamed=regexrepi('[^ 0-9a-zñ&;,.?¿!¡=)(_:#-/]','-',name)
    renamed=renamed.replace('==','\\')
    return renamed

def chiascrap_rklmaker(anime_url):
    #url='http://m2.chia-anime.tv/show/d-gray-man-anime/'
    [episode_name,down_url,anime_name,ep_name,vid_urls]=chia_anime_animescrap_fast(anime_url)
    #[episode_name,down_url,name,ep_names,ep_vid_urls]
    #[ep_name,vid_urls]=chia_download_vid_list(down_url)
    
    anime_path=strjoin(['rkl\\',anime_name,'.rkl'])
    ensure_dir(anime_path)
    anime_data=animef_db(anime_name)
    
    
    cat_file=open(anime_path,'w')
    cat_file.write('<<series<<\n')
    cat_file.write('<<'+anime_name+'<<\n')
    cat_file.write('<<'+anime_data[1]+'<<\n')
    cat_file.write('<<'+anime_data[2]+'<<\n')
    
    
    for i in range(0,len(episode_name)):
        cat_file.write('\n<<'+episode_name[i]+'<<')
        cat_file.write(vid_urls[i]+'<<')
        
        
        
    cat_file.close()

#url='http://m1.chia-anime.tv/show/overlord-ii/'
#chiascrap_rklmaker(url)


def chia_anime_animescrap_fast(url):
    #[title,vid_url]=roku.chia_download_vid('http://download.animepremium.tv/video/96994')
    #http://download.animepremium.tv/video/
    
    #url='http://m1.chia-anime.tv/show/aa-megami-sama-sorezore-no-tsubasa/'
    css='span.mug'
    attribute='style'
    
    if url[-1] != '/':url=url+'/'
    url=url+'&paged=1&order='
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    browser.get(url)
    html_source=browser.page_source
    anime_name=browser.title.replace('Watch ','').replace(' Episodes via mobile','')
    
    delay = 20 # seconds
    
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        print("Page is ready!")
        
        all_eps_list=browser.find_elements_by_css_selector('select')
        all_eps_num=len(all_eps_list[0].text.split('\n'))
        pagged_n=round_up(all_eps_num/30)
        
        
        css_obj=browser.find_elements_by_css_selector(css)
        css_url=[]    
        episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
        episode_name=[]
        down_url=[]
        
        for i in range(0,len(css_obj)):
            css_url.append(i)
            episode_name.append(i)
            episode_name[i]=episode_obj[i].text.replace('\n',' ')
            #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
            css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
            down_url.append(i)
            down_url[i]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
        #end for
        
    except TimeoutException:
        print("Loading took too much time!")
    
    
    
    if pagged_n>1:
        for pag in range(2,pagged_n+1):
            url=url.replace('&paged='+str(pag-1)+'&order=','&paged='+str(pag)+'&order=')
            browser.get(url)
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
                print("Page is ready!")
                
                
                css_obj=browser.find_elements_by_css_selector(css)
                episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
                
                for i in range(0,len(css_obj)):
                    ii=i+30*(pag-1)
                    css_url.append(i)
                    episode_name.append(ii)
                    episode_name[ii]=episode_obj[i].text.replace('\n',' ')
                    #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
                    css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
                    down_url.append(ii)
                    down_url[ii]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
                #end for
                
            except TimeoutException:
                print("Loading took too much time!")
        #end for
    #end if
    
    episode_name=list(reversed(episode_name))
    down_url=list(reversed(down_url))
    

 ########## link between functions   #########################################
     #browser.close()
 #    return [episode_name,down_url,name]
    url_list=down_url
 #def chia_download_vid_list(url_list):
    import random as rand
     
 #url_list=["http://download.animepremium.tv/video/97263","http://download.animepremium.tv/video/97345"]

#    from selenium import webdriver
#    from selenium.webdriver.support.ui import WebDriverWait
#    from selenium.webdriver.support import expected_conditions as EC
#    from selenium.webdriver.common.by import By
#    from selenium.common.exceptions import TimeoutException
#    browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
 #############################################################################
    
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB) 
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    ep_names=[]
    ep_vid_urls=[]
    for uli in range(0,len(url_list)):
    
        url=url_list[uli]
        browser.get(url)
        
        html_source=browser.page_source
        name=browser.title.replace('Download ','')
    
        if name=='not available yet':
            print('*ERROR: Bad url or episode is not available')
            return
            
        delay = 20 # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bttn.green')))
            #print("Page is ready!")
            #print(myElem.text,myElem.get_attribute('href'))
            #video=myElem.get_attribute('href')
        #        Page is ready!
        #        Server Zero http://cache2.animepremium.tv:8880/downloadcache/J7tWTedpC0NjEz-SrSJf1Q/1516339203/ynpoovepfz6q.html.mp4/Dragon-Ball-Super-Episode-122-chia-anime.com.mp4
            videos_obj=browser.find_elements_by_css_selector('a.bttn.green')
            videos_url=[]
            
            
            for i in range(0,len(videos_obj)):
                videos_url.append(i)
                videos_url[i]=videos_obj[i].get_attribute('href')
                
########################################
            ep_names.append(uli)
            ep_vid_urls.append(uli)
            n=rand.randint(0,len(videos_url)-2)
            [ep_names[uli],ep_vid_urls[uli]]=[name,videos_url[n]]
########################################
            
        except TimeoutException:
            print("Loading took too much time!")
            
    #end for uli
    
    browser.close()
    return [episode_name,down_url,anime_name,ep_names,ep_vid_urls]

##############################################################################
def chia_anime_animescrap_v2(browser,url):
    #[title,vid_url]=roku.chia_download_vid('http://download.animepremium.tv/video/96994')
    #http://download.animepremium.tv/video/
    
    #url='http://m1.chia-anime.tv/show/aa-megami-sama-sorezore-no-tsubasa/'
    css='span.mug'
    attribute='style'
    
    if url[-1] != '/':url=url+'/'
    url=url+'&paged=1&order='
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    #browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    browser.get(url)
    html_source=browser.page_source
    anime_name=browser.title.replace('Watch ','').replace(' Episodes via mobile','')
    
    delay = 20 # seconds
    
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
        print("Page is ready!")
        
        all_eps_list=browser.find_elements_by_css_selector('select')
        all_eps_num=len(all_eps_list[0].text.split('\n'))
        pagged_n=round_up(all_eps_num/30)
        
        
        css_obj=browser.find_elements_by_css_selector(css)
        css_url=[]    
        episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
        episode_name=[]
        down_url=[]
        
        for i in range(0,len(css_obj)):
            css_url.append(i)
            episode_name.append(i)
            episode_name[i]=episode_obj[i].text.replace('\n',' ')
            #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
            css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
            down_url.append(i)
            down_url[i]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
        #end for
        
    except TimeoutException:
        print("Loading took too much time!")
    
    
    
    if pagged_n>1:
        for pag in range(2,pagged_n+1):
            url=url.replace('&paged='+str(pag-1)+'&order=','&paged='+str(pag)+'&order=')
            browser.get(url)
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))
                print("Page is ready!")
                
                
                css_obj=browser.find_elements_by_css_selector(css)
                episode_obj=videos_obj=browser.find_elements_by_css_selector('tr')
                
                for i in range(0,len(css_obj)):
                    ii=i+30*(pag-1)
                    css_url.append(i)
                    episode_name.append(ii)
                    episode_name[ii]=episode_obj[i].text.replace('\n',' ')
                    #css_url[i]=roku.text_between(css_obj[i].get_attribute(attribute),'"','"')
                    css_url[i]=numbers_in_string(css_obj[i].get_attribute(attribute))
                    down_url.append(ii)
                    down_url[ii]=strjoin(['http://download.animepremium.tv/video/',css_url[i]])
                #end for
                
            except TimeoutException:
                print("Loading took too much time!")
        #end for
    #end if
    
    episode_name=list(reversed(episode_name))
    down_url=list(reversed(down_url))
    
    #browser.close()
    return [episode_name,down_url,anime_name,browser]

def chia_download_vid_list_v2(browser,url_list):
#url_list=["http://download.animepremium.tv/video/97263","http://download.animepremium.tv/video/97345"]
    import random as rand

    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    
    #browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB) 
    #browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    ep_names=[]
    ep_vid_urls=[]
    for uli in range(0,len(url_list)):
    
        url=url_list[uli]
        browser.get(url)
        
        html_source=browser.page_source
        name=browser.title.replace('Download ','')
        
        available=True
        if name=='not available yet':
            print('*ERROR: Bad url or episode is not available')
            available=False
            return
            
        delay = 20 # seconds
        try:
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bttn.green')))
            #print("Page is ready!")
            #print(myElem.text,myElem.get_attribute('href'))
            #video=myElem.get_attribute('href')
        #        Page is ready!
        #        Server Zero http://cache2.animepremium.tv:8880/downloadcache/J7tWTedpC0NjEz-SrSJf1Q/1516339203/ynpoovepfz6q.html.mp4/Dragon-Ball-Super-Episode-122-chia-anime.com.mp4
            videos_obj=browser.find_elements_by_css_selector('a.bttn.green')
            videos_url=[]
            
            
            for i in range(0,len(videos_obj)):
                videos_url.append(i)
                videos_url[i]=videos_obj[i].get_attribute('href')
                
########################################
            ep_names.append(uli)
            ep_vid_urls.append(uli)
            n=rand.randint(0,len(videos_url)-2)
            
            if available:
                [ep_names[uli],ep_vid_urls[uli]]=[name,videos_url[n]]
            else:
                [ep_names[uli],ep_vid_urls[uli]]=[name,'https://darkstuffsite.000webhostapp.com/videos/video_not_found.mp4']
########################################
            
        except TimeoutException:
            print("Loading took too much time!")
            
    #end for uli
    
    browser.close()    
    return [ep_names,ep_vid_urls]

def chiascrap_rklmaker_v2(anime_url):
    from selenium import webdriver
    browser = webdriver.Chrome(executable_path="C:\\c\\Python_projects\\chromedriver.exe")
    
    [episode_name,down_url,anime_name,browser]=chia_anime_animescrap_v2(browser,anime_url)
    #[episode_name,down_url,name,ep_names,ep_vid_urls]
    [ep_name,vid_urls]=chia_download_vid_list_v2(browser,down_url)
    
    anime_path=strjoin(['rkl\\',anime_name,'.rkl'])
    ensure_dir(anime_path)
    anime_data=animef_db(anime_name)
    
    
    cat_file=open(anime_path,'w')
    cat_file.write('<<series<<\n')
    cat_file.write('<<'+anime_name+'<<\n')
    cat_file.write('<<'+anime_data[1]+'<<\n')
    cat_file.write('<<'+anime_data[2]+'<<\n')
    
    
    for i in range(0,len(episode_name)):
        cat_file.write('\n<<'+episode_name[i]+'<<')
        cat_file.write(vid_urls[i]+'<<')
        
        
        
    cat_file.close()
    
    
class rkl_file:

    def __init__(self, full_dir):  
        self.full_dir = full_dir
        
        z=open(full_dir,'r', encoding="latin-1").read()
        z=z.strip()
        z=z.split('\n')
        z2=[]
        c=0
        for i in range(len(z)):
            if '<<' in z[i]:
                z2.append(c)
                z2[c]=z[i]
                c+=1
        self.lines=z2
        if 'series' in self.lines[0].lower():
            self.type='series'
            self.series_name=z2[1].replace('<<','')
            self.series_poster=z2[2].replace('<<','')
            self.series_desc=z2[3].replace('<<','')
            
            ep_names=[]
            ep_urls=[]
            media=[]
            c=0
            for e in range(4,len(z2)):
                ep_names.append(c)
                ep_urls.append(c)
                media.append(c)
                
                temp_line=z2[e].split('<<')                
                ep_names[c]=temp_line[1]
                ep_urls[c]=temp_line[2]
                
                media[c]=[temp_line[1],temp_line[2],self.series_poster,self.series_desc]
                
                c+=1
            
            
            self.media=media
            self.series_epnames=ep_names
            self.series_epurls=ep_urls
            
        elif 'movies' in self.lines[0].lower():
            self.type='movies'
            
            mov_names=[]
            mov_urls=[]
            mov_posters=[]
            mov_descs=[]
            media=[]
            c=0
            for e in range(1,len(z2)):
                mov_names.append(c)
                mov_urls.append(c)
                mov_posters.append(c)
                mov_descs.append(c)
                media.append(c)
                
                temp_line=z2[e].split('<<')
                mov_names[c]=temp_line[1]
                mov_urls[c]=temp_line[2]
                mov_posters[c]=temp_line[3]
                mov_descs[c]=temp_line[3]
                
                media[c]=temp_line[1:5]
                
                c+=1
                
            
            self.media=media
            self.movie_names=mov_names
            self.movie_urls=mov_urls
            self.movie_posters=mov_posters
            self.movie_descs=mov_descs
            

def format_filename(your_string):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    file_name=''
    s=your_string
    
    for x in s:
        if x.isalnum() or x in "._- ()":
            file_name+=x
        elif x in ('\\//'):
            file_name+='-'
        else:
            file_name+='-'
            
        file_name=strip_accents(file_name)
    return file_name


def strip_accents(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def valid_filename_win(s):
    import re
    ans=s
    # for c in 'CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8, LPT9'.split(', '):
    #     # ans=ans.replace(c,'-')
    #     insensitive_hippo = re.compile(re.escape(c), re.IGNORECASE)
    #     ans=insensitive_hippo.sub('-', ans)


    for c in '"*<>?\\|/:':
        ans=ans.replace(c,'-')
    ans=ans.strip('.')
    ans=ans.strip()
    ans=ans.strip('.')
    ans=ans.strip()
    return ans

def slugify(value, allow_unicode=False):
    import unicodedata
    import re
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    ovalue=str(value)
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
    value = re.sub(r"[^'$=,()\"&%.\w\s-]", '<', value)
    print(value)
    ans=re.sub(r'[\s]+', ' ', value).strip(' _').replace('<','-')
    if ans:
        ans=ans[0:-1] if ans[-1]=='.' else ans
    ans=ans.strip()
    # print(len(ans))
    if len(ans)==0:
        # return strip_accents(ovalue)
        from fold_to_ascii import fold
        folded=fold(ovalue).strip()
        if folded:
            return folded
        else:
            return valid_filename_win(ovalue)

    return ans

# s="st. james I\'maNul, mon ami - (2022) \"tower of god\" !#$%&/().txt"
# s="Все панки попадают в рай"
# print(s)
# print(slugify(s))


# print(valid_filename_win('aNul!"#$%&/().txt'))