new WOW().init();
// new SmoothScroll('a[href*="#"]'),
//     {
//     easing:'linear',
//     speed:1000
// };

// add name to breadcrumb
//-- used hidden input in base.html to access django url --//
//-- pagination parameters --//
let nextPage = null;
let currentPage = 1;
let itemCount = -1;     //-- total count of item in the database --//
let itemPerPage = 8;   //-- fetched item count in each try --//
let loading = $("#main-page-loading");

console.log("Main Page");
loading.addClass('loading');
$(window).on('scroll load' , function () {
    //console.log("h = " + $(window).scrollTop());
    if  ($(window).scrollTop()>300){

        $('#go-to-top').css('opacity','1').css('visibility' ,'visible');
    }else
        {
        $('#go-to-top').css('opacity','0').css('visibility' ,'hidden');
    }
});

$("#class-news-approve-status").on("click",function(){
    console.log("kjhkjhkjh")
  var newsId =  $(this).attr("data-id");
  var newsTitle =  $(this).attr("data-title");
  console.log(newsId)
  //post code
});

function newsApproveByAdminInIndex(newsId) {


    let url_newsApprove = $("#url-news-approve-id").attr("data-url").replace(/12345/, newsId.toString());

     // alert(url_newsApprove);
     // return
    $("#modalNewsApproveIndex").modal("hide");

    $.ajax({
        url: url_newsApprove,
        type: 'GET',
        // dataType: 'json',
        // data: query,
        success: function (data) {
            // alert(data)
            if(data.indexOf("news approved") > -1){
                $("#class-news-approve-status1-"+ newsId).addClass("d-none");
                $("#class-news-approve-status2-"+ newsId).addClass("d-none");
            }
        }
    })

}

showLimitedCountOfAnalyzedSymbols(10);

//-- show 10 item of analyzed symbols --//
function showLimitedCountOfAnalyzedSymbols(count) {

    $(".symbol-analyzed-tile").each(function (index) {

        if(index <= count){
            $(this).removeClass("d-none");
        }
    });

}