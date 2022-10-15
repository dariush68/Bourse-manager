let isProfilo;

// Tooltips Initialization
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function(){


	let timer_member;
    $('#search-user-add-symbol').on('keyup', function (e) {

		clearTimeout(timer_member);
		timer_member =setTimeout(function(){

			console.log($("#search-user-add-symbol").val());
			addSymbol($("#search-user-add-symbol").val());

			}, 600);

    });

    loadAllRequestedSymbols();
    loadAllPortfolioSymbols();

});


function addSymbol(search) {

    let url_symbolList = $("#url-symbol-list").attr("data-url");
// alert(url_symbolList);
// return

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': search,
            'page_size': 20,
        },
        success: function (data) {
            // console.log(data);
            let container = $("#container-user-pannel-symbols");
            container.empty();

            for(let i=0; i< data.length; i++){

                container.append(
                    `<a onclick="addTag('${data[i].id}', '${data[i].symbol}')" style="color: #515151">` +
                        `<div class="row  mb-1">` +
                            `<i class="fa fa-angle-double-left ml-1 mt-1 text-black-50"></i>` +
                            `${data[i].symbol}` +
                            `<small class="mr-1 mt-1">(${data[i].fullName})</small>` +
                        `</div>` +
                    `</a>`

                    /*`<li id="member-${data[i].id}" value="${data[i].id}" data-page="1" class="myclass-member-tile p-1 border-bottom" style="margin-right: -30px">` +
                    `<a onclick="selectMember('member-'+${data[i].id})" class="d-flex justify-content-between">` +
                    `<img src="${img_member}" alt="avatar" class="avatar rounded-circle d-flex align-self-center img-thumbnail" style="object-fit: contain; width: 60px; height: 60px;">` +
                    `<div class="text-small text-right mr-1">` +
                    `<small dir="ltr">@${data[i].username}</small>` +
                    `<p class="last-message text-muted mb-0">${data[i].first_name} ${data[i].last_name}</p>` +
                    `</div>` +
                    `<div class="text-small text-right" >` +
                    `<p class="text-smaller text-muted mb-0">Just now</p>` +
                    `<span class="badge badge-danger float-left d-none">1</span>` +
                    `</div>` +
                    `</a>` +
                    `</li>`*/
                );
            }

        },
        fail: function (e) {
            console.log('error', e);
        }
    })

}

function addTag(symbolId, symbolTitle) {
    // console.log(symbolId, symbolTitle)

    let container = $("#container-selected-symbols-tag");
    container.append(
        `<div class="chip" data-id="${symbolId}">` +
            `${symbolTitle}` +
            `<i class="close fas fa-times"></i>` +
        `</div>`
    )
}

function clearModal(isProfiloItem) {
    isProfilo = isProfiloItem;
    let container = $("#container-selected-symbols-tag");
    container.empty();
    $('#search-user-add-symbol').val('');
}

function modalApproveButton() {

    let container = $("#container-selected-symbols-tag");
    let datat = [];
    $('.chip').each(function (index) {
        console.log($(this).attr('data-id'));
        datat.push(
            $(this).attr('data-id')
        );
    });

    let url_symbolAdd = $("#url-symbol-req-add").attr("data-url");
    if(isProfilo){
        url_symbolAdd = $("#url-symbol-portfolio-add").attr("data-url");
    }
// alert(url_symbolList);
// return

    $.ajax({
        url: url_symbolAdd,
        type: 'GET',
        dataType: 'json',
        data: {
            'symbols': datat
        },
        success: function (res) {
            // console.log(res);
            if(res.data.indexOf('symbols added') > -1){
                 if(isProfilo){
                     loadAllPortfolioSymbols();
                 }
                 else{
                     loadAllRequestedSymbols();
                 }

                $('#centralModalSm').modal('hide');
            }
        },
        fail: function (e) {
            console.log('error', e);
        }
    })
}

function loadAllRequestedSymbols() {

    let url_symbolList = $("#url-symbol-req-list").attr("data-url");
// alert(url_symbolList);
// return

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': user_id
        },
        success: function (data) {
            // console.log(data);
            // return;
            let container = $("#container-symbol-req-list");
            container.empty();
            let base = $('#url-base').attr('data-url');

            for(let i=0; i< data.length; i++){

                let url_symbol_detail = $("#url-symbol-detail").attr('data-url');
                url_symbol_detail = url_symbol_detail.replace('/1234', data[i].company);

                let analyze =''
                if(data[i].isAnalyzed == true){
                    analyze = 'تحلیل شد (' + toJalaliDate(data[i].analyzedAt) + ')'
                }

                container.append(
                    `<div id="symbol-req-tile-${data[i].id}" class="media white z-depth-0 border rounded mb-1">` +
                        `<img src="${base}media/${data[i].symbolPic}" alt="" class="rounded-right z-depth-1" style="height: 53px; width: 53px; object-fit: contain">` +
                        `<div class="media-body p-1">` +
                            `<p class="text-uppercase text-muted mb-1"><span class="float-left small text-success">${analyze}</span><small>${toJalaliDate(data[i].createAt)}</small></p>` +
                            `<span class="float-left" onclick="removReqSymbol(${data[i].id}, 'symbol-req-tile-${data[i].id}')"> <i class="fa fa-trash text-black-50"></i></span>` +
                            `<a href="${base}${url_symbol_detail}" class=""><h5 class="font-weight-bold mb-0 small">` +
                                `${data[i].symbol}` +
                            `</h5></a>` +
                        `</div>` +
                    `</div>`
                );
            }
        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}

function removReqSymbol(symbolId, tile) {
    // console.log('reqto remove ', symbolId)

    let url_symbolList = $("#url-symbol-req-list").attr("data-url");

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'remove': symbolId
        },
        success: function (data) {
            // console.log(data);
            let itm = '#' + tile
            $(itm).remove();
        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}


function removePortfolioSymbol(symbolId, tile) {
    // console.log('reqto remove ', symbolId)

    let url_symbolList = $("#url-symbol-portfolio-list").attr("data-url");

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'remove': symbolId
        },
        success: function (data) {
            // console.log(data);
            let itm = '#' + tile
            $(itm).remove();
        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}

function loadAllPortfolioSymbols() {

    let url_symbolList = $("#url-symbol-portfolio-list").attr("data-url");
// alert(url_symbolList);
// return

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': user_id
        },
        success: function (data) {
            // console.log(data);
            // return;
            let container = $("#container-symbol-portfolio-list");
            container.empty();
            let base = $('#url-base').attr('data-url');

            for(let i=0; i< data.length; i++){

                let url_symbol_detail = $("#url-symbol-detail").attr('data-url');
                url_symbol_detail = url_symbol_detail.replace('/1234', data[i].company);

                container.append(
                    `<div id="symbol-portfolio-tile-${data[i].id}" class="media white z-depth-0 border rounded mb-1">` +
                        `<img src="${base}media/${data[i].symbolPic}" alt="" class="rounded-right z-depth-1" style="height: 53px; width: 53px; object-fit: contain">` +
                        `<div class="media-body p-1">` +
                            `<p class="text-uppercase text-muted mb-1"><small>${data[i].createAt}</small></p>` +
                            `<span class="float-left" onclick="removePortfolioSymbol(${data[i].id}, 'symbol-portfolio-tile-${data[i].id}')"> <i class="fa fa-trash text-black-50"></i></span>` +
                            `<a href="${base}${url_symbol_detail}" class=""><h5 class="font-weight-bold mb-0 small">` +
                                `${data[i].symbol}` +
                            `</h5></a>` +
                        `</div>` +
                    `</div>`
                );
            }

        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}


function loadUserRequestedSymbols(user_id) {

    let url_symbolList = $("#url-symbol-req-list").attr("data-url");
// alert(url_symbolList + "-" + user_id);
// return

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': user_id
        },
        success: function (data) {
            // console.log(data);
            // return;
            let container = $("#container-user-requests");
            container.empty();
            let base = $('#url-base').attr('data-url');

            for(let i=0; i< data.length; i++){

                let url_symbol_detail = $("#url-symbol-detail").attr('data-url');
                url_symbol_detail = url_symbol_detail.replace('/1234', data[i].company);

                container.append(
                    `<a href="${base}${url_symbol_detail}" target="_blank">` +
                        `<div  class="media white z-depth-0 border rounded mb-1 p-2">` +
                            `<i class="fa fa-angle-double-left ml-2 mt-1 text-black-50"></i>`+
                            `${data[i].symbol}` +
                        `</div>`+
                    `</a>`
                );
            }

        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}

function loadUserPortfolioSymbols(user_id) {

    console.log(user_id)

    let url_symbolList = $("#url-symbol-portfolio-list").attr("data-url");
// alert(url_symbolList);
// return

    $.ajax({
        url: url_symbolList,
        type: 'GET',
        dataType: 'json',
        data: {
            'q': user_id
        },
        success: function (data) {
            console.log(data);
            // return;
            let base = $('#url-base').attr('data-url');
            let container = $("#container-user-portfolio");
            container.empty();

            for(let i=0; i< data.length; i++){
                let url_symbol_detail = $("#url-symbol-detail").attr('data-url');
                url_symbol_detail = url_symbol_detail.replace('/1234', data[i].company);

                container.append(
                    `<a href="${base}${url_symbol_detail}" target="_blank">` +
                        `<div  class="media white z-depth-0 border rounded mb-1 p-2">` +
                            `<i class="fa fa-angle-double-left ml-2 mt-1 text-black-50"></i>`+
                            `${data[i].symbol}` +
                        `</div>`+
                    `</a>`
                );
            }

        },
        fail: function (e) {
            console.log('error', e);
        }

    })
}
