/**
 * Created by flyboss on 2019/1/9.
 */
$(document).ready(function () {
    getAdvanceCookie();
    $("#advancesearch").click(function () {

        setAdcanceCookie();
        window.location.href = address + "/ordinary";
        // $("#answer").empty();
        // var question = {
        //     "name": $("#name").val(), "rule": $("#rule").val(),
        //     "benefit": $("#benefit").val(), "weakness": $("#weakness").val(), "exception": $("#exception").val()
        // };
        // $.ajax({
        //     type: 'POST',
        //     url: address + "/advanceSearch",
        //     contentType: "application/json; charset=utf-8",
        //     dataType: "json",
        //     data: JSON.stringify(question),
        //     // contentType:"application/x-www-form-urlencoded",
        //     success: function (result) {
        //         var json = result.data;
        //         if (!$.isEmptyObject(json)) {
        //             for (var i = 0; i < json.length; ++i) {
        //                 displayEntity(json[i]);
        //             }
        //             Prism.highlightAll();
        //         }
        //     },
        //     failure: function (result) {
        //         alert(result);
        //     },
        //     error: function (result) {
        //         alert(result);
        //     }
        // });
    });
    
   
});

function getAdvanceCookie() {
    if (getCookie("name") !== "") {
        $("#name").val(getCookie("name"));
    }
    if (getCookie("rule") !== "") {
        $("#rule").val(getCookie("rule"));
    }
    if (getCookie("benefit") !== "") {
        $("#benefit").val(getCookie("benefit"));
    }
    if (getCookie("weakness") !== "") {
        $("#weakness").val(getCookie("weakness"));
    }
    if (getCookie("exception") !== "") {
        $("#exception").val(getCookie("exception"));
    }
}

function setAdcanceCookie() {
    var nameValue = $('#name').val();
    nameValue = $.trim(nameValue);
    setCookie("name", nameValue);
    var ruleValue = $('#rule').val();
    ruleValue = $.trim(ruleValue);
    setCookie("rule", ruleValue);
    var benefitValue = $('#benefit').val();
    benefitValue = $.trim(benefitValue);
    setCookie("benefit", benefitValue);
    var weaknessValue = $('#weakness').val();
    weaknessValue = $.trim(weaknessValue);
    setCookie("weakness", weaknessValue);
    var exceptionValue = $('#exception').val();
    exceptionValue = $.trim(exceptionValue);
    setCookie("exception", exceptionValue);

    var ordinarySearch = "";
    if (nameValue !== "") {
        ordinarySearch += "-n " + "'" + nameValue + "'";
    }
    if (ruleValue !== "") {
        ordinarySearch += " -r " + "'" + ruleValue + "'";
    }
    if (benefitValue !== "") {
        ordinarySearch += " -b " + "'" + benefitValue + "'";
    }
    if (weaknessValue !== "") {
        ordinarySearch += " -w " + "'" + weaknessValue + "'";
    }
    if (exceptionValue !== "") {
        ordinarySearch += " -e " + "'" + exceptionValue + "'";
    }
    setCookie("ordianrySearch", ordinarySearch);
    setCookie("notSendQuery", "yes");
}