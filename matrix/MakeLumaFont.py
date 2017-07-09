from luma.core.legacy.font import CP437_FONT
import functools, operator
import binascii

class MakeLumaFont:

    def __init__(self):
        pass

    def main(self):
        source_file='/home/pi/kdev/misaki/misaki_gothic.bdf'        
        #source_file='./misaki_gothic.bdf'
        #source_file='./misaki_4x8_iso8859.bdf'
        fp=open(source_file, 'r')
        s = fp.readline()

        if s[:13] != "STARTFONT 2.1":
            raise SyntaxError("not a valid BDF file")

        props = {}
        while True:
            s = fp.readline()
            if not s or s[:13] == "ENDPROPERTIES":
                break

            i = s.find(" ")
            props[s[:i]] = s[i+1:-1]
            if s[:i] in ["COMMENT", "COPYRIGHT"]:
                if s.find("LogicalFontDescription") < 0:
                    comments.append(s[i+1:-1])

            #font = props["FONT"].split("-")

            font = []
            utf8_dic={}
            while True:
                c = self.__bdf_char(fp)
                if not c:
                    break

                id, ch, (xy, dst, src), bitmap = c
                font_list=self.__makeList(bitmap)
                # jisの文字コードを作成
                jis=bytes('1b2442'+id+'1b2842', 'iso-2022-jp')
                # UTF-8に変更
                utf8=''
                ord_id=0
                try:
                    utf8=binascii.a2b_hex(jis).decode('iso-2022-jp')
                    ord_id=ord(utf8)
                except:
                    # 無意味な処理
                    pass
                    #print(sys.exc_info()[0])

                utf8_dic[ord_id]=font_list

            font_list=[]
            for i in range(0,65509):
                if i > 255:
                    font_list.append(utf8_dic.get(i,[]))
                else:
                    # asciiフォントは既存のfontを使う
                    font_list.append(CP437_FONT[i])

            return(font_list)
        
    def __bdf_char(self,f):
        '''
        bdfファイルからchar毎にlumaのfont形式に変換する
        '''
        # skip to STARTCHAR
        while True:
            s = f.readline()
            if not s:
                return None
            if s[:9] == "STARTCHAR":
                break

        id = s[9:].strip()

        # load symbol properties
        props = {}
        while True:
            s = f.readline()
            if not s or s[:6] == "BITMAP":
                break
            i = s.find(" ")
            props[s[:i]] = s[i+1:-1]
        
        # load bitmap
        bitmap = []
        while True:
            s = f.readline()
            if not s or s[:7] == "ENDCHAR":        
                break
            bitmap.append(s[:-1])

        bitmap = ",".join(bitmap)    

        # lumaが利用するfontの形式に変換する
        [x, y, l, d] = [int(s) for s in props["BBX"].split()]
        [dx, dy] = [int(s) for s in props["DWIDTH"].split()]

        bbox = (dx, dy), (l, -d-y, x+l, -d), (0, 0, x, y)

        return id, int(props["ENCODING"]), bbox, bitmap


    def __makebit(self,ff, line):
        '''
        bdfのbitmap表記から配列形式でのbitmapに変換する
        '''
        tgt=int(ff, 16)
        MAX_BIT = 8 #最大のbit数
        bit=[]
        for i in range(0,MAX_BIT):
            dot=0
            if( tgt>>MAX_BIT-1-i & 1 ) == 1:
                dot=1

            bit.append(dot)

        bit=list(map(lambda x: 2**line*x,bit))

        return(bit)

    def __makeList(self, bitmap):
        '''
        '''
        bit_list=bitmap.split(',')
        line=0
        font_seed=[]
        for ff in bit_list:
            bit=self.__makebit(ff, line)
            font_seed.append(bit)
            line+=1

        new_list=[functools.reduce(operator.add,x) for x in zip(*font_seed)]

        return(new_list)

