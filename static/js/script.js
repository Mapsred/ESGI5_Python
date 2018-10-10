$.fn.dataTable.ext.order['dom-checkbox'] = function (settings, col) {
    return this.api().column(col, {order: 'index'}).nodes().map(function (td, i) {
        return $('input', td).prop('checked') ? '1' : '0';
    });
};

var Table = {
    MAX_CARDS: 30,

    init: function () {
        Table.initTable();
    },

    initTable: function () {
        $('#dataTable tfoot th').each(function () {
            let title = $(this).text();
            let disabled = $(this).hasClass('disabled') ? 'disabled' : '';

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

    },

    handle_cards: function () {
        var checked_cards = $(".card-checkbox:checkbox:checked").toArray();

        $('#dataTable_wrapper').on("click", ".card-checkbox", function (e) {
            $(this).is(":checked") ? checked_cards.push(e.target) : Table.remove_target(checked_cards, e.target);

            if (checked_cards.length > Table.MAX_CARDS) {
                e.preventDefault();
                Table.remove_target(checked_cards, e.target);
                alert("Warning ! You can only have up to 8 cards in a deck !")
            }
        });
    },

    remove_target: function (checked_cards, target) {
        var index = checked_cards.indexOf(target);
        if (index > -1) {
            checked_cards.splice(index, 1);
        }
    },
};


$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();

    if (document.getElementById('dataTable')) {
        Table.init();
        Table.handle_cards()
    }
});