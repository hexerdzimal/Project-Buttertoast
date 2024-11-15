from Engine.plugin_Interface import plugin_Interface

class Svg(plugin_Interface):    
    def run(self, truecrypt, svg_host):        
        offset = svg_host.find(b'>')
        comment_start = (b'<!--')
        comment_end = (b'//-->')    
        polyglott = svg_host[:offset+1] + comment_start + truecrypt[offset+5:] + comment_end + svg_host[1+offset:]

        return polyglott