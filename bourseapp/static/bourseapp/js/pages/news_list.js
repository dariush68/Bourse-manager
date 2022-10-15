

$('.ok').on('click', function(e){
    alert($("#news-table tr.selected td:first").html());
});

// Material Select Initialization
$(document).ready(function() {
    $('.mdb-select').materialSelect();
    $('.select-wrapper.md-form.md-outline input.select-dropdown').bind('focus blur', function () {
        $(this).closest('.select-outline').find('label').toggleClass('active');
        $(this).closest('.select-outline').find('.caret').toggleClass('active');
    });
});

//-- input check --//
$('input[type="checkbox"]').click(function(){
    console.log("imp: " + $(this).attr('dataId'));

    if($(this).prop("checked") == true){
        console.log("Checkbox is checked.");
        updateNewsImportant(true, $(this).attr('dataId'));
    }
    else if($(this).prop("checked") == false){
        console.log("Checkbox is unchecked.");
        updateNewsImportant(false, $(this).attr('dataId'));
    }
});

//-- edit news important --//
function updateNewsImportant(isImportant, newsId) {

    console.log(isImportant, newsId)

	let url_updateNews = $("#url-news-update").attr("data-url");

	$.ajax({
		url: url_updateNews,
		type: 'POST',
		beforeSend: function (xhr, settings)
		{
        	xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
		// dataType: 'json',
		data: {
		    'newsId': newsId,
		    'important': isImportant,
        },
		success: function (resault) {
			// console.log(resault);

		},
		fail: function (e) {
			console.log('error', e);
		}
	})
}

