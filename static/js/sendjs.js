/**
 * Created by hyh on 2017/7/18.
 */
var xmlHttp;
var pagecount=1;


<!--创建XMLHttpRequest对象-->
function createXMLHttpRequest()
{
    //判断浏览器是否支持ActiveXObject对象
    if(window.ActiveXObject)
    {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    //判断浏览器是否支持XMLHttpRequest对象
    else if (window.XMLHttpRequest)
    {
        xmlHttp = new XMLHttpRequest();
    }
}
<!--如果一切正常，在客户端显示simple.xml中的内容-->
function handleStateChange() {
    if (xmlHttp.readyState == 4) {
        if (xmlHttp.status == 200) {

            $('#content').html(xmlHttp.response);

        }
    }
}


function newsearch() {
    createXMLHttpRequest();
    //设置在请求结束后调用handleStateChange函数
    xmlHttp.onreadystatechange = handleStateChange;
    //用get方法请求服务器端的simple.xml
    xmlHttp.open("POST","newsearch",true);

    var search=document.getElementById("searchkey").value;
    //发送请求
    var form=new FormData();
    form.append("name",search);
    console.log(form);
    xmlHttp.send(form);
}

function searchinresult() {

    createXMLHttpRequest();
    //设置在请求结束后调用handleStateChange函数
    xmlHttp.onreadystatechange = handleStateChange;
    //用get方法请求服务器端的simple.xml
    xmlHttp.open("POST","addsearch",true);

    var search=document.getElementById("searchkey").value;
    var data=search;
    var form=new FormData();
    form.append("name",data);
    console.log(form);
    xmlHttp.send(form);

}

function searchgroupby(btn) {

    createXMLHttpRequest();
    //设置在请求结束后调用handleStateChange函数
    xmlHttp.onreadystatechange = handleStateChange;
    //用get方法请求服务器端的simple.xml
    xmlHttp.open("POST","addsearchandterm",true);

    var search=btn.value;
    var field=btn.name;
    var data=search+"@"+field;
    var form=new FormData();
    form.append("name",data);
    console.log(form);
    xmlHttp.send(form);
}

function sendpageid() {

    createXMLHttpRequest();
    //设置在请求结束后调用handleStateChange函数
    xmlHttp.onreadystatechange = handleStateChange;
    //用get方法请求服务器端的simple.xml
    xmlHttp.open("POST","getmore",true);

    pagecount++;
    var form=new FormData();
    form.append("name",pagecount);
    xmlHttp.send(form);
}

function recommondDetail(btn) {
    createXMLHttpRequest();
    //设置在请求结束后调用handleStateChange函数
    xmlHttp.onreadystatechange = handleStateChange;
    //用get方法请求服务器端的simple.xml
    xmlHttp.open("POST","recommondDetail",true);
    // 添加超时
    xmlHttp.timeout = 300000;

    var id=btn.value;
    var form=new FormData();
    form.append("id",id);
    xmlHttp.send(form);

}
