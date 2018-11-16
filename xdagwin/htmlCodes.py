header = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title></title>
<style type="text/css">
<!--
.STYLE1 {
	color: #FF0000;
	font-weight: bold;
}
-->
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
</style>
</head>

<body>
<p>游戏地址： <a href="https://explorer.xdag.io/block/dvNo7wYcVz4zl6qRUy+twdFZv7vIJiuW"><span class="STYLE1">dvNo7wYcVz4zl6qRUy+twdFZv7vIJiuW</span></a></p>
<p>游戏规则：（<span class="STYLE1">测试阶段无任何手续费</span>）</p>
<p>1、挂单：转入不等于下表数量的XDAG</p>
<p>2、吃单：转入等于下表数量的XDAG，如哈希值大于下表哈希值，则立即获得相同数额的XDAG</p>
<p>3、传输哈希值计算方法：将传输哈希中的数字进行累加</p>
<table class="gridtable">
  <tr>
    <td>传输哈希</td>
    <td>哈希值</td>
    <td>数量</td>
  </tr>
"""

footer = """
</table>
</body>
</html>
"""