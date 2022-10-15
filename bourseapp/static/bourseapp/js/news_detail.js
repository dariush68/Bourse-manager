$(function(){


});

function newsApproveByAdmin() {

    let url_newsApprove = $("#url-news-approve").attr("data-url");
     // alert(url_newsApprove);
     // return
    $("#modalNewsApprove").modal("hide");

    $.ajax({
        url: url_newsApprove,
        type: 'GET',
        // dataType: 'json',
        // data: query,
        success: function (data) {
            // alert(data)
            if(data.indexOf("news approved") > -1){
                $("#news-approve-status").addClass("d-none");
            }
        }
    })

}
