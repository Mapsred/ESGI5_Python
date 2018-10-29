$.fn.dataTable.ext.order['dom-checkbox'] = function (settings, col) {
    return this.api().column(col, {order: 'index'}).nodes().map(function (td, i) {
        return $('input', td).prop('checked') ? '1' : '0';
    });
};

var Table = {
    init: function () {
        Table.initTable();
    },

    initTable: function () {
        $('#dataTable tfoot th').each(function () {
            var title = $(this).text();
            var disabled = $(this).hasClass('disabled') ? 'disabled' : '';

            $(this).html('<input type="text" class="form-control column_search" style="width: 100%" ' +
                'placeholder="' + title + '" ' + disabled + ' />');
        });

        Table.table = $('#dataTable').DataTable({
            "order": [[4, 'desc']],
            "scrollX": true,
            "searchDelay": 350,
            "bDeferRender": true,
            "sPaginationType": "full_numbers",
            "pagingType": "full_numbers",
            "aoColumns": [null, null, null, null, {'sSortDataType': "dom-checkbox"}]
        });

        $('#dataTable_wrapper').on('keyup', ".column_search", function () {
            Table.table.column($(this).parent().index()).search(this.value).draw();
        });
    }
};


var TableCards = {
    MAX_CARDS: 30,

    total: 0,
    cards: {},

    handle_cards: function () {
        TableCards.fill_checked_cards();
        TableCards.cards_total();

        $('#dataTable_wrapper').on("change", ".card_count", function (e) {
            TableCards.fill_checked_cards();
            TableCards.cards_total();
            if (TableCards.total > TableCards.MAX_CARDS) {
                e.preventDefault();
                alert("Warning ! You can only have up to" + TableCards.MAX_CARDS + " cards in a deck !")
            }
        });
    },

    fill_checked_cards: function () {
        $("input.card_count").each(function () {
            var tr = $(this).parent().parent().parent();
            var name = tr.children("td").first().text();
            TableCards.cards[name] = $(this).val();
        });
    },

    cards_total: function () {
        TableCards.total = 0;
        $.each(TableCards.cards, function (card, nb) {
            TableCards.total += parseInt(nb);
        });
    }
};


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


    if (document.getElementById('dataTable')) {
        Table.init();
        TableCards.handle_cards()
    }
});