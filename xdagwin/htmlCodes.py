header = """
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Welcome to XDAG holder!</title>
<style>
	    body {
			font-size: 14px;
			margin: 30px 30px;
			background:#C4CEBF;
			color:#333333
		}
		a {
			color:#D20000;
			text-decoration:none;
		}
		a:visited {
			color:#D20000
		}
		 
		table {
		  border-bottom: 5px solid #ACBAA5;
		  border-right: 5px solid #ACBAA5;
		  /*border-radius: 5px;*/
		  background-color: #ffffff;
		  width:100%;
		  font-size:14px;
		  align:center;
		  border-spacing: 1px
		}
 
		th {
		  background-color:#466871;
		  color: rgba(255,255,255,0.9);
		  cursor: pointer;
		}
		td {
		  background-color: #C4CEBF;
		}
		
		th, td {
		  min-width: 90px;
		  padding: 7px 7px;
		}
	</style>
<meta http-equiv="refresh" content="60"> 
</head>
<body>
<p style="text-align:center;font-weight:bold;font-size:18px">游戏地址（Game wallet）： <a href="https://explorer.xdag.io/block/zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF"><span class="STYLE1">zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF</span></a></p>
<p style="font-weight:bold">挂单列表 （Available list）：</p>
<table id="table1">
  <tr>
	<th>数量 （Amount）</th>
    <th>交易ID数字和 （Tx ID digit sum）</th>
    <th>交易ID （Tx ID）</th>
    <th>钱包 （Wallet）</th>
  </tr>
"""



tableHeader = """
<br>
<p style="font-weight:bold">最近结果 （Recent results）：</p>
<table>
  <tr>
  <th>钱包 （Wallet）</th>
  <th>交易ID （Tx ID）</th>
  <th>交易ID数字和 （Tx ID digit sum）</th>
	<th>数量 （Amount）</th>
	<th>结果 （Result）</th>
  </tr>
"""
tableFooter ="""
</table>
"""

footer = """
<p style="font-weight:bold">游戏规则：（<span style="color:#D20000">测试阶段无任何手续费</span>）</p>
<p>1、挂单：转入不等于挂单列表数量的XDAG（如想撤单可以再向游戏钱包转入相同数量的XDAG，则所有XDAG会自动转回到你的钱包）
<br>2、吃单：转入等于挂单列表数量的XDAG，如交易ID数字和与表中的交易ID数字和相加为偶数，则立即获得两倍数额的XDAG，为奇数则挂单者获得两倍数额的XDAG
<br>3、交易ID数字和：将传输区块中 “FEE” 地址中的 <b>数字</b> 进行 <b>累加</b> 即可得到</p>
<script src="./sortTable.js"></script>
"""