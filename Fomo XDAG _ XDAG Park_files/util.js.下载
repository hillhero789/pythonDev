function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires+"; path=/"; 
}
function getCookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
}


function checkCookie(){
    var user=getCookie("username");
    if (user!=""){
        alert("欢迎 " + user + " 再次访问");
    }
    else {
        user = prompt("请输入你的名字:","");
          if (user!="" && user!=null){
            setCookie("username",user,30);
        }
    }
}

function getIP(){

}

function getLocationByIP(ip){

}

function getLanguage(){
	var cookieName = "GeekCashTreasureGame";
	var lang = getCookie(cookieName);
	if(lang == null || lang == ""){
		lang = navigator.language || navigator.userLanguage;
		if(lang.substr(0,3) == 'zh-') {
			// Load Chinese
			//window.location.href='./ch/index.html';
			lang="ch";
			setCookie(cookieName,lang,365);
		}
		else{
			// Load English
			//window.location.href='./en/index.html';
			lang="en";
			setCookie(cookieName,lang,365);
		}
	}
	return lang;
}

function isChinese(){
	var lang = getLanguage();
	return lang == "ch";
}

function isEnglish(){
	var lang = getLanguage();
	return lang == "en";
}

function setChineseLangCookie(){
	var cookieName = "GeekCashTreasureGame";
	var lang = "ch";
	setCookie(cookieName, lang, 365);
}

function setEnglishLangCookie(){
	var cookieName = "GeekCashTreasureGame";
	var lang = "en";
	setCookie(cookieName, lang, 365);
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&#]*)/gi,
        function(m,key,value) {
            vars[key] = value;
        }
    );
    return vars;
}


function timestampToLocalTime(timestamp) {

    var Y,M,D,h,m,s
    var timestamp= parseInt(timestamp)
    var date = null
    if (timestamp.toString().length == 10) {

        date = new Date(timestamp * 1000); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
    } else if (timestamp.toString().length == 13) {
        date = new Date(timestamp); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
    }
    Y = date.getFullYear() + '-';
    M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
    D = date.getDate() + ' ';
    h = date.getHours() + ':';
    m = date.getMinutes() + ':';
    s = date.getSeconds();
    return Y + M + D; //这里自定义返回 需要后面的加上就好了

}

function padLeftZero (str) {
    return ('00' + str).substr(str.length)
}