$(document).ready(function(){

	//-- adjas message member win height --//
	$("#container-message-members").height(window.innerHeight * 0.6);
	// console.log(window.innerHeight)

	let timer_member;
	$("#search-member").on('keyup', function (e) {

		clearTimeout(timer_member);
		timer_member =setTimeout(function(){

			console.log($("#search-member").val());
			loadMemberList($("#search-member").val());

			}, 600);
		//
		// setTimeout(searchUser(), 10000);
		// if (e.keyCode === 13) {
		// 	let srchterm = $("#search-category").val();
		// 	let tag_a = document.getElementById("category-search-link");
		// 	tag_a.href = "?search-category=" + srchterm;
		// 	tag_a.click();
		// }
	});

	//-- load admin message --//
	selectMember('admin-member');

});

//-- load all member --//
function loadMemberList(search="") {

        let url_memberList = $("#url-member-list").attr("data-url");
         // alert(url_memberList);
         // return

        $.ajax({
            url: url_memberList,
            type: 'GET',
            dataType: 'json',
            data: {
            	'q': search,
            	'page_size': 20,
			},
            success: function (data) {
                // console.log(data);
				let container = $("#container-member-list");
				container.empty();
				let img_member = $("#img-member-placeholder").attr('src');
				// for(let i=0; i< Math.min(data.length, 20); i++){
				// selectMember()
				for(let i=0; i< data.length; i++){

					container.append(
						`<li id="member-${data[i].id}" value="${data[i].id}" data-page="1" class="myclass-member-tile p-1 border-bottom" style="margin-right: -30px">` +
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
						`</li>`
					);
				}

            },
			fail: function (e) {
            	console.log('error', e);
			}
        })

    }

//-- select on member --//
function selectMember(memberId, isAdmin=false, isFromHtml=false) {


	//-- select all li tag witch have two class myclass-member-tile and active. --//
	$('li.myclass-member-tile.active').removeClass('active grey lighten-3');

	let itm = "#" + memberId;
	$(itm).addClass('active grey lighten-3');

	//-- load first paget --//
	if(isFromHtml){
		$(itm).attr('data-page', '1');
	}

	let target = $(itm).attr('value');
	let url_messageGet = $("#url-message-create").attr("data-url");

	let sendData;

	if(isAdmin){
		sendData = {
			'user2admin': target,
			'admin': $('#admin-member').attr('value'),
			'page': parseInt($(itm).attr('data-page')),
		}
	}
	else{
		sendData = {
			'target': target,
			'page': parseInt($(itm).attr('data-page')),
		}
	}

	$.ajax({
		url: url_messageGet,
		type: 'GET',
		beforeSend: function (xhr, settings)
		{
        	xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
		dataType: 'json',
		data: sendData,
		success: function (resault) {
			// console.log(resault);
			let container = $('#container-message-members');
			if(sendData.page == 1){
				container.empty();
			}

			let img_member = $('#img-member-placeholder').attr('src');
			let img_admin = $('#img-admins-placeholder').attr('src');

			let data = resault.results;
			// console.log(parseInt($(itm).attr('data-page')))
			$(itm).attr('data-page', sendData.page+1);
			// console.log(sendData['page'])
			// console.log($(itm).attr('data-page'))


			for (let i=0; i<data.length; i++){

				const d = new Date(data[i].createAt);
				// request a weekday along with a long date
				let options2 = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
				, hour: 'numeric', minute: 'numeric', second: 'numeric'};
				let options = {
				  year: 'numeric', month: 'numeric', day: 'numeric',
				  hour: 'numeric', minute: 'numeric', second: 'numeric',
				};
				const date = new Intl.DateTimeFormat('fa-IR', options).format(d);
				let checkUser = isAdmin ? data[i].receiver : data[i].sender;
				let seenIcon = data[i].isSeen ? 'fa-check text-success' : 'fa-eye text-info';

				let deletPermition = data[i].sender == user_id ? '' : 'd-none';
				if(isAdmin) data[i].sender == $('#admin-member').attr('value') ? '' : 'd-none';
				// console.log(data[i].sender + '==' + $('#admin-member').attr('value') + "? " + (data[i].sender == $('#admin-member').attr('value')))
				//-- target is sender --//
				if(target == checkUser){
					container.prepend(
						`<li id="msg-contain-${data[i].id}" class="d-flex justify-content-between mb-4">` +
							`<img src="${img_admin}" alt="avatar" class="avatar rounded-circle d-flex img-thumbnail z-depth-1 ml-2" style="object-fit: contain; width: 60px; height: 60px; ">` +
							`<div class="chat-body white p-3 ml-1 mr-1 z-depth-1 rounded">` +
								`<div class="header">` +
									`<i class="fa ${seenIcon} small"></i>` +
									`<small class="pull-right text-muted"> ${date} <i class="far fa-clock"></i></small>` +
									`<strong class="primary-font">${data[i].sender_name}</strong>` +
								`</div>` +
								`<hr class="w-100">` +
								`<p class="mb-0">` +
									`${data[i].description}` +
								`</p>` +
								`<i class="fa fa-trash text-black-50 small float-left ${deletPermition}" onclick="deleteMsg(${data[i].id}, 'msg-contain-${data[i].id}')"></i>` +
							`</div>` +
						`</li>`
					);
				}
				else{
					container.prepend(
						`<li id="msg-contain-${data[i].id}" class="d-flex justify-content-between mb-4">` +
							`<div class="chat-body white p-3 ml-1 mr-1 z-depth-1 rounded">` +
								`<div class="header">` +
									`<i class="fa ${seenIcon} small"></i>` +
									`<small class="pull-right text-muted"> ${date} <i class="far fa-clock"></i></small>` +
									`<strong class="primary-font">${data[i].sender_name}</strong>` +
								`</div>` +
								`<hr class="w-100">` +
								`<p class="mb-0">` +
									`${data[i].description}` +
								`</p>` +
								`<i class="fa fa-trash text-black-50 small float-left ${deletPermition}" onclick="deleteMsg(${data[i].id}, 'msg-contain-${data[i].id}' )"></i>` +
							`</div>` +
							`<img src="${img_member}" alt="avatar" class="avatar rounded-circle d-flex img-thumbnail z-depth-1 ml-2" style="object-fit: contain; width: 60px; height: 60px; ">` +
						`</li>`
					);
				}
				
			}

			$('#li-member-more').remove();
			//-- add more button if item exist --//
			if(resault.count > (sendData.page*20)){
				container.prepend(
					`<li id="li-member-more" class="d-flex justify-content-center mb-4">` +
					`<a onclick="selectMember('${memberId}', ${isAdmin}, false)">بیشتر</a>` +
					`</li>`
				);
			}

			//-- scroll to end --//
			// console.log(sendData.page , resault.count , (sendData.page*20))
			if(sendData.page == 1){
				$('#container-message-members').scrollTop($('#container-message-members')[0].scrollHeight);
			}

		},
		fail: function (e) {
			console.log('error', e);
		}
	})
}

//-- delete message --//
function deleteMsg(msgId, msg_item) {

	console.log('delete ', msgId);

	let url_messageDelete = $("#url-message-delete").attr("data-url");
    url_messageDelete = url_messageDelete.replace('1234', msgId);

	$.ajax({
		url: url_messageDelete,
		type: 'DELETE',
		beforeSend: function (xhr, settings)
		{
        	xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
		// dataType: 'json',
		// data: {},
		success: function (data) {
			let itm = "#" + msg_item;
			$(itm).remove();
		}
	});
}

//-- send message --//
function sendMessage(isAdmin=false) {

	let msg = $('#txt-messageBox').val();
	let receiver = $('li.myclass-member-tile.active').attr('value');

	if(msg.length == 0){
		alert('متن پیغام خالی است');
		return;
	}
	if(receiver == undefined){
		alert('گیرنده انتخاب نشده است');
		return;
	}

	let url_messageCreate = $("#url-message-create").attr("data-url");

	let sendData;

	if(isAdmin){
		sendData = {
			'receiver': receiver,
			'description': msg,
			'sender': $('#admin-member').attr('value'),
		}
	}
	else{
		sendData = {
			'receiver': receiver,
			'description': msg,
			'sender': user_id,
		}
	}
	// alert(url_messageCreate, csrftoken)

	$.ajax({
		url: url_messageCreate,
		type: 'POST',
		beforeSend: function (xhr, settings)
		{
        	xhr.setRequestHeader("X-CSRFToken", csrftoken);
		},
		dataType: 'json',
		data: sendData,
		success: function (data) {
			console.log(data);
			let container = $('#container-message-members');

			let img_member = $('#img-member-placeholder').attr('src');
			let img_admin = $('#img-admins-placeholder').attr('src');

				const d = new Date(data.createAt)
				options = {
				  year: 'numeric', month: 'numeric', day: 'numeric',
				  hour: 'numeric', minute: 'numeric', second: 'numeric',
				};
				const date = new Intl.DateTimeFormat('fa-IR', options).format(d);

			if(isAdmin){
				container.append(
				`<li class="d-flex justify-content-between mb-4">` +
					`<img src="${img_admin}" alt="avatar" class="avatar rounded-circle d-flex img-thumbnail z-depth-1 ml-2" style="object-fit: contain; width: 60px; height: 60px; ">` +
					`<div class="chat-body white p-3 ml-1 mr-1 z-depth-1 rounded">` +
						`<div class="header">` +
							`<i class="fa fa-eye text-info small"></i>` +
							`<small class="pull-right text-muted"> ${date} <i class="far fa-clock"></i></small>` +
							`<strong class="primary-font">${data.sender_name}</strong>` +
						`</div>` +
						`<hr class="w-100">` +
						`<p class="mb-0">` +
							`${data.description}` +
						`</p>` +
					`</div>` +
				`</li>`
			);
			}
			else{
				container.append(
				`<li class="d-flex justify-content-between mb-4">` +
					`<div class="chat-body white p-3 ml-1 mr-1 z-depth-1 rounded">` +
						`<div class="header">` +
							`<i class="fa fa-eye text-info small"></i>` +
							`<small class="pull-right text-muted"> ${date} <i class="far fa-clock"></i></small>` +
							`<strong class="primary-font">${data.sender_name}</strong>` +
						`</div>` +
						`<hr class="w-100">` +
						`<p class="mb-0">` +
							`${data.description}` +
						`</p>` +
					`</div>` +
					`<img src="${img_member}" alt="avatar" class="avatar rounded-circle d-flex img-thumbnail z-depth-1 ml-2" style="object-fit: contain; width: 60px; height: 60px; ">` +
				`</li>`
			);
			}


			//-- clear text box --//
			$('#txt-messageBox').val('');

			//-- scroll to end --//
			$('#container-message-members').scrollTop($('#container-message-members')[0].scrollHeight);

			if(isAdmin){
				// location.reload();
				let str = "#member-unReadMsgCount-" + receiver
				$(str).remove();
			}

		},
		fail: function (e) {
			console.log('error', e);
		}
	})
}