header = """
<!doctype html>
<html lang="zh-CN">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<link href="https://xdag.io/assets/images/fav/favicon.png" rel="icon">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Welcome to XDAG holder!</title>
<meta http-equiv="refresh" content="60"> 
</head>

<body>
<nav class="navbar navbar-expand-lg navbar-expand-sm navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="index.html"><img src="https://xdag.io/assets/images/fav/favicon.png" class="img-responsive" alt="Responsive image"><span class="font-weight-bold"> XDAG Holder</span></a>
        <ul class="nav justify-content-end">
            <button class="navbar-toggler collapsed" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="navbar-collapse collapse" id="navbarNav" style="">
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle text-light" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Language
                    </a>
                    <div class="dropdown-menu bg-dark" aria-labelledby="navbarDropdown">
                        <a class="dropdown-item text-light" href="#" onclick="alert('Coming soon, stay tuned!')">English</a>
                        <a class="dropdown-item text-light" href="#">中文</a>
                    </div>
                </li>
            </div>
        </ul>
    </div>
</nav>
<div class="container-fluid">

<div class="container text-center">
<br>
<div class="card border-light mb-3">
<div class="card-header"><strong>游戏地址：</strong></div>
<div class="card-body">
    <p class="card-text"><a href="https://explorer.xdag.io/block/zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF">zEHEOBggVqqAhQ4XQWTIIGFI4tmysxJF</a></p>
  </div>
</div></div>

<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>游戏规则：</strong>（<span style="color:#D20000">测试阶段无任何手续费</span>）</div>
<div class="card-body">
<h6>1、挂单：转入<strong>不等于</strong>挂单列表数量的XDAG（如想撤单可以再向游戏钱包转入相同数量的XDAG，则所有XDAG会自动转回到你的钱包）
<br>2、吃单：转入<strong>等于</strong>挂单列表数量的XDAG，如转账后生成的ID数字和大于表中的挂单的ID数字和，则立即获得两倍数额的XDAG，否则挂单者获得两倍数额的XDAG（相等时挂单者胜）
<br>3、ID数字和：将传输区块中 “FEE” 地址中的所有 <b>数字</b> 进行 <b>累加</b> 即可得到
<br>
<br><a href="ruleExample.html">游戏规则示例</a></h6>
  </div>
</div></div>

<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>挂单列表：</strong></div>
<div class="card-body">
<table id="table1" class="table table-hover table-responsive text-nowrap text-center table-sm">
<thead>
  <tr>
	<th>数量</th>
    <th>ID数字和</th>
    <th>ID</th>
    <th>钱包</th>
  </tr>
 </thead>
 <tbody>
"""

tableFooter ="""
</tbody>
</table>
</div>
</div></div>
"""

tableHeader = """
<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>最近结果：</strong></div>
<div class="card-body">
<table class="table table-hover table-responsive text-nowrap table-sm">
<thead class="text-center">
  <tr>
  <th>结果</th>
  <th>数量</th>
  <th>ID数字和</th>
	<th>ID</th>
	<th>钱包</th>
  </tr></thead>
   <tbody>
"""


footer = """
<div class="container text-center"><br>Copyright 2018 xdagholder</div>
<script src="./sortTable.js"></script>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
"""