/**
 * Created by flyboss on 2019/1/2.
 */


$(document).ready(function () {
    if (getCookie("code") !== "") {
        $("#code").val(decodeURIComponent(getCookie("code")));
    }else{
//        $("#code").val("check if the code is normative");
    }
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode:"text/x-java",
        lineNumbers: true
    });
    $("#check").click(function () {
        if($("#result").is(":hidden")){
            $("#result").show();
        }
        $("#result").empty();
        var query = editor.getValue();
        setCookie("code", encodeURIComponent(query));
        var question = {"code": query};
        console.log(question)
        $.ajax({
            type: 'POST',
            url: address + "/checkCode",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify(question),
            success: function (result) {
                console.log(result);
                if (result.status==="success"){
                    var json = result.data;
                    if (json.length===0){
                        $("#result").append("<div>Sorry,we can only analyze a complete Java class without syntax errors." 
                        		+"</div>>");
                    }else{
                        for (var i=0;i<json.length;i++){
                            $("#result").append("<p>"+json[i]+"</p>");
                        }
                    }
                }else{
                    $("#result").append("<p>"+result.error_msg+"</p>>");
                }
                sethash();
            },
            error: function (result) {
                console.log(result);
                $("#result").append(result);
            }
        });
    });
    function sethash(height){
        var iframeH;
        if(height != null || height != undefined){
            iframeH = height;
        }
        else{
            iframeH = $(document.body).outerHeight(true);
        }
        var message = "参数%" + iframeH + "%" + (new Date().getTime());
        //向父页面传递参数
        window.parent.postMessage(message, 'http://202.120.40.28:4463/index.html');
    }
});