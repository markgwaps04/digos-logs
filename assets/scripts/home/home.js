


(function(jq) {

const btn_full_screen = jq("#full_screen");
const main_table = jq("#main");
const header = jq(".app-header");


document.addEventListener("fullscreenchange", function(e) {
    if (document.fullscreenElement) return;
    btn_full_screen_toggle_off();
});

const btn_full_screen_toggle_off = function() {
    main_table.removeClass("fullscreen");
    header.removeClass("hide");
    btn_full_screen.addClass("btn-light");
    btn_full_screen.removeClass("btn-focus");
    document.exitFullscreen()
    btn_full_screen
        .off("click")
        .on("click",btn_full_screen_toggle_on);

};

const btn_full_screen_toggle_on = function() {
    main_table.addClass("fullscreen");
    header.addClass("hide");
    btn_full_screen.removeClass("btn-light");
    btn_full_screen.addClass("btn-focus");
    document.documentElement.requestFullscreen()
    btn_full_screen
        .off("click")
        .on("click",btn_full_screen_toggle_off);

};

btn_full_screen.on("click", btn_full_screen_toggle_on);

})(jQuery);




(function(jq){

vex.defaultOptions.className = "vex-theme-top";

const jsgrid_table = jq(".jsgrid.main");

$.fn.init_modal = function(obj)
{
    const on_default = {
        callback_func : function(){},
        string_parent_container : null,
        confirmation : false,
        confirmation_message : "Are you sure you want to made a changes"
    };

    obj = {...on_default,...obj};

    const $element = jQuery(this);

    const change_state = function(form) {

        const $selected_element = jQuery(form);

        const parent_container = obj.string_parent_container
            ? jq(string_parent_container)
            : $selected_element.closest(".modal");

        const spinner = parent_container.find(".overlay-spinner");
        const data = $selected_element.serialize_form();
        const modal = jQuery(".modal");


        const send = jq.ajax({
            url : form.action,
            headers: {"X-CSRFToken": jq.cookie("csrftoken")},
            data : data,
            type : "post",
            beforeSend : function() {
                spinner.addClass("show");
            },
            success : function() {
                spinner.removeClass("show");
            }
        });

        send.done(function(response) {

            /** hide all shown and existing modal **/

            modal.modal('hide');

            /** end modal **/

            const template = jQuery(response);
            if(!template.is(".modal"))
                return alert('Error occured during fetching contents, please reload the page!');


            template
                .modal("show")
                .on("hidden.bs.modal", function() {
                    template.find('[data-dismiss="modal"]').click();
                    template.remove();
                });

            obj.callback_func(template);
        });

    };

    $element.off("submit");
    $element.submit(function(event) {
        event.preventDefault();
        const that_form = this;

        if(obj.confirmation)
        {

            return vex.dialog.confirm({
                message : obj.confirmation_message,
                callback : function(value)
                {
                    if (!value) return false;
                    return change_state(that_form);
                }
            });

        }

        return change_state(that_form);


    });


};

jsgrid_table.jsGrid({
    inserting: false,
    editing: false,
    filtering: false,
    width: "100%",
    heading: false,
    paging: true,
    autoload: true,
    pageSize: 10,
    paging:true,
    pageLoading:true,
    pagerContainer : jq("#main .pagination"),
    pageIndex:1,
    controller: {
    loadData : function(filter)
    {
        const filter_form = jq("form#form-filter");
        const filter_alert = jq("#main .filter-alert");
        const data_params_filter = filter_form.serialize_form();

        is_filtered = Object.values(data_params_filter).filter(Boolean);
        filter_alert.addClass("hidden");

        if(is_filtered.length > 0)
             filter_alert.removeClass("hidden");

        const params = {};
        const data = {...params, ...data_params_filter, ...filter};
        const send = jq.ajax({
            url : "/log/populate",
            headers: {"X-CSRFToken": jq.cookie("csrftoken")},
            data : data,
            type : "post",
        });

        return new Promise(function(resolve) {
            send.done(function(response)
            {
                jsgrid_table.jsGrid("_hideLoading");
                const is_valid = String(response).valid_selector_jquery();
                const $res_element = jq(response);
                const length = $res_element.attr("item_count") || 0;
                if(!Number(length) && Number(length) <= 0)
                {

                    return resolve({
                        data: [],
                        itemsCount: length
                    });
                }

                resolve({
                    data: [response],
                    itemsCount: length
                });

            });

        });

    }
    },
    loadIndicator : {
        show : () => jq("#main .overlay-spinner").addClass("show"),
        hide : () => jq("#main .overlay-spinner").removeClass("show")
      },
    rowRenderer : function(template)
    {
        const of_template = jQuery(template);
        const more_link = of_template.find(".more");

        const modal_content = function(result) {

             const inner_init_modal = result
                .find("form.init_modal")
                .init_modal({
                    callback_func: () => {
                        jsgrid_table.jsGrid("loadData");
                    },
                    confirmation: true
                });



        };

        const init_modal = of_template
            .find("form.init_modal")
            .init_modal({ callback_func: modal_content });


        if (more_link.length) more_link.read_more(100);
        return of_template;


      },
    noDataContent: function () {
        const container = jq("<div>");
        container.addClass("inner_content");

        const per = jq("<div>");
        container.addClass("no_display");

        const title = jq("<h4>");
        title.html("No display");

        per.append(title);
        per.append('<p>' +
          '<span>'+
          'We cant find any information or source' +
          '</span>' +
          '</p>');

        container.append(per);

        return container;

      }
    });

})(jQuery);


//Filter

(function(jq) {

var start = moment().subtract(29, 'days');
var end = moment();

const filter_form = jq("form#form-filter");
const jsgrid_table = jq(".jsgrid.main");
const date_range = jq("form#form-filter #daterange");
const start_date = date_range.children("[name='start_date']");
const end_date = date_range.children("[name='end_date']");


window.test = filter_form;


function cb(start, end) {
     date_range.children(".date_range_input").val(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
     start_date.val(start.format('YYYY-MM-D'));
     end_date.val(end.format('YYYY-MM-D'));
}


date_range.daterangepicker({
  startDate: start,
  endDate: end,
  ranges: {
     'Today': [moment(), moment()],
     'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
     'Last 7 Days': [moment().subtract(6, 'days'), moment()],
     'Last 30 Days': [moment().subtract(29, 'days'), moment()],
     'This Month': [moment().startOf('month'), moment().endOf('month')],
     'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
     }
}, cb);

date_range.on('apply.daterangepicker', function(ev, picker) {
  //do something, like clearing an input
  filter_form.trigger("reload");
});


function delay(callback, ms) {
  var timer = 0;
  return function() {
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      callback.apply(context, args);
    }, ms || 0);
  };
}
filter_form.on("reset", function() {
    start_date.val('');
    end_date.val('');
    filter_form.trigger("reload");
});

jq(".reset-filter").click(function() {
    filter_form.trigger("reset");
});

filter_form.on("keyup change reload",delay(function() {

    const send = jsgrid_table.jsGrid("search")
    send.done(function(result) {
//        console.log(result);
    });

},500));

})(jQuery)
