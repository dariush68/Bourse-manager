$(document).ready(function(){

    let all_symbols_analyzed = [];
    //-- save all symbols --//
    $(".mc-symbol-tile").each(function (index, obj) {

        all_symbols_analyzed.push($(this))
        });

    $("#search-symbols-analyzed").on("keyup", function() {

        let search = $("#search-symbols-analyzed").val();
        $(".mc-symbol-tile").each(function (index, obj) {

          // console.log($(this).attr('value').indexOf(search))
            if($(this).attr('value').indexOf(search) == -1){
                $(this).addClass('d-none');
            }
            else{
                $(this).removeClass('d-none');
            }
        });

        //-- category tile --//
        $(".mc-category-symbols-analyze").each(function (index) {

            let isHide = true;
            $(this).find('.mc-symbol-tile').each(function () {
                if(!$(this).hasClass('d-none')) isHide = false
            });
            if(isHide){ $(this).addClass('d-none')  }
            else{ $(this).removeClass('d-none') }
        });

        //-- col tile --//
        $(".mc-col-symbols-analyze").each(function (index) {

            let isHide = true;
            $(this).find('.mc-category-symbols-analyze').each(function () {
                if(!$(this).hasClass('d-none')) isHide = false
            });
            if(isHide){ $(this).addClass('d-none') }
            else{  $(this).removeClass('d-none') }
        });

    });

});