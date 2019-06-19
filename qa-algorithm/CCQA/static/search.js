/**
 * Created by flyboss on 2018/12/26.
 */
$(document).ready(function () {
    if (getCookie("ordianrySearch") != "") {
        $('#query').val(getCookie("ordianrySearch"));
    }
    if (getCookie("notSendQuery") === "yes") {
        setCookie("notSendQuery", "no");
        $("#answer").empty();
        var question = {
            "name": getCookie("name"),
            "rule": getCookie("rule"),
            "benefit": getCookie("benefit"),
            "weakness": getCookie("weakness"),
            "exception": getCookie("exception")
        };
        $.ajax({
            type: 'POST',
            url: address + "/advanceSearch",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify(question),
            success: function (result) {
                if (result.status === "success") {
                    var json = result.data;
                    if ($.isEmptyObject(json) || json === []) {
                        $("#answer").append("<p>don't know</p>");
                    } else {
                        for (var i = 0; i < json.length; ++i) {
                            displayEntity(json[i]);
                            $("#answer").append("<hr style='border: 1px solid lightgray;'>");
                        }
                        Prism.highlightAll();
                    }
                } else {
                    $("#answer").append("<p>" + result.error_msg + "</p>");
                }
                sethash();
            },
            error: function (result) {
                $("#answer").append("<p>" + result + "</p>");
            }
        });
    }
    $("#ordinarysearch").click(function () {
        setCookie("ordianrySearch", $('#query').val());
        $("#answer").empty();
        var query = $('#query').val();
        var question = {"question": query};
        $.ajax({
            type: 'POST',
            url: address + "/ordinarySearch",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify(question),
            success: function (result) {
                if (result.status === "success") {
                    var json = result.data;
                    if ($.isEmptyObject(json) || json === []) {
                        $("#answer").append("<p>don't know</p>");
                    } else {
                        for (var i = 0; i < json.length; ++i) {
                            displayEntity(json[i]);
                            $("#answer").append("<hr style='border: 1px solid lightgray;'>");
                        }
                        Prism.highlightAll();
                    }
                } else {
                    $("#answer").append("<p>" + result.error_msg + "</p>");
                }
                
            },
            error: function (result) {
                $("#answer").append("<p>" + result + "</p>");
            }
        });
    });
   
    
});



