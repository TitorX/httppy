# coding=utf-8
__author__ = 'titorx'
import web
import os


MIME = {
    "rtf": "application/rtf",
    "jpeg": "image/jpeg",
    "tcl": "application/x-tcl",
    "jng": "image/x-jng",
    "mp3": "audio/mpeg",
    "mng": "video/x-mng",
    "xml": "text/xml",
    "img": "application/octet-stream",
    "jar": "application/java-archive",
    "ts": "video/mp2t",
    "tk": "application/x-tcl",
    "wml": "text/vnd.wap.wml",
    "jad": "text/vnd.sun.j2me.app-descriptor",
    "m4a": "audio/x-m4a",
    "bin": "application/octet-stream",
    "mpg": "video/mpeg",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "woff": "application/font-woff",
    "mov": "video/quicktime",
    "tif": "image/tiff",
    "hqx": "application/mac-binhex40",
    "jardiff": "application/x-java-archive-diff",
    "crt": "application/x-x509-ca-cert",
    "mp4": "video/mp4",
    "xls": "application/vnd.ms-excel",
    "htc": "text/x-component",
    "htm": "text/html",
    "webm": "video/webm",
    "webp": "image/webp",
    "sea": "application/x-sea",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "mpeg": "video/mpeg",
    "ico": "image/x-icon",
    "rpm": "application/x-redhat-package-manager",
    "kml": "application/vnd.google-earth.kml+xml",
    "dll": "application/octet-stream",
    "pem": "application/x-x509-ca-cert",
    "ra": "audio/x-realaudio",
    "kmz": "application/vnd.google-earth.kmz",
    "run": "application/x-makeself",
    "m3u8": "application/vnd.apple.mpegurl",
    "asx": "video/x-ms-asf",
    "js": "application/javascript",
    "msp": "application/octet-stream",
    "asf": "video/x-ms-asf",
    "mml": "text/mathml",
    "iso": "application/octet-stream",
    "pdf": "application/pdf",
    "pdb": "application/x-pilot",
    "xspf": "application/xspf+xml",
    "tiff": "image/tiff",
    "wmv": "video/x-ms-wmv",
    "ppt": "application/vnd.ms-powerpoint",
    "txt": "text/plain",
    "wbmp": "image/vnd.wap.wbmp",
    "jnlp": "application/x-java-jnlp-file",
    "ps": "application/postscript",
    "xpi": "application/x-xpinstall",
    "zip": "application/zip",
    "json": "application/json",
    "swf": "application/x-shockwave-flash",
    "gif": "image/gif",
    "msm": "application/octet-stream",
    "msi": "application/octet-stream",
    "war": "application/java-archive",
    "pl": "application/x-perl",
    "pm": "application/x-perl",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "bmp": "image/x-ms-bmp",
    "atom": "application/atom+xml",
    "ogg": "audio/ogg",
    "ear": "application/java-archive",
    "png": "image/png",
    "rss": "application/rss+xml",
    "dmg": "application/octet-stream",
    "der": "application/x-x509-ca-cert",
    "midi": "audio/midi",
    "flv": "video/x-flv",
    "doc": "application/msword",
    "deb": "application/octet-stream",
    "svgz": "image/svg+xml",
    "prc": "application/x-pilot",
    "ai": "application/postscript",
    "jpg": "image/jpeg",
    "rar": "application/x-rar-compressed",
    "avi": "video/x-msvideo",
    "7z": "application/x-7z-compressed",
    "shtml": "text/html",
    "sit": "application/x-stuffit",
    "3gpp": "video/3gpp",
    "mid": "audio/midi",
    "html": "text/html",
    "xhtml": "application/xhtml+xml",
    "css": "text/css",
    "3gp": "video/3gpp",
    "kar": "audio/midi",
    "m4v": "video/x-m4v",
    "exe": "application/octet-stream",
    "svg": "image/svg+xml",
    "eps": "application/postscript",
    "cco": "application/x-cocoa",
    "eot": "application/vnd.ms-fontobject",
    "wmlc": "application/vnd.wap.wmlc"
}


def static_handler(path):

    class StaticFileHandler(web.RequestHandler):

        """
        用以处理静态文件请求
        """

        static_dir_path = ''

        def handler(self):
            file_path = os.path.abspath(os.path.join(self.static_dir_path, self.request.url_param['path'].rstrip('/')))
            # 判断目标文件是否位于指定的目录下 以及 目标文件是否存在
            if (self.static_dir_path in file_path) and os.path.isfile(file_path):
                # 发送文件
                with open(file_path) as f:
                    self.response.body = f.read()
                # 获取文件的类型
                mime = MIME.get(os.path.basename(file_path).split('.')[-1], None)
                if mime:
                    self.response.set_header('Content-type', mime)
            else:
                self.response = web.Response404()

    setattr(StaticFileHandler, 'static_dir_path', os.path.abspath(path))
    return StaticFileHandler
