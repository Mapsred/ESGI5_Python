$(document).ready(function () {
    $("#action_submit").click(function () {
        var card = $("#profile_player_card").val();
        if (!card) {
            return false;
        }

        $("#profile_player_card option[value='" + card + "']").remove();

        $.ajax({
            url: '/combat/action/ajax',
            method: 'POST',
            data: {
                'player_card': card
            },
            dataType: 'json',
            success: function (data) {
                var selected_card_img = $("div#profile_" + card);
                $("#fighting_zone").prepend('<div class="action"></div>');
                selected_card_img.prependTo("#fighting_zone .action:first");

                var selected_target_card = data['selected_target_card'];
                selected_card_img = $("div#target_" + selected_target_card['player_card']);
                selected_card_img.appendTo("#fighting_zone .action:first");

                $("#" + data['looser']).addClass('looser');
                $("#" + data['winner']).addClass('winner');

                if (data['player_state'] === 'winner') {
                    increment($(".win"));
                } else {
                    increment($(".loose"));
                }
            }
        });

    });


    function increment(selector) {
        selector = $(selector);
        var value = parseInt(selector.html());
        value++;

        $(selector).html(value)
    }
});