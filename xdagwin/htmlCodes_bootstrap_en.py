header_en = """
<!doctype html>
<html lang="en">
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
                        <a class="dropdown-item text-light" href="index_en.html">English</a>
                        <a class="dropdown-item text-light" href="index.html">中文</a>
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
<div class="card-header"><strong>Game wallet：</strong></div>
<div class="card-body">
    <p class="card-text"><a href="https://explorer.xdag.io/block/rNjmn9TPaAWpePMcQZkA0sSDxYUgUaD+">rNjmn9TPaAWpePMcQZkA0sSDxYUgUaD+</a></p>
  </div>
</div></div>

<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>Rules：</strong>（<span style="color:#D20000">No fee</span>）</div>
<div class="card-body">
<h6>1、Maker：Transfer any amount of XDAG to game wallet that <strong>not equal</strong> to any of the amount on the list. <span style="color:#D20000">Every hour, top 10 makers will get 0.1% profits.</span>(no more than 1 XDAG/hour).
<br>2、Taker：Transfer an amount of XDAG that <strong>equal</strong> to the amount on the list, if the ID digit sum is bigger than that of the maker，you can earn double amount of XDAG, or the maker get double amount of XDAG.
<br>3、ID digit sum：The sum of all the digit of "FEE" address in the transaction blcok which you generated when transfer XDAG to game wallet.
<br>
<br><a href="ruleExample.html">An example of game rules</a></h6>
  </div>
</div></div>

<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>Maker list：</strong></div>
<div class="card-body">
<table id="table1" class="table table-hover table-responsive text-nowrap text-center table-sm">
<thead>
  <tr>
	<th>Amount</th>
    <th>ID digit sum</th>
    <th>ID</th>
    <th>Wallet</th>
  </tr>
 </thead>
 <tbody>
"""

tableFooter_en ="""
</tbody>
</table>
</div>
</div></div>
"""

tableHeader_en = """
<div class="container">
<div class="card border-light mb-3">
<div class="card-header"><strong>Recent result：</strong></div>
<div class="card-body">
<table class="table table-hover table-responsive text-nowrap table-sm">
<thead class="text-center">
  <tr>
  <th>Result</th>
  <th>Amount</th>
  <th>ID digit sum</th>
	<th>ID</th>
	<th>Wallet</th>
  </tr></thead>
   <tbody>
"""


footer_en = """
<div class="container text-center">Friends links: <a href="https://xdagpark.com">XDAG Park</a><br><br>Copyright 2018 xdagholder</div>
<script src="./sortTable.js"></script>
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
"""