from Engine.plugin_Interface import plugin_Interface

class Html(plugin_Interface):    
    def run(self, truecrypt, html_host):        
        offset = html_host.find(b'>')
        if offset == -1:
            print("No HTML found!")
        else:
            comment_start = (b'<!--')
            comment_end = (b'//-->')    
            polyglott = html_host[:offset+1] + comment_start + truecrypt[offset+5:] + comment_end + html_host[1+offset:]
        
        return polyglott