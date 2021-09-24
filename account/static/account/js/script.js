$('#following-btn').click(function () {
    let btn_class;
    let btn_text;
    let url;
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    const user_id = $("#following-btn").attr('data-id')
    const follow = $('#following-btn').text()

    if (follow === 'Follow') {
        url = '/account/follow/';
        btn_text = 'UnFollow';
        btn_class = 'btn btn-warning text-center mx-auto';
    } else {
        url = '/account/unfollow/';
        btn_text = 'Follow';
        btn_class = 'btn btn-primary text-center mx-auto';
    }


    $.ajax({
        url: url,
        method: 'POST',
        data: {
            'user_id': user_id,
        },
        success: function (data) {
            if (data['status'] === 'ok') {
                $("#following-btn").text(btn_text)
                $('#following-btn').attr({'class': btn_class})
            }
        }
    });
});