$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle=popover-img]').popover({
        html: true,
        trigger: 'hover',
        template: '' +
            '<div class="popover popover-img" role="tooltip">' +
            '   <h3 class="popover-header"></h3>' +
            '   <div class="popover-body"></div>' +
            '</div>',
        content: function () {
            return '<img src="' + $(this).data('img') + '" />';
        }
    });


    if (document.getElementById('cards_select')) {
        $('#cards_select').select2({
            maximumSelectionLength: 30,
            allowClear: true,
            closeOnSelect: false,
            templateResult: function (state) {
                if (!state.id) {
                    return state.text;
                }

                return $('<span data-img="' + $(state.element).data('img') + '">' + state.text + '</span>')
            }
        });

        var tooltip = '' +
            '<div class="popover popover-img manual-tooltip" style="display: none;opacity: 1;" role="tooltip">' +
            '   <h3 class="popover-header"></h3>' +
            '   <div class="popover-body"></div>' +
            '</div>';

        $('body').append(tooltip);

        var selector = '.select2-results__option';
        $(document).on('mouseenter', selector, function () {
            $('.manual-tooltip .popover-body').html('<img src="' + $(this).find('span').data('img') + '" />');

            $('.manual-tooltip').show().css({
                'left': ($(this).offset().left + $(this).outerWidth(true)) + 2,
                'top': parseFloat($('#cards_select').offset().top)
            });
        }).on('mouseleave', selector, function (e) {
            $('.manual-tooltip').hide();
        });
    }


});