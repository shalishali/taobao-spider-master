# taobao-spider
淘宝商品数据爬虫，可以获取商品名称、价格、销量、位置、好评中评差评数。憋不出毕业论文心烦写的爬虫，喜欢给个star噢! thx<br>
使用指南:<br>
  -h  --help:   显示帮助信息.<br>
  -v  --ver:    显示脚本版本<br>
  -k  --key:    搜索关键词，默认 iphone7<br>
  -n  --num:    搜索页数，每页包含44条商品数据，如输入2，那说明会抓取2*44条商品数据<br>
  -f  --file:   获取的文件保存位置，默认为D:\iphone.txt<br>
使用实例：<br>
  <pre>python taobao.py -k 滑板鞋 -n 5 -f D:\huaban.txt</pre><br>
Python环境：python 3.*
