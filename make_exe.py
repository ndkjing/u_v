from PyInstaller.__main__ import run

if __name__ == '__main__':
    opts = ['start.py',  # 主程序文件
            '-n u_v',  # 可执行文件名称
            '-F',  # 打包单文件
            # '-w', #是否以控制台黑窗口运行
            r'--icon=F:\pythonProject\ship\statics\planet.ico',  # 可执行程序图标
            '-y',
            '--clean',
            '--workpath=build',
            # '--add-data=res;templates',  # 打包包含的html页面
            '--add-data=statics;statics',  # 打包包含的静态资源
            '--distpath=build',
            '--specpath=./'
            ]
    run(opts)

