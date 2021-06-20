<h2>SetDisplayMode</h2>
<p><em>在保证笔记本电脑屏幕处于最佳分辨率的前提下，根据电源模式自动设置屏幕亮度、刷新率，适用于安装了Windows系统的笔记本电脑</em></p>
<h3>说明</h3>
<ul>
    <li>该程序每隔2分钟检查一次笔记本电脑是否充电及电池状态，将屏幕显示参数写入<strong>log</strong>目录下的<strong>SetDisplayMode-INFO.log</strong>文件，可以通过检查该文件是否正常写入内容判断程序是否正常运行</li>
    <li>如果笔记本电脑连接了电源，屏幕亮度调至100%。如果笔记本电脑屏幕支持可变刷新率，屏幕刷新率调至最高</li>
    <li>如果笔记本电脑使用电池供电，屏幕亮度根据电池余量从80%逐渐降至50%。如果笔记本电脑屏幕支持可变刷新率，屏幕刷新率调至最低</li>
    <li>该程序首次运行时自动安装Python和依赖库，请耐心等待。程序通过Windows任务计划程序实现后台运行</li>
    <li>该程序在联想小新 Pro16 GTX1650（Windows 10)上进行了测试</li>
</ul>
<h3>用法</h3>
<ul>
    <li>将程序解压</li>
    <li>运行 <strong>start.bat</strong>，提示安装成功后关闭窗口，注意不要删除程序</li>
</ul>
<h3>文件</h3>
<ul>
    <li>start.bat： 安装/启动 程序</li>
</ul>
<h3>目录</h3>
<ul>
    <li>.venv： Python运行环境</li>
    <li>conf： 配置信息</li>
    <li>core： 主程序</li>
    <li>init：程序初始化、打包</li>
    <li>log： 运行日志</li>
    <li>output： 运行结果</li>
    <li>source： 引用资源</li>
</ul>