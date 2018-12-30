$(document).ready(function () {
    $("#action_submit").click(function () {
        playAction();
    });

    var urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('auto') === 'true') {
        $(".card-list .form-group").hide();

        loopTimeout($("#profile_player_card option").length);

        function loopTimeout(i) {
            setTimeout(function () {
                playAction();

                if (--i) {
                    loopTimeout(i);
                }
            }, 2500);
        }
    }

    function playAction() {
        var card = $("#profile_player_card").val();
        if (!card) {
            return false;
        }

        $.ajax({
            url: '/combat/action/ajax',
            method: 'POST',
            data: {
                'player_card': card
            },
            dataType: 'json',
            success: function (data) {
                $("#fighting_zone").prepend('<div class="action"></div>');

                var selected_card_img = data['selected_player_card'];
                selected_card_img = $("div#profile_" + selected_card_img['player_card']);
                selected_card_img.prependTo("#fighting_zone .action:first");

                var selected_target_img = data['selected_target_card'];
                selected_target_img = $("div#target_" + selected_target_img['player_card']);
                selected_target_img.appendTo("#fighting_zone .action:first");

                $("#" + data['looser']).addClass('looser');
                $("#" + data['winner']).addClass('winner');

                $("#profile_player_card option[value='" + card + "']").remove();

                if (data['player_state'] === 'winner') {
                    increment($(".win"));
                } else {
                    increment($(".loose"));
                }

                checkEnd();
            }
        });
    }

    function increment(selector, number) {
        number = number || 1;

        selector = $(selector);
        var value = parseInt(selector.html());
        value = value + number;

        $(selector).html(value)
    }

    function checkEnd() {
        var player_card = $(".card-list").find("div[id^='profile']");
        var target_card = $(".card-list").find("div[id^='target']");

        var player_card_number = player_card.length;
        var target_card_number = target_card.length;

        var ended = false;
        var winner = 'draw';

        if (player_card_number === 0 && target_card_number === 0) {
            ended = true;
            var win = parseInt($(".win").html());
            var loose = parseInt($(".loose").html());
            var win_loose_phrase = 'You won ' + win + ' times and lost ' + loose + ' times.';

            var css = 'text-warning';
            var text = 'It is a draw';

            if (win > loose) {
                css = 'text-success';
                text = 'You won this fight';
                winner = 'player';
            } else if (win < loose) {
                css = 'text-danger';
                text = 'You lost this fight';
                winner = 'target';
            }

            $("#fighting_zone").prepend(
                '<div class="action">' +
                '   <p class="' + css + '">' +
                '        ' + win_loose_phrase + '<br> ' + text + ' !' +
                '   </p>' +
                '</div>');
        }

        if (player_card_number === 0 && !ended) {
            increment($(".loose"), target_card_number);
            ended = true;
            winner = 'target';

            $("#fighting_zone").prepend(
                '<div class="action">' +
                '   <p class="text-danger">' +
                '       You no longer have any card, and your opponent still have ' + target_card_number + ' cards.' +
                '       <br> You lost this fight !' +
                '   </p>' +
                '</div>');
        }

        if (target_card_number === 0 && !ended) {
            increment($(".win"), player_card_number);
            ended = true;
            winner = 'player';

            $("#fighting_zone").prepend(
                '<div class="action">' +
                '   <p class="text-success">' +
                '       Your opponent no longer have any card, and your still have ' + player_card_number + ' cards.' +
                '       <br> You won this fight !' +
                '   </p>' +
                '</div>');
        }


        if (ended) {
            $(".card-list .form-group").hide();
            $.ajax({
                url: '/combat/action/ajax',
                method: 'POST',
                data: {
                    'winner': winner
                },
                dataType: 'json',
                success: function (data) {

                }
            });

        }

    }
});