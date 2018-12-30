$(document).ready(function () {
    //Update the messages
    setInterval(function () {
        fetch_messages();
    }, 5000);

    //Post the message
    $("#msg_send_btn").click(function () {
        submit_message();
    });

    //Post the message on enter key
    $('.write_msg').keypress(function (e) {
        if (e.which === 13) {
            submit_message();
        }
    });


    $("#write_msg").change(function () {
        $("#error").hide();
    });

    function fetch_messages() {
        $.ajax({
            url: '/accounts/messages/ajax',
            method: 'GET',
            data: {
                'contact': $("#contact").data("contact")
            },
            dataType: 'json',
            success: function (data) {
                write_messages(data);
            }
        });
    }

    function submit_message() {
        var message = $("#write_msg").val();
        if (message.length >= 1) {
            $.ajax({
                url: '/accounts/messages/ajax/post',
                method: 'POST',
                data: {
                    'contact': $("#contact").data("contact"),
                    'message': message
                },
                dataType: 'json',
                success: function (data) {
                    $("#write_msg").val("");
                    fetch_messages();
                }
            });
        } else {
            $("#error").show();
        }
    }

    function write_messages(messages) {
        var profile_id = $("#contact").data("profile");

        $(".msg_history").children().remove();
        $.each(messages['conversations'], function (key, message) {
            var clone;
            var content = "<p>" + message['message'] + "</p>" +
                "<span class='time_date'>" + message['date'] + "</span>";

            if (message['sender_id'] === profile_id) {
                clone = $(".model-msg .outgoing_msg").clone();
                clone.find(".sent_msg").html(content);
            } else {
                clone = $(".model-msg .incoming_msg").clone();
                clone.find(".received_withd_msg").html(content);
            }

            $(".msg_history").append(clone);
        });
    }

});