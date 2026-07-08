import sys, os, base64, re

def embed_images(html_path):
    html_dir = os.path.dirname(html_path)
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 匹配 src="images/xxx" 和 src="/absolute/path/xxx"
    def replace_src(match):
        src = match.group(1)
        # 跳过已经是base64或http的
        if src.startswith('data:') or src.startswith('http'):
            return match.group(0)
        
        # 解析实际文件路径
        if src.startswith('/'):
            img_path = src
        else:
            img_path = os.path.join(html_dir, src)
        
        if not os.path.exists(img_path) or os.path.getsize(img_path) == 0:
            print(f"  ⚠️ 图片不存在或为空: {img_path}")
            return match.group(0)
        
        # 判断mime
        ext = os.path.splitext(img_path)[1].lower()
        mime = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif', 'webp': 'image/webp'}.get(ext.lstrip('.'), 'image/jpeg')
        
        with open(img_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('ascii')
        
        print(f"  ✅ 内嵌: {src} ({os.path.getsize(img_path)//1024}KB)")
        return f'src="data:{mime};base64,{b64}"'
    
    html = re.sub(r'src="([^"]*)"', replace_src, html)
    
    out_path = html_path.replace('.html', '-embedded.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  输出: {out_path}")
    print(f"  文件大小: {os.path.getsize(out_path)//1024}KB")
    return out_path

if __name__ == '__main__':
    for html_path in sys.argv[1:]:
        print(f"\n处理: {html_path}")
        embed_images(html_path)
